# Current status — v29

Reviewed September 12, 2026. [Start here](README.md). The final release hash is authoritative; historical guides are not current status.

## Delivered

| Area | Final behavior |
| --- | --- |
| Fighter art | All twelve slots reskinned; original fighting behavior retained. Complete body-pose import work includes effects/attachments and later corrections. |
| Roster | Ryu → Leo/Don; Ken → Raph/Mikey; Honda → Bebop; Blanka → Leatherhead; Guile → Casey; Chun-Li → April; Zangief → Slash; Dhalsim → Splinter; dictator → Krang; claw → Shredder; boxer → Rocksteady; Sagat → Super Shredder. |
| Stages | Eleven replacement rooms plus Leatherhead's retained riverside with night palettes. Leo: close Japanese night backstreet. Raph: SoHo Sewer. Slash: Dimension X scrapyard, original foreground fence, plain floor. Three distinct Technodrome concepts are preserved and used for Shredder/Super/Krang. |
| Portraits/UI | Separate icons, neutral, injured and continue appearances; full opaque icon interiors and borders; inward-facing neutral portraits; names/quotes; twelve TMNT biography packets. |
| Alternates | Start selects Don or Mikey; attack buttons select Leo/Raph. Costume-aware HUD, select, VS and winner names; aggregate records intentionally share LEO/DON and RAPH/MIKEY. |
| Projectile | Casey's Sonic Boom is visually a hockey stick, with its required release DMA preserved. Original attack properties and Flash Kick remain. |
| Endings | Fourteen illustrated endings, two story pages per identity, five common credit cards, localized native environmental motion and continuous stock ending music with native title/menu return. |
| Voices | Accepted Casey/Splinter/Shredder/Super voices plus shared turtle movie calls, April movie snippets and selected cartoon villain calls. V29 adds actor-private routes and scoped events where native sharing required it. |
| Media | Native CPU-versus-CPU capture recipes, full matches, all endings and voice showcase; latest landscape showcase 69.06 s, full progress recap 179.36 s. Media are identified by build and provenance. |

## Open, paused and intentionally retained

| ID | State | Next action |
| --- | --- | --- |
| VIS-02 | **Open: turtle idle polish.** Connected v8-derived motion is improved but still not fully accepted. Later pilots failed the fixed-head requirement and were not imported. | One short native Leo/Raph pilot: stable head/neck and feet, small shoulder/arm movement, more torso than upper-leg motion; avoid stretched bands or pasted body blocks. Have Ryan review the actual loop before expanding. |
| MUS-01 | **Paused by Ryan.** Original music stays in the release. Native MIDI Music Lab and cartoon-theme experiment are preserved privately. | Resume only on a new request. Arrangement, percussion, mix and fast-cue transitions are not a finished production soundtrack. |
| AUD-01 | **Selected voice pass complete.** Short shared hurt grunts and April KO remain stock. Four turtles share three calls. | Further performance/source-ambience changes are optional; no pending blanket instruction to replace every sound. Preserve original impacts/non-vocal effects. |
| Presentation | Original title/logo, world map and geography retained. | Optional future art scope, not automatically a broken-feature backlog. |
| Portability | Public patching works cross-platform; native authoring/capture was exercised on Linux. | Restore dependencies and test a bounded native route on the new host. macOS/Windows native core/player validation remains unclaimed. |

No new roster has been selected. Mortal Kombat is an example of a future SFII skin set. Using MK fighters here would still give them their mapped SFII moves unless a separate gameplay project is requested.

## Repaired defects — do not reopen without current evidence

- v11 and subsequent ownership audits: map/bonus/destructible graphics corruption caused by assuming non-fighter resources were unused.
- v13: Shredder's stage scroll/cage compensation. This is separate from animation tile writes.
- v15: old decorative background animation writing obsolete graphics; stage-specific retirement preserves mechanical objects. Leatherhead's retained native scene intentionally still animates.
- v17/v18: Leatherhead/Slash inconsistent sizing, clipped select busts, blank icon bands, missing borders/backgrounds; Super waist poses 000–003.
- v19: Splinter standing orientation, both player sides.
- v20: Slash's new room preserves the original compressed stream also used by bonus scene 13; Casey release-pose auxiliary graphics restored.
- v21/v22: Normal/Turbo alternate-palette normalization and costume-aware names across separate text systems.
- v23: Mikey/Raph raised-arm victory pose 073's missing second DMA load.
- v25: Super walking poses 004/005 missing 204 waist pixels; twelve biography packets and continuous ending music.
- v28: Slash/Leatherhead burn silhouettes had wrongly imported body graphics; Splinter flame OAM restored for poses 111–117.
- v29: shared voice conflicts handled with private actor resources and guarded events. Wrong pointer-table offset +4 and instrument address guesses were rejected, not shipped.

## Evidence and limits

The v29 release has 24 component voice routes, focused final both-side/KO/Normal routes, 38 live sample-hash checks, and a fresh 39,163-frame Slash Turbo Arcade campaign through all twelve stages, three bonuses, seven ending/credit pages and title/menu. It preserves 34 song resources, common effects, accepted voice resources, 1,962 graphics consumers and 27 scene graphs. Public release QA: 38 tests and 19 actual patcher input routes; the historical 92-file audit count grows with these new docs.

Earlier targeted campaigns establish their own documented coverage. Matching static resources supports preservation; it does not mean every earlier native route was rerun on every release. Some captures use health/controller fixtures and are demonstrations. There is no exhaustive every-matchup/physical-console certification or universal frame-identity claim. If a defect appears, record ROM SHA, mode, side, costume, stage, move/pose, time and emulator before diagnosing it.

Private evidence: `KNOWN-ISSUES.md`, `README-Voices-V29.md`, `work/all-voices-v29/delivery.json`, `work/all-voices-v29/combined-r5/verification.json`, and the earlier versioned guides/receipts. [Verification workflow](VERIFICATION-AND-VIDEO.md).
