# Heavenly Bodies — Complete Game Design Document

**Consolidated reference.** This single file concatenates all four working documents for the project, unedited, in dependency order: the canonical rules, the full decision-history audit, the current Star roster, and the active build/test brief. Hand this whole file to any Claude Code session (or any collaborator) and it is fully self-contained — no other file needs to be attached alongside it.

**Contents:**
1. Rules v2 (canonical ruleset)
2. Star Roster (12 cards, working list)
3. Design Audit & Project Log (full reasoning trail + decision log)
4. Build & Test Brief (current work order: generate 36 COs + 60 AEs, then simulate)

---
---

# PART 1 — RULES v2 (CANONICAL, LIVING DOCUMENT)

**Status:** IN PROGRESS. This document contains only fully locked decisions. Anything not yet resolved is marked `[OPEN — see Audit]` rather than guessed at. Do not treat silence on a topic as an answer — check the linked Audit document's status board before assuming a rule is settled.

**Paper trail:** every rule below was decided in the companion Design Audit & Project Log (Part 3 of this file), which records the reasoning, the date/session, and the alternatives that were considered and rejected. This document is the *what*; the Audit is the *why*.

## 1. Game Overview

Heavenly Bodies is a strategy card game of orbital mechanics. Players represent celestial forces — each anchored by a **Star** card — building a system of orbiting Celestial Objects (COs) and using Astronomical Events (AEs) to attack, defend, and maneuver toward one of two win conditions.

**Supported modes:** the game supports both **1v1** and **multiplayer free-for-all (3+ players, last-planet-standing)** as first-class modes, using the same core ruleset. `[LOCKED]`

## 2. Win Conditions

Two win conditions, designed to be equally viable:

1. **Star Destruction:** Reduce an opponent's Star HP to 0. **Checked immediately** the instant HP reaches 0, at any point in the turn — does not wait for End of Turn. `[LOCKED]` Applies identically to **self-inflicted** HP loss (e.g., an AE's own cost) — a player who drops their own Star to 0 loses, exactly as if an opponent had done it. In multiplayer, the last player remaining wins; an eliminated player's **orbit and hand** are fully removed to the discard pile, and their seat is skipped in turn order. `[LOCKED]` **Any cards the eliminated player previously sent to the shared Out of Orbit zone are unaffected** — that zone is ownerless/open-access by rule (§6), so nothing there is tied to the eliminated player specifically; it remains in play for the rest of the game. `[LOCKED]`
2. **Critical Mass:** The moment a player's total Size **currently in orbit** reaches **15+** (COs in the Out of Orbit zone never count toward this total), it is announced. `[LOCKED — checked only at End of Turn, per §7; not evaluated mid-phase.]` If their total Size is **still ≥15 at the end of their very next turn**, they win immediately. `[LOCKED]` If total Size drops below 15 at *any point* before that deadline, the countdown cancels and must be re-triggered by reaching 15 again. **Re-trigger deadline is always the achiever's next turn, never the current turn:** even if a cancelled countdown is re-triggered later within that same turn (e.g., the deadline turn itself), the new deadline is still "end of the achiever's *next* turn" — never that same turn's own End of Turn. `[LOCKED]` This preserves a full round of counterplay regardless of when in a turn the re-trigger happens. **No restriction on targeting a player mid-countdown:** an AE may target any Star, including one currently mid-Critical-Mass-countdown, unless the card states otherwise. `[LOCKED]` **No tie-break rule needed for "simultaneous" Critical Mass:** since turns are strictly sequential and both win conditions are checked immediately when true, there is no moment where two players' win-checks occur at once — whichever player's check comes first in actual turn order resolves first, and the game ends immediately if they win, before any other pending countdown can matter. `[LOCKED]` If a player is eliminated via Star Destruction while another player has an active Critical Mass countdown running against them, that is simply the outcome — no special protection exists for a countdown in progress. `[LOCKED]`

## 3. Core Attributes

- **Size (1–5):** A CO's contribution toward Critical Mass.
- **Stability (1–5):** A CO's resistance to being knocked out of orbit.
- **Hard floor:** Size and Stability can never be reduced below **0** by any effect. `[LOCKED]`
- **Knockout threshold:** A CO is knocked Out of Orbit when its Stability reaches exactly **0**. `[LOCKED]`
- **Size-0 removal:** A CO whose Size reaches exactly **0** is immediately removed from orbit and **discarded** (not sent to Out of Orbit — it skips that zone entirely). `[LOCKED]`
- **Effective stats:** All thresholds and comparisons (Collision resolution, Critical Mass totals, Stability-0/Size-0 knockout) use a CO's **current effective Size/Stability** — printed value adjusted by all active modifiers (Augmentations, ongoing effects) — never the printed base value alone. `[LOCKED]` A permanent/passive reduction knocks a CO out the moment effective Stability/Size hits 0; a temporary effect likewise triggers knockout the moment it brings the effective value to 0 (checked at the moment the effect applies, not retroactively).

## 4. Orbit & Rotation

- Each player has **4 orbital positions**: **North, East, South, West.** `[LOCKED]` Seasons (Winter/Spring/Summer/Fall) may appear as visual/thematic dressing on the board or Star card but are not used in rules text.
- **Rotation scope:** Rotation is **per-player** — only the active player's own COs rotate, and only during their own turn. `[LOCKED]` Individual cards may override this default (e.g., an effect that rotates an opponent's CO), but there is no global/simultaneous rotation of all players' COs.
- Rotation direction (clockwise by default, per original notes) and full Rotation Phase sequencing: `[OPEN — folded into Turn Structure, see Audit Tier 0 #7]`.

## 5. Placing COs & Collisions

**Collision, defined:** a Collision occurs whenever two COs would occupy the same cardinal position — whether caused by rotation, or by a CO being placed there (from hand, via reclaim, or by any other placement effect). `[LOCKED]` This is a single unified event; the same resolution applies regardless of what caused it. This supersedes the earlier separate "Overtake" (placement) and "rotation-phase collision" mechanics, which are now one system.

**Placement is always legal**, including onto an occupied position — subject only to whatever restriction is printed on the CO's own card (e.g., "must enter North"). `[LOCKED]` There is no longer an "illegal Overtake": any placement that satisfies the card's own restriction succeeds, and a Collision resolves immediately if the position was occupied.

**Collision resolution hierarchy:** `[LOCKED — supersedes the alternate "highest Size+Stability sum wins" draft from the original design notes]`
1. **Stability (main):** the CO with lower effective Stability is knocked to the Out of Orbit zone.
2. **Size:** if Stability is tied, the CO with smaller effective Size is knocked to the Out of Orbit zone.
3. **Full tie:** if both Stability and Size are tied, the **incoming/moving CO wins** — the one entering or rotating into the position knocks out the one already there.
4. AE effects and CO/Star abilities may override or modify this resolution when their own text explicitly says so.

**Placement always counts as 1 of the turn's 2 plays** (or the relevant action cost — a free ability use, or an AE play), regardless of whether the placed CO wins or loses its Collision. `[LOCKED]` A CO that loses a Collision immediately upon placement is still considered to have entered orbit for "enters orbit" trigger purposes (§10) before being knocked out — both triggers fire, in that order. `[LOCKED]` This enables deliberate sacrifice plays into knockout-triggered abilities.

**No CO is ever "unplayable due to a full orbit."** `[LOCKED — supersedes the earlier "Unplayable CO" rule.]` Since placement into an occupied position is always legal, a CO can always be placed as long as it satisfies its own printed restrictions, if any. The only way a placement could fail is a card explicitly requiring an *empty* specific position (e.g., "must enter an empty North") — a pattern no current card uses, but remains legal design space.

**CO-per-turn cap:** at most **1 CO may enter a player's orbit per turn**, from any source (a fresh play from hand, a reclaim, or otherwise) — this is a separate, stricter limit than the general "2 plays per turn" cap, not an additional 2. `[LOCKED]` Specific Star abilities or AE cards may explicitly override this cap (e.g., "you may reclaim an additional CO this turn, ignoring the normal cap") as a rare, high-value exception — this is intended as a real archetype identity (particularly for Out-of-Orbit-focused Stars), not a loophole. **Rationale:** without this cap, playing 2 COs per turn could fill an entire 4-slot orbit by a player's second turn, making Critical Mass reachable as early as turn 2–3 — dramatically faster than a realistic Star Destruction race. Modeled turns-to-win with the cap in place (~turn 6–8) land much closer to a comparable pace.

**Rotation-caused Collisions:** because rotation is per-player (§4), these only ever occur within a single player's own orbit. Normal rotation (all COs shift one step simultaneously, including into empty slots) never causes a Collision on its own — it's a pure permutation. A rotation-caused Collision only occurs when a card effect anchors a CO in place or moves a CO against the normal direction, causing it to land on a slot another CO is rotating into; the rotating CO is treated as "incoming" for the tiebreak rule above.

**Enforcement note:** Heavenly Bodies has no digital engine to prevent illegal plays. This still applies to other illegal plays that remain possible (e.g., a Direct Effect AE with no legal target, §10) — those don't resolve, and the card is returned to hand as if never played. `[LOCKED]`

**Ability activation limits:** unless a card states otherwise, an **Active** ability may be activated **once per turn per source.** `[LOCKED]` **Passive abilities are exempt** — they are always-on and not a "turn action," so the limit does not apply to them.

## 6. Out of Orbit Zone

A **persistent, shared, open-access pool.** `[LOCKED]` COs knocked out of orbit go here and remain until reclaimed or otherwise removed — they are not auto-discarded at end of turn. Any player may reclaim any CO from this zone into their own orbit (subject to normal placement rules), regardless of original owner. Attached Augmentations are discarded when a CO enters this zone. Note: COs removed via the Size-0 rule (§3) go directly to discard, bypassing this zone. **No size limit** — the zone can grow unbounded over the course of a game. `[LOCKED]`

**Ownership on reclaim:** when a CO is reclaimed by a player other than its original owner, **ownership fully transfers** to the reclaiming player going forward. `[LOCKED]`

**Same-turn bounce-back:** a player may immediately reclaim their own just-knocked-out CO in the same turn, with no special restriction beyond it costing one of their normal actions (a play, or a free ability use per §5). `[LOCKED]` There is likewise no limit on how many times a single physical CO may move between orbit and Out of Orbit over a game — only the normal legal-move constraints apply each time. `[LOCKED]`

**Reclaiming a CO from this zone is not a generic default action.** `[LOCKED]` It only happens via:
- **A CO/Star ability already in play** — does not consume one of the turn's 2 plays (consistent with the once-per-turn-per-source activation rule).
- **An AE card** — counts as 1 of the turn's 2 plays, like any other AE.

**Reclaim destination legality:** a reclaim follows the same placement rules as any other CO placement (§5). `[LOCKED]` It is legal into an empty slot, or into an occupied slot (triggering a Collision, resolved the same as any other). A reclaimed CO must satisfy any placement restriction printed on its own card, exactly as if it were being played fresh from hand. `[LOCKED]` **Since placement is always legal (§5), a reclaim can no longer fail for lack of a destination** — this supersedes the earlier rule that a reclaim with no legal target couldn't be played.

## 7. Turn Structure

Four phases, in order: `[LOCKED]`

1. **Start of Turn:** "start of turn" triggers resolve.
2. **Rotation Phase:** active player's own COs rotate one step (per §4); collisions resolve.
3. **Play Phase:** play up to **2 cards** (per §8) from hand, in any order (add a CO to orbit, or play an AE).
4. **End of Turn:** end-of-turn triggers resolve; **Critical Mass is checked/announced here**; hand economy step happens here (see §8).

## 8. Hand Economy (Draw / Discard / Hand Size / Cards-Played-Per-Turn)

`[PROVISIONAL — locked pending playtest validation, see Audit Tier 0 #8]`

- **Starting hand:** 5 cards.
- **Draw:** 2 cards at Start of Turn.
- **Play:** up to 2 cards per turn (unchanged from original draft).
- **Net economy:** symmetric (draw 2, play up to 2) — hand size self-stabilizes regardless of how aggressively a player plays, rather than trending toward zero. Chosen over an asymmetric draw-1/play-2 pattern, which was modeled and found to drain a hand to 0–1 cards by roughly turn 5–6.
- **Optional End of Turn swap (discard 1, draw 1):** `[OPEN — deferred]` Not yet confirmed as a rule; may not be needed given draw 2/play 2 already provides income. Revisit if playtesting shows a need for a "fix a dead card" tool.
- **Max hand size:** 7 — a hand may **temporarily exceed 7** during a player's turn (especially right after drawing 2). The cap is only enforced at **End of Turn**: discard down to 7 if still over. `[LOCKED]`
- **Deck depletion safety net:** when the shared draw deck is empty, shuffle the discard pile to form a new deck. `[LOCKED]` This decouples sustainability from the eventual total card count (a Tier 3 content decision), since the game cannot stall from an empty deck regardless of final deck size.
- **Flat across player counts:** all hand economy numbers above (starting hand, draw, play, cap) are identical regardless of player count (2p through 6p) — no scaling by table size. `[LOCKED]` Considered and rejected: scaling starting hand/cap up with player count to compensate for fewer personal turns in bigger games — this depended on an assumed fixed game-duration target that the designer clarified is not a real constraint; genre precedent (Bang!, Fluxx, Exploding Kittens) also keeps personal turn economy flat and scales deck composition or thresholds instead, if anything.

## 9. Interrupts & the Stack

**No instant-speed play from hand.** `[LOCKED]` Players cannot play AEs (or any card) on another player's turn. Only automatic triggered/passive abilities already in play may respond to each other; when multiple such triggers fire simultaneously, they resolve via a **LIFO stack** (last triggered resolves first).

## 10. Card Types

- **Star Cards:** HP 5–9 (lower HP paired with stronger abilities by design intent). Chosen at setup, not part of the shuffled draw deck. **HP curve: 1/2/3/3/3 (9/8/7/6/5), 12 total** — deliberately asymmetric: rare at the top (safe/tanky), increasingly common toward the bottom (fragile/powerful). `[LOCKED — supersedes the earlier symmetric 1/3/4/3/1 (10–6) curve]` Mean HP dropped from 8.0 to 6.58 (~18% reduction), a deliberate lever to speed up the Star Destruction path relative to Critical Mass. The shape change (rare-high vs. the old rare-both-extremes) is intentional — it also skews the *average* table toward faster, more aggressive picks, reinforcing the same goal. **12-Star roster is the base-set scope**, kept deliberately fixed rather than expanded now — roster growth is a planned lever for future expansion packs, not the initial print run. `[LOCKED]` **No duplicate Stars per table** — each Star is unique within a single game. `[LOCKED]` **Star selection method: the rulebook offers two variants, and the table picks which to use.** `[LOCKED]` (1) *Full-visibility draft:* all 12 Stars are laid out, players pick freely in turn order. (2) *Random-deal-then-choose (Bang!-style):* deal 2 random Stars to each player, they pick 1 and the other returns to the pool. **Remaining tuning lever if playtesting shows the Star Destruction path still drags relative to Critical Mass:** increase AE damage output and/or the proportion of damage-dealing cards in the 96-card pool.
- **Celestial Objects (COs):** Size + Stability, may have Active or Passive abilities, may have orbital placement restrictions. **"Enters orbit" triggers:** if a CO's printed text includes an enters-orbit trigger, it fires whenever that CO is placed into orbit for any reason — a fresh play from hand, a placement that wins its Collision, or a reclaim from the Out of Orbit zone (even one that immediately loses its own Collision — see §5). `[LOCKED]`
- **Astronomical Events (AEs):** Two subtypes — **Augmentations** (attach to a CO in orbit, discarded whenever the attached CO leaves orbit for any reason — knockout via Collision, discard, or otherwise — an Augmentation never "follows" a CO between zones) and **Direct Effects** (resolve once, then discard). **No limit on stacking:** multiple different Augmentations may be attached to the same CO simultaneously. `[LOCKED]` A Direct Effect AE with **no legal target on the board is illegal to play** — it cannot be attempted, and does not resolve or consume a play. `[LOCKED]` **Cost philosophy:** most AEs are free or carry only soft prerequisites (targeting/board-state conditions); hard costs (self-damage, discarding, sacrificing a CO) are reserved for the strongest effects only. `[LOCKED]`

**Default multiplayer targeting:** unless a card states otherwise, "target an opponent" is always the **acting player's choice** of opponent. `[LOCKED]`

## 11. Deck Structure

One shared, shuffled deck of COs + AEs (Star cards are a separate selection pool, not shuffled in). **Print target: 108 total cards — 12 Stars + 96 CO/AE draw pile.** `[LOCKED]` Benchmarked against comparable shared-deck genre print runs (108 matches Sushi Go, among others) and print-industry base-12 sheet economics. 12 Stars = exactly 2x the 6-player max, giving real setup choice without an oversized initial roster; 96 sits within the earlier ~90–100 provisional target for the draw pile and is itself print-clean (8 sheets of 12). **Within the 96: 36 COs, 60 AEs — all unique, zero duplicate copies.** `[LOCKED]` AE-heavy split chosen because the CO-per-turn cap (§5) already throttles CO usage regardless of supply, while AE volume is the primary lever for tuning Star Destruction pacing against Critical Mass. No duplicates: reshuffle-on-empty (§9) already solves sustainability regardless of copy count, so duplicates would only trade away unique variety for no real benefit — and keeping the base set fully unique avoids future friction with Phase 2's constructed-deck copy-limit system, which can introduce its own rarity/copy structure independently rather than inheriting one from the base set. The locked 75/25 core-to-unique CO split lands cleanly on 27 core + 9 unique designs at 36 total.

*This section of the ruleset will grow as Audit items are resolved. Sections marked `[OPEN]` are placeholders, not defaults — do not build card text against them until they're locked.*

---
---

# PART 2 — STAR ROSTER (WORKING LIST)

**Status:** IN PROGRESS — 12 of 12 slots filled, names not yet assigned. This is the current working list, not final card text — abilities may still be adjusted for balance/wording as playtesting and further review continue.

**HP curve:** 1/2/3/3/3 across 9/8/7/6/5 — deliberately asymmetric, rare at the top (safe/tanky), common at the bottom (fragile/powerful). Mean HP 6.58. (Shifted down from an original 6–10 symmetric bell after modeling pacing against Critical Mass.)

## HP 9 *(1 card — rarest, safest tier)*

**Archetype:** Simple
**Ability:** Once per turn, you may discard a card to draw a different card.

## HP 8 *(2 cards)*

**Archetype:** Augmentation-stacking
**Ability:** Once per turn, you may move an Augmentation from one of your COs to another.

**Archetype:** Out of Orbit
**Ability:** Whenever one of your COs is knocked into the Out of Orbit zone, you may draw a card.
*Note: synergizes with the deliberate-sacrifice design space (Rules v2 §5) — a player can intentionally lose a Collision to trigger this.*

## HP 7 *(3 cards)*

**Archetype:** Critical Mass
**Ability:** While your total Size in orbit is 10 or greater, your COs gain +1 Stability.

**Archetype:** Aggression
**Ability:** Once per turn, if you have 3 or more COs in orbit, you may deal 1 damage to an opponent's Star.

**Archetype:** Aggression
**Ability:** Once per turn, when an opponent's effect knocks one of your COs out of orbit, you may deal 1 damage to that opponent's Star.

## HP 6 *(3 cards)*

**Archetype:** Aggression
**Ability:** Once per turn, if this Star took damage since your last turn, you may deal 1 damage to an opponent's Star.

**Archetype:** Augmentation-stacking
**Ability:** While a CO in your orbit has 2 or more Augmentations, it also has +1 Size.

**Archetype:** Out of Orbit
**Ability:** Once per turn, you may reclaim a CO from the Out of Orbit zone into your orbit, even if a CO has already entered your orbit this turn.
*Confirmed: this is the card's explicit override of the CO-per-turn cap (Rules v2 §5) — its actual archetype identity.*

## HP 5 *(3 cards — most common tier, highest power ceiling)*

**Archetype:** Critical Mass
**Ability:** Your Critical Mass threshold is 13 instead of 15.

**Archetype:** Out of Orbit
**Ability:** Whenever you reclaim a CO, it deals 1 damage to an opponent's Star.

**Archetype:** Denial/control
**Ability:** Once per turn, when one of your COs is knocked out of orbit for any reason, you may deal 1 damage to an opponent's Star.

---

## Archetype tally (12 cards)

| Archetype | Count |
|---|---|
| Aggression | 3 |
| Out of Orbit | 3 |
| Critical Mass | 2 |
| Augmentation-stacking | 2 |
| Simple | 1 |
| Denial/control | 1 |

*Note: original plan targeted 2 cards per archetype across 6 categories. Current list is Aggression/Out-of-Orbit-heavy (3 each) and Denial/control-light (1, down from a planned 2) — worth a deliberate look once ability text is finalized, though not necessarily a problem on its own.*

## Open items before this list is truly final

1. **Archetype balance** — Denial/control is underrepresented (1 card) relative to the original 2-per-archetype plan; Aggression and Out-of-Orbit are both over.
2. **No names yet** — cosmetic, but needed before this becomes print-ready content.
3. **Ability power-level pass** — none of these 12 have been checked against actual playtesting; all HP/ability pairings remain provisional per Rules v2 §10.

---
---

# PART 3 — DESIGN AUDIT & PROJECT LOG

**This document is the record of *how* Rules v2 got there:** the reasoning, the alternatives considered, and what's still open. If you are picking up this project in a new session (any account, any assistant), read this part first — it's written to be a self-contained briefing, not just a task list.

**Working relationship:** Claude acts as the project's recorder. Rules v2 only receives fully-locked decisions. When a new decision touches an unresolved or ambiguous area, Claude checks with the designer before updating either document rather than resolving it unilaterally.

## Part A — Project Narrative (read this first if you're new to the project)

### What Heavenly Bodies is

A tabletop strategy card game where players represent celestial forces, each anchored by a **Star** card, building a system of orbiting Celestial Objects (COs), while using Astronomical Events (AEs) to attack, defend, and manipulate the board. Two win conditions are designed to be equally viable: destroy your opponent's Star, or build up 15+ total Size in orbit and hold it (Critical Mass). The game supports both 1v1 and multiplayer free-for-all.

The mechanical hook that makes this design distinctive: **COs rotate around the orbit every turn.** Board position isn't static — it's a clock. This turns "where do I place this card" into an ongoing tactical puzzle rather than a one-time decision, and it's the thing most worth protecting as the design evolves.

### How the project got here

The design originated as a single, large brainstorming document — official-sounding "Official Rules" sections interleaved with open-ended design exploration (card ability brainstorms, two draft Planet rosters, percentage-based content guidelines for card design). It was never fully reconciled into one consistent spec; several mechanics were drafted more than once, with the later drafts sometimes contradicting the earlier ones (e.g., three different versions of the turn structure exist in the original document).

On **Session 1**, Claude read the full original document and produced a full audit (this document), identifying every internal contradiction, gap, and open design question, sorted into priority tiers. On the same session, four early rules questions were resolved by the designer before the full audit was requested:

- The game supports **both 1v1 and multiplayer free-for-all**, not just one mode.
- Orbital collisions: the CO with **lower Stability is knocked out**; ties broken by **smaller Size**.
- Size and Stability have a **hard floor of 0** — no effect can push them negative — and a CO is knocked out at **exactly 0 Stability**.
- The hand economy (how/whether players draw each turn) was explicitly **deferred** — flagged as needing dedicated design attention rather than being decided quickly.

Following the full audit, the designer requested a formal two-document system going forward: **Rules v2** (canonical) and this **Audit & Project Log** (paper trail), with Claude as recorder. This section of the document — Part A — exists specifically so that *vision and journey*, not just action items, survive into any future session.

### Design philosophy notes worth preserving

A few intentional choices worth remembering, since they should inform how open questions below eventually get resolved:

- **No mana/resource-cost system.** The only throttle on power is cards-played-per-turn plus per-card built-in costs. This is a deliberate minimalist stance, not an oversight — it should be treated as a pillar to protect unless explicitly reconsidered.
- **Dual win conditions must stay genuinely co-equal.** Not just thematically — the designer has emphasized this should hold up mathematically too (turn-count-to-win should be comparable for both paths).
- **The original document's card lists (Planet rosters, CO samples) are suggestions only**, explicitly not canon, per the designer's early instruction. They're useful as tone/flavor reference but shouldn't be treated as locked content.
- **Game duration targets (the source's "10–20 min for 2p, 25–40 min for 6p" figures) are flexible, not hard constraints.** Designer explicitly corrected an early Claude analysis that treated these as fixed — worth remembering, since these numbers still appear in the source material and could mislead future reasoning if taken as binding.

### Long-Term Product Vision & Roadmap

**Phase 1 (current, in development):** Heavenly Bodies ships as a standalone boxed game — a single shared draw pile and discard pile, all players drawing from and contributing to the same communal deck, in the tradition of shared-deck party/family card games.

**Phase 2 (future vision, not yet in active design):** Individual player decks, purchasable/expandable via expansion sets or booster packs — a constructed-deck model, following the *same core rules* as Phase 1. A player would build and bring their own deck rather than share one communal pile with the table.

**Design implication flagged for later (not an open Tier item, a standing note for whenever content design begins):** shared-deck and individual-constructed-deck are two different balance problems, not the same rules with a different deck source. In shared-deck play, luck evens out across a game and no one can guarantee access to specific cards or combos; in constructed play, a player can deliberately stack synergies or run multiple copies of their strongest cards, which can break balance tuned only for random shared access. This doesn't block Phase 1 work at all, but two things should be decided **before real card content design begins**, with Phase 2 in mind:
1. **Copy limits** per deck (irrelevant to Phase 1, critical to Phase 2).
2. Whether cards are designed conservatively enough to survive both environments, or whether a later constructed-format balance pass (bans/restrictions) is simply accepted as normal, the way most TCGs handle this.

**Good news validated by the rules work so far:** the core mechanics (Collision resolution, rotation, both win conditions, draw/play economy) don't care whether the deck is shared or personal — only the deck-sourcing layer would need to change for Phase 2 (shared pile → personal pile; the reshuffle-on-empty rule would become per-player instead of table-wide). The core game does not need a redesign to eventually support Phase 2, only an added mode.

## Part B — Status Board

A quick-reference table of every open item from the original audit. Full detail for each is in Part C below.

| # | Item | Tier | Status | Resolution (if any) |
|---|------|------|--------|----------------------|
| 1 | Star vs. Planet naming | 0 | RESOLVED | **Star** is the official term; "Planet" freed up for CO/flavor use (Rules v2 §1) |
| 2 | Orbital position naming (seasons/cardinal/numbered) | 0 | RESOLVED | Cardinal (N/E/S/W) is mechanical; seasons are visual flavor only (Rules v2 §4) |
| 3 | Critical Mass timing window (end vs. beginning of next turn) | 0 | RESOLVED | End of achiever's next turn; dips below 15 cancel the countdown (Rules v2 §2) |
| 4 | Rotation scope (whose COs rotate on whose turn) | 0 | RESOLVED | Per-player: only active player's COs rotate, only on their turn; card effects can override (Rules v2 §4) |
| 5 | Out of Orbit zone: persistent pool vs. one-turn buffer | 0 | RESOLVED | Persistent shared pool (Rules v2 §5) |
| 6 | Out of Orbit zone: open-access vs. owner-restricted | 0 | RESOLVED | Open-access — any player may reclaim any CO (Rules v2 §5) |
| 7 | Turn structure (reconcile 3 drafts) | 0 | RESOLVED | 4-phase structure locked: Start/Rotation/Play/End (Rules v2 §6) |
| 8 | Hand economy (draw/discard/hand size) | 0 | PROVISIONAL | Draw 2/play 2 (symmetric), hand cap 7, reshuffle-on-empty locked, confirmed flat across all player counts (Rules v2 §8) |
| 9 | Stack/priority system for responses | 0 | RESOLVED | No instant-speed play from hand; only auto-triggers use LIFO stack (Rules v2 §9) |
| 10 | Deck structure (shared deck, explicit statement) | 0 | PARTIALLY LOCKED | Shared deck confirmed; count/copies open (see #30) |
| 11 | CO stat-bucket overlap bug | 1 | RESOLVED | Fixed to non-overlapping bounds: ≤4/5–6/≥7 (15%/70%/15%) |
| 12 | Critical Mass reachability math | 1 | OPEN | — |
| 13 | HP-race pacing math | 1 | OPEN | — |
| 14 | Resource/cost curve — protect as pillar? | 1 | NOTED (see Part A) | Treated as intentional; revisit only if power creep forces it |
| 15 | AE cost philosophy contradiction | 1 | RESOLVED | Mostly free/soft-prerequisite; hard costs reserved for strongest effects (Rules v2 §9) |
| 16 | Default multiplayer targeting rule | 1 | RESOLVED | Acting player's choice, always (Rules v2 §9) |
| 17 | Elimination handling in multiplayer | 1 | RESOLVED | Board fully removed to discard; seat skipped in turn order (Rules v2 §2) |
| 18 | Kingmaker/dogpile risk on Critical Mass in FFA | 1 | NOTED | Treated as intentional tension pending playtest feedback |
| 19 | Ability activation limits (once per turn?) | 1 | RESOLVED | Once per turn per source, default (Rules v2 §5) |
| 20 | Simultaneous multiplayer collision order | 1 | RESOLVED (moot) | Per-player orbit/rotation means no cross-player collisions exist |
| 21 | Two competing Planet rosters | 2 | OPEN (low urgency — lists are non-canonical) | — |
| 22 | Orphaned name fragments in Planet list | 2 | OPEN (low urgency) | — |
| 23 | Copy-paste errors in sample CO abilities | 2 | OPEN (low urgency) | — |
| 24 | HP distribution target table not yet audited | 2 | LOCKED | Curve: 1/2/3/3/3 (9-5 HP), asymmetric rare-high; range shifted from 6-10 to 5-9 (Rules v2 §10) |
| 25 | "Secondary orbit" mechanic unintegrated | 2 | OPEN | — |
| 26 | Card-state/zone terminology glossary | 2 | OPEN | — |
| 27 | No sample AE cards exist yet | 2 | OPEN | — |
| 28 | Position-restriction percentages need naming resolved first | 2 | BLOCKED on #2 | — |
| 29 | Card template/visual layout | 3 | OPEN | — |
| 30 | Print-run/card-count targets | 3 | LOCKED | 108 total: 12 Stars + 96 CO/AE (36 CO / 60 AE, all unique, no duplicates) (Rules v2 §11) |
| 31 | Rulebook teaching pass | 3 | OPEN | — |
| 32 | Playtesting plan | 4 | IN PROGRESS | Mock 1v1 playtest run session 1; surfaced items 33–38 below |
| 33 | Overtake: playing a CO onto an occupied position | 0 | SUPERSEDED | See item 68 — unified into the Collision system; placement is now always legal (Rules v2 §5) |
| 34 | Reclaiming a CO from Out of Orbit as an action | 0 | RESOLVED | Not a default action; via ability (free) or AE card (counts as a play) (Rules v2 §6) |
| 35 | Star Destruction win-check timing | 0 | RESOLVED | Checked immediately on HP hitting 0, not deferred to End of Turn (Rules v2 §2) |
| 36 | Size-0 CO handling | 1 | RESOLVED | Immediately removed from orbit and discarded (bypasses Out of Orbit) (Rules v2 §3) |
| 37 | Unplayable CO when orbit full, no legal Overtake | 1 | SUPERSEDED | See item 68 — no CO is ever unplayable due to a full orbit under the unified Collision system (Rules v2 §5) |
| 38 | Augmentation AEs as early-game dead draws | 2 | NOTED | Design goal: AE effects that place/interact with COs in a player's orbit could double as variation + inter-player interaction; remember for AE content design |
| 39 | Reclaim: no legal destination slot | 0 | SUPERSEDED | See item 68 — reclaim can no longer fail for lack of a destination (Rules v2 §6) |
| 40 | Seat elimination — confirm no disruption to other players' Critical Mass "next turn" anchors | 1 | RESOLVED | Confirmed as-is; if a player is eliminated mid-countdown against them, that's simply the outcome, no special protection (Rules v2 §2) |
| 41 | Dogpile dynamics in FFA | 1 | VALIDATED | Confirmed working as intended via mock playtest — no rule change needed |
| 42 | Effective (current) vs. printed base stats for all thresholds | 0 | RESOLVED | Always effective/current stats; permanent reductions knock out immediately at 0, temporary effects trigger knockout the moment they cause 0 (Rules v2 §3) |
| 43 | Passive abilities vs. the once-per-turn-per-source activation limit | 1 | RESOLVED | Passives exempt — always-on, not a turn action (Rules v2 §5) |
| 44 | Hand cap of 7 — can it be temporarily exceeded mid-turn? | 0 | RESOLVED | Yes, mid-turn overflow allowed; enforced only at End of Turn (Rules v2 §8) |
| 45 | Order of ops: discard-swap vs. forced hand-cap discard at End of Turn | 0 | DEFERRED | The discard-1/draw-1 swap itself is deferred — not confirmed as a rule; question moot until it's decided |
| 46 | Self-inflicted Star Destruction | 0 | RESOLVED | Treated identically to opponent-inflicted — ends the game the same way (Rules v2 §2) |
| 47 | Direct Effect AE with no legal target | 1 | RESOLVED | Illegal to play, not a fizzle — same treatment as illegal Overtake (Rules v2 §10) |
| 48 | Overtaken CO's Augmentation discard | 0 | RESOLVED | Confirmed and generalized: Augmentations never follow a CO between zones, for any exit reason (Rules v2 §10) |
| 49 | Reclaimed CO satisfying placement restrictions | 0 | RESOLVED | Must satisfy printed restrictions exactly as a fresh hand-play (Rules v2 §6) |
| 50 | Reclaimed/newly-placed CO triggering "enters orbit" effects | 0 | RESOLVED | Yes, if printed on the card — applies to fresh play, Overtake, or reclaim alike (Rules v2 §10) |
| 51 | Rotation collision behavior on partially-filled orbits | 0 | RESOLVED | Normal simultaneous rotation never self-collides (pure permutation); collision only if a card anchors/reverses a CO (Rules v2 §5) |
| 52 | Same-turn bounce-back reclaim of your own knocked-out CO | 0 | RESOLVED | Fully allowed, no special restriction beyond costing one action (Rules v2 §6) |
| 53 | Simultaneous Critical Mass across two players in the same round | 1 | RESOLVED | No tie-break rule needed — turns are sequential, first check in turn order resolves and ends the game (Rules v2 §2) |
| 54 | Critical Mass checked mid-phase vs. only at boundaries | 0 | RESOLVED (reconfirmed) | Checked only at End of Turn, never mid-phase (Rules v2 §2) |
| 55 | Illegal Overtake — real rules gap or UX/self-enforcement note | 0 | RESOLVED | No digital enforcement exists; illegal plays are self-enforced by players and simply don't resolve (Rules v2 §5) |
| 56 | Targeting a player mid-Critical-Mass-countdown | 1 | RESOLVED | No restriction — any Star may be targeted unless a card states otherwise (Rules v2 §2) |
| 57 | Out of Orbit zone size limit | 0 | RESOLVED | No limit — can grow unbounded over a game (Rules v2 §6) |
| 58 | CO ownership after being reclaimed by another player | 0 | RESOLVED | Ownership fully transfers to the reclaiming player (Rules v2 §6) |
| 59 | Restrictions on repeated orbit/Out-of-Orbit bounces | 1 | RESOLVED | None — as many times as legal moves allow (Rules v2 §6) |
| 60 | Critical Mass counts only in-orbit Size, not Out of Orbit | 1 | RESOLVED | Explicit line added — in-orbit Size only, applied directly as a wording fix (Rules v2 §2) |
| 61 | Same-turn Critical Mass re-trigger deadline | 0 | RESOLVED | Always "achiever's next turn," never the current turn, regardless of re-trigger timing (Rules v2 §2) |
| 62 | Augmentation stacking on one CO | 0 | RESOLVED | No limit — multiple Augmentations may stack on the same CO (Rules v2 §10) |
| 63 | Eliminated player's Out of Orbit history — cleared or stays? | 0 | RESOLVED | Stays in the shared pool — only orbit + hand are removed on elimination (Rules v2 §2) |
| 64 | "Whenever ANY CO enters orbit" (table-wide) trigger text | 2 | NOTED | Allowed as a content pattern; treat as high-power, rare — content design guideline, not a rules lock |
| 65 | No-duplicate-Stars-per-table rule | 0 | LOCKED | Each Star is unique within a single game (Rules v2 §10) |
| 66 | Base-set Star roster size vs. Bang!'s 16 characters | 3 | LOCKED | 12 confirmed for base set (proportionally comparable leftover-variety ratio to Bang!); roster growth deferred to future expansion packs (Rules v2 §10) |
| 67 | Star selection method at setup | 0 | LOCKED | Rulebook offers both full-visibility draft and Bang!-style random-deal-then-choose as variants; table picks (Rules v2 §10) |
| 68 | Unify Overtake + rotation-collision into one Collision system | 0 | LOCKED | Single event, any cause; placement always legal; Stability→Size→incoming-wins-ties hierarchy; supersedes items 33, 37, 39 (Rules v2 §5) |
| 69 | CO-per-turn cap (Critical Mass rush-speed risk) | 0 | LOCKED | Max 1 CO enters orbit/turn, any source; stricter than but separate from the 2-plays/turn cap; card-specific exceptions allowed (Rules v2 §5) |

## Part C — Full Detail (original audit, ranked by priority)

### TIER 0 — Structural Blockers

1. **Star vs. Planet naming collision. `RESOLVED`.** The document calls the same core card "Planet" in most sections but "Star" in others. **Decision: "Star" is the official mechanical term.** Reasoning: it makes the orbital geometry make sense (things orbit a star, not another planet), it matches the Win Conditions section's existing language (smaller find-and-replace), it fits the "Heavenly Bodies" title, and it frees "Planet" as an unreserved flavor word for CO names.

2. **Orbital position naming. `RESOLVED`.** Decision: **cardinal directions (N/E/S/W) are mechanical**; seasons remain as visual/flavor dressing only, never in rules text. Numbered slots dropped.

3. **Critical Mass timing. `RESOLVED`.** Decision: hold window is **end of the achieving player's next turn**. Reaching 15 is announced; if still ≥15 at that deadline, win locks in. Dipping below 15 at any point before the deadline cancels the countdown (must re-trigger by reaching 15 again). Gives the table exactly one full round of counterplay.

4. **Rotation scope. `RESOLVED`.** Decision: **per-player rotation** — only the active player's own COs rotate, only on their own turn. Individual cards may override this default. This keeps pacing consistent across 1v1 and multiplayer table sizes and keeps ownership of rotation-triggered decisions unambiguous.

5. **Out of Orbit zone persistence. `RESOLVED`.** Decision: **persistent shared pool** — COs are not auto-discarded at end of turn.

6. **Out of Orbit zone access. `RESOLVED`.** Decision: **open-access** — any player may reclaim any CO from the zone, regardless of original owner.

7. **Turn structure. `RESOLVED`.** Decision: four phases — Start of Turn, Rotation, Play, End of Turn. Critical Mass is checked/announced at End of Turn. Cards-playable-per-turn is not locked here; it's folded into item 8 below.

8. **Hand economy. `PROVISIONAL`.** Two problems separated: (a) deck depletion risk, solved structurally via reshuffle-discard-into-deck when the draw deck empties — decouples sustainability from final card-count, which stays a Tier 3 content decision (item 30); (b) draw/play *ratio*, resolved by comparing genre conventions (MTG/Dominion are resource-gated, not a good comp; Smash Up is the closest structural cousin — no mana curve, card-count-gated plays). Draw-1/play-2 was modeled and found to drain a hand to 0–1 cards by turn 5–6, given no-instant-speed play and mostly-free AE costs removing any reason to hold cards. **Landed on draw 2/play 2 (symmetric)**, starting hand 5, hand cap 7. Marked provisional — first candidate for adjustment once playtesting (Tier 4) is underway.

9. **Stack/priority system. `RESOLVED`.** Decision: **no instant-speed play from hand** — cards can only be played on your own turn. Automatic triggered/passive abilities may still respond to each other and resolve via a LIFO stack when multiple fire simultaneously. Chosen to protect the "teach in 5 minutes" goal against Magic-style priority complexity.

10. **Deck structure/ownership not explicitly stated.** Implied to be one shared communal deck of COs + AEs (Planets chosen separately), but never stated as an explicit rule. *(Status: shared-deck structure has effectively been confirmed via the Rules v2 draft — count/copy targets remain open, tracked as item 30.)*

### TIER 0.5 — Discovered During Mock Playtest (Session 1)

*A placeholder-card 1v1 mock game was run to stress-test the locked rules skeleton (Rotation → Play → End, Overtake, Out of Orbit, Critical Mass). It surfaced several real mechanics that hadn't been specified yet — all resolved in the same session:*

33. **Overtake — playing a CO onto an occupied position. `RESOLVED`.** Distinct from rotation-phase collisions. Legal only if the incoming CO's Stability is strictly greater than the resident's; otherwise the play is illegal outright (not attempted, doesn't consume a play). A legal Overtake counts as 1 of the turn's 2 plays. No voluntary/forced swap exists outside this. *(Note: this entire mechanic was later superseded by item 68's unified Collision system.)*

34. **Reclaiming a CO from Out of Orbit as an action. `RESOLVED`.** Not a default, generic action. Only available via (a) a CO/Star ability already in play — free, doesn't consume a play, once/turn/source — or (b) an AE card, which does consume 1 of the 2 plays.

35. **Star Destruction win-check timing. `RESOLVED`.** Checked immediately the instant a Star's HP hits 0, at any point in the turn — unlike Critical Mass, which is deliberately checked only at End of Turn. The asymmetry is intentional: destruction is a hard, immediate state; Critical Mass is a held state.

36. **Size-0 CO handling. `RESOLVED`.** A CO whose Size drops to 0 is immediately removed from orbit and sent straight to discard — it does not pass through the Out of Orbit zone. Prevents "dead weight" COs sitting in orbit contributing nothing to Critical Mass.

37. **Unplayable CO when orbit is full with no legal Overtake target. `RESOLVED (provisional)`.** The card is simply unplayable that turn. Flagged as provisional — worth revisiting if playtesting shows this feels too punishing. *(Superseded by item 68.)*

38. **Augmentation AEs as early-game dead draws. `NOTED — content design goal, not a rule.`** Augmentations need a CO already in orbit to target, which can make them awkward early draws. Designer's stated goal: AE effects that place or otherwise interact with COs in a player's orbit could serve double duty — creating variation and forcing inter-player interaction. Carry this into AE content design (relates to Tier 2 item 27).

### Mock Multiplayer & Follow-up Playtest (Session 1, continued)

*Further mock games (1v1 and 3-player FFA) stress-tested Overtake/Reclaim interactions, buffed/debuffed stats, passive abilities, and hand-cap timing. 22 questions were raised; the designer resolved the first 6 in this pass.*

39. **Reclaim: no legal destination slot. `RESOLVED`.** Follows the same placement legality as any CO placement (Rules v2 §5) — legal into an empty slot, or as an Overtake if the target has lower effective Stability. If neither applies, the reclaim **cannot be played/activated at all** — fizzles at the attempt stage, same treatment as an illegal Overtake. *(Superseded by item 68.)*

40. **Seat elimination and Critical Mass timing. `RESOLVED`.** Confirmed as-is: each player's Critical Mass deadline is anchored to their own next turn, not a shared counter. If a player is eliminated via Star Destruction while another player has an active countdown running against them, that's simply the outcome — no special protection exists for a countdown in progress.

41. **Dogpile dynamics in FFA. `VALIDATED`.** Mock 3-player game showed two different players independently found different valid counters (HP-race vs. Size-denial) against the same Critical-Mass-leading player. No rule change needed — this is the intended tension working as designed.

42. **Effective vs. printed base stats. `RESOLVED`.** All thresholds (Overtake comparisons, Critical Mass totals, Stability-0/Size-0 knockout) always use **current effective stats** (printed value + active modifiers), never printed base values alone. Permanent/passive stat reductions trigger knockout the instant the effective value hits 0. Temporary effects likewise trigger knockout at the moment they cause the value to hit 0 — this is a one-time check at the moment of application, not a continuously re-evaluated state.

43. **Passive abilities and the activation limit. `RESOLVED`.** The "once per turn per source" activation limit applies only to **Active** abilities. Passive abilities are always-on and don't count as a turn action, so they're exempt entirely.

44. **Hand cap of 7 — mid-turn overflow. `RESOLVED`.** A hand may temporarily exceed 7 during a player's own turn (expected, since players draw 2 at Start of Turn before playing anything). The cap is enforced only at End of Turn — discard down to 7 if still over at that point.

45. **Order of operations: discard-swap vs. forced hand-cap discard. `DEFERRED`.** Moot for now — the underlying discard-1/draw-1 swap rule itself was deferred (not confirmed as needed, given draw 2/play 2 already provides income). Revisit both together if the swap rule returns.

46. **Self-inflicted Star Destruction. `RESOLVED`.** Treated identically to opponent-inflicted — a player who drops their own Star to 0 (e.g., via an AE's own cost) loses immediately, same as if an opponent had done it.

47. **Direct Effect AE with no legal target. `RESOLVED`.** Illegal to play, not a wasted/fizzled play — consistent with the illegal-Overtake treatment (attempt is blocked outright, doesn't consume a play).

48. **Overtaken CO's Augmentation discard. `RESOLVED` — generalized.** Confirmed and broadened into a general rule: an Augmentation is discarded whenever its attached CO leaves orbit for *any* reason (rotation-collision knockout, Overtake, discard, etc.) — it never follows the CO between zones.

49. **Reclaimed CO satisfying placement restrictions. `RESOLVED`.** A reclaimed CO must satisfy any placement restriction printed on its own card, exactly as if it were being played fresh from hand.

50. **"Enters orbit" triggers on reclaim. `RESOLVED`.** If a CO's printed text has an enters-orbit trigger, it fires on any placement into orbit — fresh play, Overtake, or reclaim alike.

51. **Rotation collision on partially-filled orbits. `RESOLVED`.** Normal simultaneous rotation (all COs shift one step at once, including into empty slots) is a pure permutation and can never self-collide. A rotation-phase collision requires a card effect that anchors a CO in place or reverses its direction, causing it to land on a slot another CO is rotating into.

52. **Same-turn bounce-back reclaim. `RESOLVED`.** Fully allowed — a player may reclaim their own just-knocked-out CO the same turn, with no restriction beyond it costing one of the turn's normal actions.

53. **Simultaneous Critical Mass across two players. `RESOLVED`.** No tie-break rule needed. Both win conditions are checked immediately when true, and turns are strictly sequential — there's never a moment where two players' checks occur at once. Whichever player's check comes first in actual turn order resolves first, and the game ends immediately if they win.

54. **Critical Mass check timing — mid-phase vs. boundary. `RESOLVED (reconfirmed)`.** Checked only at End of Turn — never evaluated mid-phase, even if a triggered ability pushes total Size over 15 earlier in the turn.

55. **Illegal Overtake — rules gap or self-enforcement note. `RESOLVED`.** Heavenly Bodies has no digital engine; illegal plays (illegal Overtake, targetless Direct Effect AE) are self-enforced by the players at the table — if attempted, they simply don't resolve and the card returns to hand.

56. **Targeting a player mid-Critical-Mass-countdown. `RESOLVED`.** No restriction — an AE may target any Star, including one currently mid-countdown, unless its own text says otherwise.

57. **Out of Orbit zone size limit. `RESOLVED`.** None — the zone can grow unbounded over the course of a game.

58. **CO ownership after reclaim by another player. `RESOLVED`.** Ownership fully transfers to the reclaiming player going forward.

59. **Restrictions on repeated orbit/Out-of-Orbit bounces. `RESOLVED`.** None — a CO may move between the two zones as many times as legal moves allow, no cap.

60. **Critical Mass counting only in-orbit Size. `RESOLVED`.** Made explicit in Rules v2 as a direct wording fix (analogous to the stat-bucket math correction, item 11) rather than a live decision — COs in the Out of Orbit zone never count toward the 15 threshold.

**Status: 22 of 22 list items now closed** (resolved, deferred, or validated).

### 4-Player FFA Mock Simulation (Session 1, continued)

61. **Same-turn Critical Mass re-trigger deadline. `RESOLVED`.** Surfaced when a 4-player FFA mock game had a player's countdown cancelled and re-triggered within the same turn that was the original deadline. Claude recommended, and designer confirmed: the deadline is **always** "end of the achiever's next turn," never the current turn's own End of Turn — even if the re-trigger happens on what would have been the deadline turn itself. Preserves the one-full-round counterplay guarantee regardless of re-trigger timing.

### Further Mock Scenarios (2p Augmentation stacking, 6p FFA)

62. **Augmentation stacking on one CO. `RESOLVED`.** No limit — multiple different Augmentations may be attached to the same CO simultaneously. Chosen over a "1 per CO" cap to avoid an exception with no demonstrated problem behind it, and to leave room for Augmentation-heavy strategies as a real archetype.

63. **Eliminated player's Out of Orbit history. `RESOLVED`.** Stays in the shared pool, unaffected by the elimination. Only the eliminated player's **orbit and hand** are removed to discard (per the existing rule) — anything they'd already sent to the Out of Orbit zone is ownerless/shared by rule and simply remains in play, reclaimable by anyone, for the rest of the game.

64. **"Whenever any CO enters orbit" (table-wide) trigger text. `NOTED — content design guideline, not a rules lock.`** Designer confirmed this pattern is allowed, but should generally be treated as strong/powerful design space once real card balance work begins — filed for later content design rather than resolved as a Rules v2 entry now.

65. **No-duplicate-Stars-per-table rule. `LOCKED`.** Surfaced while discussing whether the HP-tier card counts (bell curve) actually matter mechanically. Confirmed: each Star is unique within a single game — this is what makes the bell curve's rarity-at-extremes meaningful (caps how many players at one table can simultaneously play the riskiest HP tiers), rather than purely cosmetic.

66. **Base-set Star roster size vs. Bang!'s 16 characters. `LOCKED`.** Designer noted Bang! has more characters than our 12. Claude compared leftover-variety ratios at max table size: Bang! (16 characters, max 7 players) leaves ~56% unused; Heavenly Bodies (12 Stars, max 6 players) leaves exactly 50% unused — proportionally comparable, not undersized. Also noted Bang!'s asymmetry softens further via its own expansions (Dodge City, etc.), mapping directly onto Heavenly Bodies' own Phase 2 roadmap (expansion packs). Designer confirmed: keep 12 for the base set, treat roster growth as a future-expansion lever rather than expanding the initial 108-card print run.

67. **Star selection method at setup. `LOCKED`.** Two variants exist in comparable games: full-visibility draft (all Stars visible, pick freely) vs. Bang!-style random-deal-then-choose (hidden information, limited choice). Designer chose to offer **both as official rulebook variants**, letting the table pick which fits their group.

68. **Unify Overtake + rotation-collision into one Collision system. `LOCKED` — supersedes items 33, 37, 39.** Surfaced while reworking a card's text, which needed to reference the placement-onto-occupied-slot mechanic without using internal rules jargon. Designer clarified the intended model: a single "Collision" event, triggered by rotation *or* placement, resolved the same way regardless of cause (Stability main, Size as tiebreak, AE/CO abilities as further modifiers). Claude asked what value allowing always-legal placement (vs. the old illegal-if-insufficient-Stability block) would add; designer confirmed unifying anyway. Real consequences of the change: placement is now always legal (subject only to a card's own restriction); a placed CO that loses its Collision still triggers "enters orbit" before being knocked out (enabling deliberate sacrifice plays into knockout-triggered abilities); the "Unplayable CO" rule (item 37) and "reclaim with no legal destination" rule (item 39) both became obsolete, since a destination is now always available. A full-tie (Stability and Size both equal) resolves in favor of the incoming/moving CO — this was actually the original source material's own answer, rediscovered during the deck-size research digression and formally locked here. *(Rules v2 §5, with cascading renumbering of §§6–12 → §§6–11 documented across both files)*

69. **CO-per-turn cap. `LOCKED`.** Surfaced while discussing the shifted HP curve's effect on pacing — designer asked directly whether Critical Mass could be rushed via placing multiple COs per turn. Claude modeled it: with the existing 2-plays/turn rule allowing 2 COs/turn, an orbit could fill completely by a player's second turn, making Critical Mass reachable turn 2–3 — far faster than a realistic Star Destruction race. Designer proposed a 1-CO/turn cap; first draft (separate 1-placement + 1-reclaim caps, up to 2/turn total) was found exploitable via deliberate self-sacrifice-then-reclaim loops once the Out of Orbit zone has any contents, which happens early regardless of intent. Resolved instead as a **strict baseline of 1 CO entering orbit per turn from any source**, with specific cards explicitly allowed to override it — reframing the override as the Out-of-Orbit archetype's actual identity (beating the normal throttle) rather than diluting a universal action. Modeled turns-to-win with the cap in place lands around turn 6–8, much closer to parity with a Star Destruction race.

11. **CO stat-distribution buckets — bug fixed.** Original "= 5 or 6" (70%) / "< 6" (15%) / "> 6" (15%) overlapped at sum=5. **Corrected, non-overlapping bounds:** Size+Stability **≤4** (15%) / **5–6** (70%) / **≥7** (15%), covering the full possible range of 2–10. `RESOLVED` — this is a definitional fix, not a design call, so applied directly rather than raised as a question. **Exact allocation, final version.** Iterated four times: (1) initial grid; (2) corrected for a bucket-total drift found mid-process; (3) skewed toward higher Size/lower Stability per the "dynamic, not static" direction, but over-corrected — Size 1 had zero designs at Stability 1–3; (4) fix attempt softened the skew to restore coverage, which unintentionally weakened it (Size avg 3.14→3.06, Stability avg 2.42→2.50) — designer flagged this regression and asked for a redesign that kept both. **True final version**: the ≤4 bucket (only 5 cards over 6 cells) has no slack to both cover every cell and skew, so it was set to a coverage-first floor (1 each, except the single (Size 1, Stability 1) zero); the recovered skew was pushed entirely into the 5–6 bucket instead (25 cards over 9 cells has real slack), which more than compensated. **Final marginals: Size average 3.36, Stability average 2.19** — stronger than the original skew attempt, not weaker, while keeping full coverage. Note: Size 4/Stability 1 is a concentrated peak at 6 of 36 designs (~17%) — a real design choice, not an accident, worth keeping in mind during actual card drafting. Full grid (Stability rows, Size 1–5 columns): Stability=1 → [0,1,1,6,5]; Stability=2 → [1,1,3,3,2]; Stability=3 → [1,2,2,1,1]; Stability=4 → [1,2,1,1,0]; Stability=5 → [1,0,0,0,0].

12. **Critical Mass reachability hasn't been modeled against the actual stat curve.** Max total Size in orbit is 20 (4 × 5); threshold is 15. Needs real math once a card list exists: expected turns-to-15 for an average hand, checked against the stated game-length targets.

13. **HP-race pacing hasn't been modeled either.** Risk that the Critical Mass path is faster than the Star Destruction path, undermining the "co-equal win conditions" goal. Needs the same modeling treatment as #12. **Added insight (Bang! comparison):** the risk compounds on two axes, not one — our HP pool (6–10, pre-revision) is roughly double Bang!'s (3–5), *and* our deck spreads effects across many more categories than Bang!'s combat-dense pool, so Star-damage card density per draw will likely be proportionally lower too. This could make a pure Star Destruction race meaningfully slower than the HP gap alone suggests — which may be fine (it would organically push players toward Critical Mass as the faster path, sharpening the two win conditions' distinct identities) or a real problem (if both paths end up slow). Flagged as a top-priority check for the planned simulation tool once real AE damage-density numbers exist.

14. **No resource/cost curve exists at all.** *(See Part A — currently treated as an intentional pillar. Revisit only if power creep becomes hard to manage by feel alone.)*

15. **AE cost philosophy. `RESOLVED`.** Most AEs are free or carry only soft prerequisites; hard costs reserved for the strongest effects only.

16. **Default multiplayer targeting. `RESOLVED`.** "Target an opponent" defaults to acting player's choice, always.

17. **Elimination handling in multiplayer. `RESOLVED`.** Eliminated player's entire board (orbit + hand) goes to discard; their seat is skipped in turn order.

18. **Kingmaker/dogpile risk on Critical Mass in FFA.** *(Currently treated as likely-intentional table drama — worth a deliberate playtest observation rather than an assumption either way.)*

19. **Ability activation limits. `RESOLVED`.** Once per turn per source, unless a card states otherwise.

20. **Simultaneous multiplayer collision order. `RESOLVED (moot)`.** Because rotation is per-player (item 4), collisions only ever happen within one player's own orbit — there's no cross-player scenario requiring a resolution order.

### TIER 2 — Content Consistency & Cleanup

21. **Two competing, overlapping Planet rosters exist**, sharing names with conflicting stats. Low urgency since neither list is canon yet — flag for whenever a roster is finalized.

22. **Orphaned name fragments** with no stats attached — editorial cleanup once a roster is chosen.

23. **Copy-paste errors in sample CO abilities** — editorial pass needed once sample cards are finalized.

24. **HP distribution target table. `LOCKED`.** Extensive discussion covered: Bang!-style near-binary distributions vs. a symmetric bell, the value of extremes being rare (only meaningful if Stars are unique per table), and the risk that a wide HP range compounds with lower Star-damage card density to slow the Star Destruction path relative to Critical Mass. Initially landed on a 1/3/4/3/1 bell (10–6 HP), then revised further during actual card drafting: designer proposed shifting the whole range down to **5–9**, reasoned through as a genuine tuning-lever pull (mean HP drops from 8.0 to 6.58, ~18% reduction, corrected from an initial miscalculated ~13%) rather than a cosmetic change. The tier shape also changed to **1/2/3/3/3 (9/8/7/6/5)** — deliberately asymmetric, rare-at-the-top instead of rare-at-both-extremes — confirmed intentional, since it also skews the average table toward faster, more aggressive Star picks, reinforcing the same pacing goal from a second angle.

25. **"Secondary orbit" mechanic introduced once, never integrated** with the 4-CO orbit cap, collision rules, or Critical Mass Size counting. Needs full spec or a decision to cut it.

26. **Card-state/zone terminology needs a formal glossary.** "Knocked Out of Orbit" / "Discarded" / "Removed from Game" are used inconsistently — likely three genuinely different states that need a one-page zone diagram.

27. **No sample AE cards exist yet**, despite design guidance (Augmentation/Effect split, damage ratios) already being written. Natural next content gap once core rules lock.

28. **Position-restriction percentages (~20/40/40 split) need a settled naming system first** — blocked on item 2.

### TIER 3 — Production & Presentation

29. **No card template/visual layout discussed yet** — stat iconography, layout per card type.

30. **Print-run/card-count targets. `LOCKED`.** Source material was checked directly and confirmed to give ratios only (75/25 core-to-unique, 30/70 AE type split, etc.) with no absolute deck size anywhere. Claude benchmarked comparable shared-deck, no-resource-curve games and print-industry base-12 sheet economics. Designer set the total print target at **108 cards** (matching genre precedent like Sushi Go, and clean base-12 printing). Split into **12 Stars** (2x the 6-player max, for real setup choice) **+ 96-card CO/AE draw pile** (print-clean at 8 sheets of 12, and consistent with the earlier ~90–100 provisional estimate). **CO/AE split finalized: 36 COs / 60 AEs, AE-heavy.** Reasoning: the CO-per-turn cap (item 69) already throttles CO usage regardless of supply, making CO oversupply a hand-clog risk rather than a benefit; AE volume is the primary tuning lever for Star Destruction pacing (item 13). **No duplicate copies** — all 96 are unique designs. Reasoning: reshuffle-on-empty already solves sustainability independent of copy count, so duplicates would trade unique variety for no real benefit; keeping the base set fully unique also avoids future friction with Phase 2's constructed-deck copy-limit system, which can introduce its own rarity structure independently rather than inheriting one from the base set.

31. **No formal rulebook teaching pass** — a "how to play in 5 minutes" quick-start, separate from full reference rules, once rules converge.

### TIER 4 — Validation

32. **No playtesting has occurred yet** beyond Claude-run mock games in this document. Recommended: a minimal physical/print-and-play test of the core loop (Stars + ~15–20 COs + ~10 AEs) once Tier 0 is locked, before scaling content volume.

**Planned tool, once real card content exists:** a Python simulation engine encoding the full Rules v2 ruleset, run with a handful of heuristic bot archetypes (Size-maximizer, aggressive attacker, balanced/reactive, random-legal-move baseline) across many simulated games. This is the intended way to resolve Tier 1 items #12 (Critical Mass reachability) and #13 (HP-race pacing) with real numbers instead of estimates — turns-to-win by win condition, stall/dominant-strategy detection, etc. Explicitly a complement to human playtesting, not a replacement: it validates the math, not the *feel*.

## Part D — Decision Log

*Chronological record. Every entry should be traceable to a specific exchange with the designer. This is the audit trail Rules v2 points back to.*

**Session 1:**
1. Win condition scope → Both 1v1 and multiplayer free-for-all supported. *(Rules v2 §1, §2)*
2. Orbital collision tiebreaker → Lower Stability knocked out; ties broken by smaller Size. *(Rules v2 §5)*
3. Stability floor → Knockout at exactly 0 Stability; Size/Stability hard-floored at 0, never negative. *(Rules v2 §3)*
4. Hand economy → Explicitly deferred by designer; not yet decided. *(Tracked as open item 8)*
5. Full audit produced and prioritized into tiers 0–4 (this document).
6. Designer requested formal two-document system (Rules v2 + this log), with Claude as recorder, checking in on ambiguous calls rather than resolving unilaterally.
7. **Star vs. Planet naming → "Star" chosen as the official term.** *(Rules v2 §1, §2, §8, §9; Tier 0 item 1 RESOLVED)*
8. **Orbital position naming → Cardinal (N/E/S/W).** Seasons kept as pure visual dressing, not rules text. *(Rules v2 §4; Tier 0 item 2 RESOLVED)*
9. **Rotation scope → Per-player.** Designer confirmed, with the explicit caveat that individual cards may override the default. *(Rules v2 §4; Tier 0 item 4 RESOLVED)*
10. **Turn structure → 4-phase (Start / Rotation / Play / End).** Cards-per-turn folded into item 8. *(Rules v2 §6; Tier 0 item 7 RESOLVED; item 8 scope expanded)*
11. **Interrupts/stack → No instant-speed play from hand.** Only automatic triggers can respond to each other, via LIFO stack. *(Rules v2 §9; Tier 0 item 9 RESOLVED)*
12. **Critical Mass timing → End of achiever's next turn; dips cancel.** *(Rules v2 §2; Tier 0 item 3 RESOLVED)*
13. **Out of Orbit zone → Persistent, shared, open-access pool.** *(Rules v2 §5; Tier 0 items 5 & 6 RESOLVED — Tier 0 fully cleared except item 8, deferred)*
14. **Tier 1 batch confirmed (4 items, rapid-fire):** AE cost philosophy (mostly free/soft, hard costs rare), default multiplayer targeting (acting player's choice), elimination handling (full board to discard, seat skipped), ability activation limits (once per turn per source). Item 20 (collision order) resolved as moot given per-player orbit structure. *(Rules v2 §§2, 5, 9; Tier 1 items 15–17, 19, 20 RESOLVED)*
15. **CO stat-bucket math bug fixed** (≤4/5–6/≥7, non-overlapping). *(Tier 1 item 11 RESOLVED)*
16. **Hand economy → Draw 2 / play 2 (symmetric), provisional.** Draw-1/play-2 was checked mathematically and shown to drain hands to 0–1 by turn 5–6; draw-2/play-2 keeps hand size stable. Designer confirmed "until further notice." *(Rules v2 §8; Tier 0 item 8 PROVISIONAL)*
17. **Mock 1v1 playtest run with placeholder cards.** Surfaced six new rules gaps (items 33–38): Overtake mechanic, reclaim-as-action, Star Destruction timing, Size-0 handling, unplayable-CO edge case, and an Augmentation-dead-draw content note. All resolved same session. *(Rules v2 §§2, 3, 5, 6; Tier 0.5 items 33–38 RESOLVED, item 38 NOTED for later content work)*
18. **Further mock games (1v1 + 3p FFA) generated a 22-point punch list.** Designer resolved the first 6: reclaim destination legality mirrors Overtake (item 39); seat-elimination/Critical-Mass-anchor question deferred (item 40); FFA dogpile dynamics validated (item 41); all thresholds use current/effective stats (item 42); Passive abilities exempted from the once-per-turn-per-source activation limit (item 43); hand cap of 7 may be temporarily exceeded mid-turn (item 44). *(Rules v2 §§3, 5, 6, 8; Tier 0.5 items 39, 41–44 RESOLVED, item 40 DEFERRED)*
19. **Continued resolving the 22-point list, items 7–11.** Discard-1/draw-1 swap deferred (item 45). Self-inflicted Star Destruction confirmed identical to opponent-inflicted (item 46). Direct Effect AEs with no legal target are illegal, not fizzled (item 47). Augmentation-discard-on-exit generalized to any exit reason (item 48). Reclaimed COs must satisfy printed placement restrictions (item 49). *(Rules v2 §§2, 6, 8, 10; items 46–49 RESOLVED, item 45 DEFERRED — 11 of 22 closed)*
20. **Finished resolving the 22-point list, items 12–22.** Enters-orbit triggers fire on any placement method (item 50). Rotation collisions only possible when a card anchors/reverses a CO (item 51). Same-turn bounce-back reclaim fully allowed (item 52). Simultaneous Critical Mass deferred (item 53). Critical Mass check timing reconfirmed End-of-Turn-only (item 54). Illegal Overtake is a self-enforced constraint, not a system gap (item 55). No restriction on targeting mid-countdown (item 56). Out of Orbit zone has no size limit (item 57). Reclaim fully transfers ownership (item 58). No cap on repeated bounces (item 59). Item 60 remained open. *(Rules v2 §§2, 5, 6, 10; items 50–52, 54–59 RESOLVED, item 53 DEFERRED, item 60 OPEN — 21 of 22 closed)*
21. **Closed items 40 and 53.** Elimination-during-countdown confirmed intentional. Simultaneous Critical Mass confirmed to need no tie-break rule. *(Rules v2 §2; items 40, 53 RESOLVED — all 22 closed)*
22. **4-player FFA mock simulation run.** Validated per-player rotation, open-access reclaim/ownership-transfer, and parallel HP-race/Size-race dynamics across 4 players. Surfaced the countdown re-trigger edge case → deadline always the achiever's *next* turn. *(Rules v2 §2; item 61 RESOLVED)*
23. **Ran 3 more mock scenarios (2p Augmentation stacking, 6p FFA elimination/reclaim-chain test).** Augmentations stack without limit (item 62); eliminated player's Out of Orbit contributions remain shared (item 63); table-wide "any CO enters orbit" triggers allowed but flagged as power-level guideline (item 64). *(Rules v2 §§2, 10; items 62, 63 RESOLVED; item 64 NOTED)*
24. **Preliminary deck size set → ~90–100 unique CO+AE cards.** Benchmarked genre comps (Bang! ~80, Fluxx ~100, Love Letter/Coup smaller, Munchkin larger) and draw-volume math. Designer confirmed ~90–100. *(Rules v2 §11; Tier 3 item 30 PROVISIONAL)*
25. **Player-count scaling for hand economy — considered and rejected.** Designer corrected that duration targets are flexible, not hard constraints. Revised recommendation: keep hand economy flat across all player counts, consistent with genre precedent. *(Rules v2 §8; item 8 remains PROVISIONAL, confirmed flat-by-player-count)*
26. **Print-run size finalized → 108 total (12 Stars + 96 CO/AE).** Driven by print-industry base-12 economics and genre precedent (Sushi Go). 12/96 split: 12 Stars as 2x the 6-player max, 96 print-clean (8 sheets of 12). *(Rules v2 §11; Tier 3 item 30 LOCKED)*
27. **Star content design begun.** Formal Star design spec drafted (HP-tier resource allocation, mechanically-checkable archetype definitions, anti-patterns, one-sentence text-complexity ceiling) after an initial batch of 3 draft Stars was rejected for double-dipping a defensive advantage on a high-HP Star (fixed: 9–10 HP Stars get utility/economy abilities, never damage prevention). Compared against Bang!'s real distribution (near-binary). Landed on **1/3/4/3/1 (10–6 HP), kept provisional**, with **no-duplicate-Stars-per-table locked** (item 65). *(Rules v2 §10; Tier 2 item 24 PROVISIONAL, item 65 LOCKED)*
28. **Housekeeping: fixed a literal text-escape bug affecting 17 lines in the Audit**, restoring proper em dashes throughout.
29. **Star roster scope and selection method locked.** Compared leftover-variety ratios at max table size (Bang! ~56% unused at 7p vs. our exactly 50% unused at 6p) — proportionally comparable. Designer confirmed keeping 12 for the base set (item 66), and chose to offer both full-visibility draft and Bang!-style random-deal-then-choose as official rulebook variants (item 67). *(Rules v2 §10; items 66, 67 LOCKED)*
30. **First full round of actual Star card drafting.** Drafted 5 Stars against a formal design spec, then 3 more — one rejected for double-dipping a defensive advantage, fixed by banning defensive/damage-prevention abilities on the 9–10 HP tier specifically. Expanded to a full pool of 24 draft Stars. Designer's review cut 4 for being "boring or non-applicable" and flagged 6 more for rework (one card's temporary Stability bonus made permanent-on-first-reclaim to avoid unbounded stacking; a Critical-Mass-neutralizing card cut outright for removing the primary validated counterplay; a timing question exposed a real rules gap around End-of-Turn ordering; one card's jargon-laden wording prompted the full Collision-system unification (item 68); one card reworked to punish Augmentation-stacking specifically; one card redirected into a broader, once-per-turn-capped knockout-retaliation effect). *(Rules v2 §§3, 5, 10; Tier 2 item 24 progressing toward actual content)*
31. **Roster narrowed toward 12, dropped named cards in favor of stat/archetype/ability shorthand** (names not finalized). Working list stands at 12 cards across HP 9/8/7/6/5. Two significant changes: (1) HP range shifted from 6–10 down to **5–9**, tier shape changed to a deliberately **asymmetric 1/2/3/3/3** (rare-high, common-low) — both confirmed intentional pacing levers, dropping mean HP from 8.0 to 6.58 (~18%). (2) A **CO-per-turn cap** was locked (item 69) after modeling showed the existing 2-plays/turn rule could let Critical Mass be rushed as early as turn 2–3. First proposal (separate 1-placement + 1-reclaim caps) was found exploitable via a self-sacrifice-then-reclaim loop; resolved instead as one strict baseline (1 CO/turn, any source) with specific cards allowed to override it. *(Rules v2 §§5, 10; Tier 2 item 24 LOCKED; item 69 LOCKED)*
32. **Star Roster document created.** An Out-of-Orbit card's wording was given an explicit CO-per-turn-cap override clause (per item 69's design intent), confirmed as intentional and finalized.
33. **CO/AE split within the 96-card pool locked → 36 CO / 60 AE, all unique, no duplicate copies.** Reshuffle-on-empty already solves sustainability independent of copy count; keeping the base set fully unique also avoids future friction with Phase 2's constructed-deck copy-limit system. Presented two clean, print-friendly AE-heavy options (24/72 extreme vs. 36/60 moderate); recommended 36/60 since 24 unique COs would feel thin against the game's real archetype needs. Designer confirmed both the no-duplicates decision and the 36/60 split. *(Rules v2 §11; Tier 3 item 30 LOCKED)*
34. **Exact CO stat allocation grid locked.** Built a 5×5 Size-by-Stability grid, redirected to show actual per-cell design counts (raw combinatorial cell count skews toward high sums, unlike dice's uniform probability — hitting the 15/70/15 target requires deliberately overriding that natural skew). Distributed the 36-card target (5/25/6 across the three buckets) across specific cells. Designer made one further adjustment: reduced both "5-and-1" corner pairings from 2 to 1 each, redistributing the freed points. Final grid locked under item 11.
35. **CO Size/Stability marginal skew, and a self-caught error.** Computed expected Size per draw (2.78), confirmed the CO-per-turn cap prevents a fast rush, but noted Size and Stability marginals were identically shaped by accident. Recommended lower Stability / higher Size (more frequent, meaningful Collisions). While rebuilding the grid, discovered the prior grid had inadvertently drifted the locked 15/70/15 bucket split to roughly 6/23/7 — flagged transparently and corrected. Final grid preserves exact 5/25/6 bucket totals, skewing within each bucket toward higher-Size/lower-Stability: Size average rises to 3.14, Stability average falls to 2.42.
36. **Coverage gap found and fixed.** Size 1 showed zero designs at Stability 1, 2, and 3 — the skew had over-corrected. Also fixed a rendering bug (column headers drifting up to 32px off-center; display-only, data unaffected). Fix: pulled the skew back to even distribution specifically within the ≤4 bucket, keeping full skew in the 5–6 bucket. Final marginals settled at Size average 3.06, Stability average 2.50 — slightly less extreme but with only one true zero cell (Size 1, Stability 1).
37. **Skew recovered without sacrificing coverage.** The coverage fix (item 36) had quietly weakened the skew (3.14→3.06 Size avg, 2.42→2.50 Stability avg); asked for a redesign that kept both. Identified the actual constraint: the ≤4 bucket only has 5 cards over 6 cells, leaving no slack to both guarantee coverage and skew — but the 5–6 bucket (25 cards, 9 cells) has real slack. Set the ≤4 bucket to a coverage-first floor and pushed all recovered skew into the 5–6 bucket. Result exceeded the original target: Size average 3.36, Stability average 2.19, while keeping full coverage. Flagged one side effect: Size 4/Stability 1 is now a concentrated peak at 6 of 36 designs. *(This is the grid as printed in Part 1, §2 of the Build & Test Brief below, and in the stat table in Tier 2 item 11 above.)*

*(Next entries get added here as further items are resolved.)*

---
---

# PART 4 — BUILD & TEST BRIEF (CURRENT WORK ORDER)

**Purpose of this part:** a self-contained work order for generating the full 96-card CO/AE draw pile against the locked ruleset above, then stress-testing it via simulation. Executable from this file alone.

## 1. Scope of This Build

Generate the complete 96-card draw pile:

| Type | Count | Notes |
|---|---|---|
| Celestial Objects (COs) | 36 | All unique, no duplicates |
| Astronomical Events (AEs) | 60 | Split: Augmentations + Direct Effects, no duplicates |
| **Total** | **96** | Combined with the 12 Stars = 108-card print target |

Then run simulation testing of the full set against:
1. The locked ruleset (Part 1, in full)
2. The 12-card Star Roster (Part 2, as currently drafted)
3. Both win conditions, checked for pacing parity (Star Destruction vs. Critical Mass)

## 2. Hard Constraints on CO Generation (36 cards)

These are locked and not open to reinterpretation during content design:

- **Stat ranges:** Size 1–5, Stability 1–5.
- **Stat-distribution grid is locked exactly as follows** (final version — see Decision Log entry 37). Rows = Stability 1–5, columns = Size 1–5, cell values = card count:

  | Stability \ Size | 1 | 2 | 3 | 4 | 5 |
  |---|---|---|---|---|---|
  | **1** | 0 | 1 | 1 | 6 | 5 |
  | **2** | 1 | 1 | 3 | 3 | 2 |
  | **3** | 1 | 2 | 2 | 1 | 1 |
  | **4** | 1 | 2 | 1 | 1 | 0 |
  | **5** | 1 | 0 | 0 | 0 | 0 |

  This sums to exactly 36 and must be followed cell-for-cell — it is the final, designer-approved output of four iteration passes, not a target to re-derive. Size average should land at **3.36**, Stability average at **2.19**. **Size 4 / Stability 1 is a deliberate concentrated peak** (6 of 36, ~17%) — keep this in mind when assigning abilities so the peak isn't accidentally also the power peak.

- **Core vs. unique split:** 75/25 → **27 "core" (simple/vanilla-leaning or common pattern) designs, 9 "unique" (build-around/signature) designs.**
- **"Enters orbit" triggers** are legal on COs and fire on any placement into orbit (fresh play, Collision win, or reclaim) per Rules v2 §10.
- **Placement restrictions** (e.g., "must enter North") are legal design space on individual COs but must not be overused — Rules v2 §5 confirms placement is otherwise always legal, so restrictions should be a flavorful minority, not a default.
- **No CO text may reference internal rules jargon** that isn't itself reader-facing (e.g., don't print "Overtake" — that term is retired; use "Collision," which is the unified, current term per Decision Log entry 68).
- **Augmentation interaction note:** deliberately bias some CO design toward wanting Augmentations attached (e.g., "if this CO has an Augmentation attached, ...") to give early Augmentation draws a target — this is a content *goal* (Decision Log entry 17, item 38), not a separate hard constraint, but should visibly show up in the 36.

## 3. Hard Constraints on AE Generation (60 cards)

- **Two subtypes only:** Augmentations (attach to a CO in orbit; discarded whenever that CO leaves orbit for any reason) and Direct Effects (resolve once, discard).
- **No fixed subtype split is locked** — allocate Augmentations vs. Direct Effects by design need, but keep both subtypes meaningfully represented (neither should round to a token handful). Record whatever split is used in the final card list for the Audit log.
- **Cost philosophy (locked):** most AEs are free or carry only soft prerequisites (board-state/targeting conditions); hard costs (self-damage, discarding, sacrificing a CO) are reserved for the **strongest effects only** — this should be a small minority of the 60, not a baseline design pattern.
- **No instant-speed play** — every AE is a your-turn-only play; do not design around a stack/response pattern.
- **Direct Effects need a legal target to be playable at all** (illegal otherwise, per Rules v2 §10) — avoid designing Direct Effects whose only plausible target is something that may not exist on an empty board.
- **AE volume is the primary pacing lever** for Star Destruction vs. Critical Mass balance (Decision Log entry 13/27) — the simulation in §5 below depends on getting real damage-density numbers from this batch, so:
  - Track, as you generate, **how many of the 60 deal direct damage to an opposing Star**, and the average damage amount among those.
  - This number is a required output of this phase, not just a side effect — it feeds directly into the simulation in §5.
- **No duplicates** — all 60 unique.
- **Table-wide "whenever ANY CO enters orbit" triggers** (Decision Log entry 23, item 64) are allowed but should be rare/high-power, not a common pattern — treat as a signature effect for at most a couple of cards.

## 4. Process for This Build Phase

1. Generate the 36 COs first, strictly filling the locked stat grid (§2) cell by cell.
2. Generate the 60 AEs second, once CO text exists (so Augmentations can reference real CO stat ranges/abilities sensibly).
3. Cross-check against the Star Roster (Part 2, 12 cards) for thematic/mechanical overlap — avoid duplicating a Star's exact effect on a common CO/AE; complementary effects are fine and encouraged.
4. Produce a flat card list (name placeholders are fine — Star names are also still TBD per the roster's own open items) with, at minimum, for every card: type, Size/Stability (COs only), subtype (AEs only), full ability text, and which stat-grid cell or cost-tier it fills.
5. Hand off the completed 96-card list plus the damage-density tally (§3) into the simulation phase below.

## 5. Simulation Testing Plan

**Objective:** validate the two standing open modeling questions that have been flagged since Decision Log items 12 and 13, and which could not be answered without a real card pool:

1. **Critical Mass reachability (item 12):** model expected turns-to-15 total in-orbit Size, given the real CO Size distribution (§2 grid) and the CO-per-turn cap (Rules v2 §5: max 1 CO entering orbit/turn, any source). Compare against the earlier rough estimate of turn 6–8 with the cap in place.
2. **Star Destruction pacing (item 13):** model expected turns-to-kill using the real AE damage-density numbers tracked in §3, against the Star Roster's HP curve (1/2/3/3/3 across HP 9/8/7/6/5, mean 6.58). Compare the two paths' turn-counts for parity — the explicit design goal (Part A) is that **both win conditions should be comparably reachable**, not just thematically co-equal.

**Method:**
- Build a simple turn-by-turn simulator (random hand draws from the 96-card shared pool, reshuffle-on-empty per Rules v2 §8, 2-card hand economy, 1-CO-per-turn cap, 2-plays-per-turn cap) rather than hand-waving the math — this is explicitly what both open items have been waiting on.
- Run it across a spread of Star pairings (don't just test one Star matchup) — include at least one high-HP/weak-ability Star (HP 9) and one low-HP/strong-ability Star (HP 5) on each side, since the roster's curve ties HP inversely to ability strength by design.
- Run both 1v1 and a 3–4 player FFA configuration, since elimination/seat-skipping (Rules v2 §2) and per-player rotation (§4) could change pacing dynamics between modes.
- Record for each run: winning condition (Star Destruction vs. Critical Mass), turn count at game end, and whether a Critical Mass countdown was ever cancelled/re-triggered (relevant to whether the simulated "AI" actually uses the counterplay window, or whether a smarter opponent would behave differently).

**Deliverable from this phase:** a short results summary (turn-count distributions for each win path, overall win-path split) plus a call on whether the **"Remaining tuning lever"** noted in Rules v2 §10 — increasing AE damage output and/or the proportion of damage-dealing cards — needs to be pulled, and if so by how much. This output updates Decision Log items 12 and 13 from `OPEN` to `RESOLVED` and should be written back into the Status Board (Part B) and Decision Log (Part D) with the actual numbers, not just a verdict.

## 6. What NOT to Touch in This Phase

- Do not alter Rules v2 (Part 1) — it is canonical and locked except where explicitly marked `[OPEN]` or `[PROVISIONAL]`.
- Do not assign final Star names — that's tracked as its own open item on the Star Roster (Part 2) and is independent of this build.
- Do not resolve the Star Roster's archetype-balance open item (Denial/control underrepresented at 1 card vs. a 2-per-archetype plan) as part of this phase — flag it again in the handoff if the CO/AE pool doesn't help compensate for it, but don't silently rebalance the Stars themselves here.
- If simulation results suggest a Rules v2 change (e.g., the CO-per-turn cap or hand economy numbers need adjustment), **do not edit Rules v2 directly** — bring the finding back as a new Decision Log item for the designer to decide, per the project's standing working relationship (see Part 3 header).

---

*End of consolidated document. This file should be treated as read-only reference once generated — updates to any individual section should still be made in the respective source document, with this consolidated file regenerated afterward if a fresh combined copy is needed.*
