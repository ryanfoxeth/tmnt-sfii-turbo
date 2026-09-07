"""Small, dependency-free reader for standard BPS patches.

This module implements the public BPS file-format specification.  It is kept
separate from Floating IPS so the release can be applied on Python 3.9+ without
shipping a platform-specific executable.
"""

from __future__ import annotations

import struct
import zlib
from dataclasses import dataclass
from typing import Dict, Tuple


class BPSError(ValueError):
    """A BPS patch is malformed or does not match its source."""


@dataclass(frozen=True)
class PatchInfo:
    source_size: int
    target_size: int
    source_crc32: int
    target_crc32: int
    patch_crc32: int
    command_counts: Dict[str, int]
    literal_bytes: int
    moved_source_bytes: int


_NAMES = ("source_read", "target_read", "source_copy", "target_copy")


def _crc32(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def _read_number(data: bytes, pos: int, limit: int) -> Tuple[int, int]:
    value = 0
    shift = 1
    while True:
        if pos >= limit:
            raise BPSError("unexpected end of BPS data")
        byte = data[pos]
        pos += 1
        value += (byte & 0x7F) * shift
        if byte & 0x80:
            return value, pos
        shift <<= 7
        value += shift


def _parse_header(patch: bytes) -> Tuple[int, int, int, int, Tuple[int, int, int]]:
    if len(patch) < 16 or patch[:4] != b"BPS1":
        raise BPSError("not a BPS1 patch")
    footer_start = len(patch) - 12
    if _crc32(patch[:-4]) != struct.unpack_from("<I", patch, len(patch) - 4)[0]:
        raise BPSError("BPS patch CRC32 does not match")
    pos = 4
    source_size, pos = _read_number(patch, pos, footer_start)
    target_size, pos = _read_number(patch, pos, footer_start)
    metadata_size, pos = _read_number(patch, pos, footer_start)
    if metadata_size > footer_start - pos:
        raise BPSError("BPS metadata extends into the footer")
    pos += metadata_size
    checksums = struct.unpack_from("<III", patch, footer_start)
    return source_size, target_size, pos, footer_start, checksums


def inspect_patch(patch: bytes) -> PatchInfo:
    """Return patch metadata and command metrics after validating structure."""
    source_size, target_size, pos, footer_start, checksums = _parse_header(patch)
    output_size = 0
    source_relative = 0
    target_relative = 0
    counts = {name: 0 for name in _NAMES}
    literal_bytes = 0
    moved_source_bytes = 0

    while pos < footer_start:
        command, pos = _read_number(patch, pos, footer_start)
        action = command & 3
        length = (command >> 2) + 1
        if length > target_size - output_size:
            raise BPSError("BPS command writes past target size")
        counts[_NAMES[action]] += 1
        if action == 0:
            if output_size + length > source_size:
                raise BPSError("SourceRead exceeds source size")
        elif action == 1:
            if length > footer_start - pos:
                raise BPSError("TargetRead extends into BPS footer")
            pos += length
            literal_bytes += length
        else:
            offset, pos = _read_number(patch, pos, footer_start)
            delta = offset >> 1
            if offset & 1:
                delta = -delta
            if action == 2:
                source_relative += delta
                if source_relative < 0 or source_relative + length > source_size:
                    raise BPSError("SourceCopy points outside source")
                source_relative += length
                moved_source_bytes += length
            else:
                target_relative += delta
                if target_relative < 0 or target_relative >= output_size:
                    raise BPSError("TargetCopy points outside produced target")
                target_relative += length
        output_size += length

    if pos != footer_start or output_size != target_size:
        raise BPSError("BPS commands do not exactly produce the target")
    return PatchInfo(source_size, target_size, *checksums, counts, literal_bytes, moved_source_bytes)


def apply_bps(source: bytes, patch: bytes) -> Tuple[bytes, PatchInfo]:
    """Validate and apply *patch* to *source*, returning target bytes and info."""
    info = inspect_patch(patch)
    if len(source) != info.source_size:
        raise BPSError("source size does not match BPS patch")
    if _crc32(source) != info.source_crc32:
        raise BPSError("source CRC32 does not match BPS patch")

    _, target_size, pos, footer_start, _ = _parse_header(patch)
    target = bytearray()
    source_relative = 0
    target_relative = 0
    while pos < footer_start:
        command, pos = _read_number(patch, pos, footer_start)
        action = command & 3
        length = (command >> 2) + 1
        if action == 0:
            target.extend(source[len(target):len(target) + length])
        elif action == 1:
            target.extend(patch[pos:pos + length])
            pos += length
        else:
            offset, pos = _read_number(patch, pos, footer_start)
            delta = offset >> 1
            if offset & 1:
                delta = -delta
            if action == 2:
                source_relative += delta
                target.extend(source[source_relative:source_relative + length])
                source_relative += length
            else:
                target_relative += delta
                for _ in range(length):
                    target.append(target[target_relative])
                    target_relative += 1
    if len(target) != target_size or _crc32(target) != info.target_crc32:
        raise BPSError("generated target CRC32 does not match BPS patch")
    return bytes(target), info
