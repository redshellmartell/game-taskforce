# Heavenly Bodies v2: card list (cycle 0)

56 cards: 52 Body cards and 4 Star cards. Machine-readable copy: `cards.json`. No tokens, no board.

## 1. Body cards (52)

Every colour has the same 13 Sizes: 1,1, 2,2,2, 3,3,3, 4,4,4, 5,5. Colours: **Ember** (red, E), **Frost** (blue, F), **Verdant** (green, V), **Solar** (gold, S). Card id = colour letter + Size + copy letter (for example `F3b`).

| Size | Kind | Card text | Ember | Frost | Verdant | Solar | Total |
|---|---|---|---|---|---|---|---|
| 1 | Comet | Captures a Giant. | E1a, E1b | F1a, F1b | V1a, V1b | S1a, S1b | 8 |
| 2 | Moon | (none) | E2a, E2b, E2c | F2a, F2b, F2c | V2a, V2b, V2c | S2a, S2b, S2c | 12 |
| 3 | World | (none) | E3a, E3b, E3c | F3a, F3b, F3c | V3a, V3b, V3c | S3a, S3b, S3c | 12 |
| 4 | Ringed World | (none) | E4a, E4b, E4c | F4a, F4b, F4c | V4a, V4b, V4c | S4a, S4b, S4c | 12 |
| 5 | Giant | Captured by a Comet. | E5a, E5b | F5a, F5b | V5a, V5b | S5a, S5b | 8 |
| | | | 13 | 13 | 13 | 13 | **52** |

Card face: large Size number in two corners, colour band, kind icon (comet tail, small moon, globe, ringed globe, giant). Card names are the colour plus the kind (for example "Frost Ringed World"); individual names can be added for art later without changing rules.

Statistics: mean Size 3.0; per colour total 39; Sizes 2-4 are 36 of 52 cards.

## 2. Star cards (4)

| Id | Name | Text (reference only, no ability) |
|---|---|---|
| ST1 | Ember Sun | Slots: North (away from you), East (your right), South (toward you), West (your left). Turn: Draw, Launch, Spin, Crash, Cool down (hand 5). Win at the start of your turn with 4 bodies: Critical Mass 15+, Constellation (one colour), Grand Alignment (1-2-3-4 or 2-3-4-5). |
| ST2 | Frost Sun | Same as ST1. |
| ST3 | Verdant Sun | Same as ST1. |
| ST4 | Solar Sun | Same as ST1. |

Star colour has no rules effect.

## 3. Dead-card check
- Comets (1): beat Giants; complete 1-2-3-4 Alignments; cheap Constellation fillers.
- Moons (2): needed for both Alignments; Constellation fillers; beat Comets.
- Worlds (3) and Ringed Worlds (4): needed for both Alignments; core of Critical Mass; mid-strength fighters.
- Giants (5): Critical Mass; 2-3-4-5 Alignment; strongest fighters except against Comets.
