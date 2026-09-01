# Squall — 50-Game Audit

## Executive summary

**Arena record after 50 games: 19–31 (38.0%).**

One recorded win (Game 34 vs Tourach) was a probable disconnect/non-game. Excluding it for deck-performance analysis gives **18–31 (36.7%)** across 49 meaningful games.

The current result is not good enough for a competitive target, but the data does **not** support the simple conclusion that Squall's recursion concept is fundamentally bad. The strongest games repeatedly show that Squall is powerful when the deck first disrupts the opponent, protects/opens a connection, and then recycles already-good cards.

The main structural problem is that the list often interacts **one card at a time** while opposing decks generate **multiplicative engines** (ramp, artifacts, commander engines, free interaction). Once those engines cross a threshold, Squall's incremental recursion cannot catch up fast enough.

## Results by block

| Games | Record | Win rate | Notes |
|---|---:|---:|---|
| 1–10 | 7–3 | 70% | Strong opening sample; several explosive Squall starts and good toolbox performances. |
| 11–20 | 4–6 | 40% | Mana screw and life-pressure issues became visible. |
| 21–30 | 4–6 | 40% | Multiversal Passage experiment improved raw land-drop consistency; one clear white color-screw remained. |
| 31–40 | 3–7 | 30% | One win was a probable disconnect. Meaningful record: 2–7. Opponents increasingly featured free interaction, artifact engines and big mana. |
| 41–50 (V2) | 1–9 | 10% | Extremely poor result, but V2 cards were barely drawn: only Seam Rip and Reprieve were reported once each. |

## V2 card exposure

Six cards entered after Game 40:

- Erode — **not reported seen**
- Farewell — **not reported seen**
- Path to Exile — **not reported seen**
- Reprieve — **seen once; useful in Game 49**
- Seam Rip — **seen once; answered by Sheltered by Ghosts in Game 48**
- Sheoldred's Edict — **not reported seen**

Therefore the 1–9 V2 result is a valid result for the **99-card configuration**, but it is not yet a fair performance test of the six specific additions.

## What is actually losing games?

The 31 recorded losses are heterogeneous, but several recurring families are clear.

### 1. Engine / snowball decks

Repeated examples include:

- Grist recursion + Chthonian Nightmare / Strip Mine lines
- Thor equipment/blink infrastructure
- Ugin + Forsaken Monument
- Golos / Lumra-style big-mana starts
- Roxanne + Roaming Throne
- Leonardo/Mickey + Bitterblossom + sacrifice/counter engine
- Iron Man artifact aggro
- The Notary Hobbits ramp into Ulamog/Emrakul
- Urza + Paradox Engine/artifact network

**Core lesson:** removing one payoff creature often delays the loss without dismantling the engine producing the next threat.

### 2. Ramp / resource inequality

Several losses occur after the opponent reaches a mana tier Squall cannot match efficiently: Poq, Raph/Mickey, Lumra/Golos shells, Ugin, Notary Hobbits and related strategies.

Squall has shown that **Strip Mine recursion** can reverse this axis when it comes online. The deck is significantly better when disruption attacks the opponent's mana engine *before* it becomes several turns ahead.

### 3. Free / low-cost stack interaction

Important examples:

- Yuriko Game 31: Daze + Flare of Denial + Force of Negation
- Kefka Game 32: concentrated counters while Squall stalled on mana
- Yuriko Game 37: Force of Negation stopped the lethal setup
- Kinnan Game 50: tapped-out opponent protected Kinnan with Fierce Guardianship, then Time Warp

**Core lesson:** additional creature removal does not solve this problem. Discard and protected-turn effects (Grand Abolisher, Voice of Victory, Ranger-Captain) are strategically different and important.

### 4. Board resets / inability to reset

- Korvold Game 35 explicitly required a sweeper that was never found.
- Raph/Mickey Game 29 used Blasphemous Act to erase a strong Squall board.
- Hei Bai Game 47 topdecked a board wipe that simultaneously rebuilt its engine.
- Amalia Game 15 swung on opposing Toxic Deluge.

The deck benefits from having real reset buttons. **Toxic Deluge and The Meathook Massacre are validated; Farewell remains untested.**

### 5. Mana / color / life failures

Mana-development losses were materially present in the early sample (notably Games 9, 13 and 18), plus Game 32 later. Game 28 was a distinct **white color-screw** despite three lands.

The Multiversal Passage change appears to have reduced pure missed-land-drop frequency. The next mana concern is more about **colored-source quality** than simply increasing land count.

Life pressure also mattered, especially with the old Dark Confidant configuration. Dark Confidant directly contributed to the Game 11 loss and has now been removed.

## Strongly validated core

These cards have repeatedly demonstrated concrete game impact and should not be cut casually:

- Squall, SeeD Mercenary
- Dark Ritual
- Esper Sentinel
- Mother of Runes
- Skrelv, Defector Mite
- Giver of Runes
- Ademi of the Silkchutes / Spectacular Spider-Man
- Barrowgoyf
- Sheoldred, the Apocalypse
- Lurrus of the Dream-Den
- Ripples of Undeath
- Disruptor Flute
- Drannith Magistrate
- Kutzil's Flanker
- Werefox Bodyguard
- Boggart Trawler
- Recruiter of the Guard
- Cloud, Midgar Mercenary
- Lightning Greaves
- Key to the City
- Skyclave Apparition
- The Meathook Massacre
- Toxic Deluge

### Important supporting cards / plans

- Thoughtseize / Inquisition / Deep-Cavern Bat: proactive information and protection against counters/engines.
- Ranger-Captain of Eos / Grand Abolisher / Voice of Victory: create protected windows rather than merely trading resources.
- Cathar Commando: role is increasingly relevant because artifact/enchantment engines are a recurring weakness.
- Stoneforge Mystic / Cloud equipment toolbox: demonstrated useful setup, especially for Greaves and Shadowspear.

## Cards that were correctly removed in V2

### Enduring Innocence
No meaningful positive match impact observed over the first 40 games.

### Moonshadow
Reported maximum performance was only about a 3/3 despite theoretical graveyard synergy. It does not disrupt, protect or generate immediate value.

### Caustic Bronco
Never meaningfully used its saddle mode in the reported sample; theoretical ceiling was not realized.

### Nethergoyf
Redundant "big body" role without Barrowgoyf's lifelink/evasion/value package.

### Dark Confidant
Powerful in isolated games but materially dangerous given the deck's fetch/shock/Tomb/Ripples/Thoughtseize life pressure. Cutting it also makes expensive reset effects safer to include.

### Phelia, Exuberant Shepherd
Low observed impact relative to an interaction slot.

**Conclusion:** the 1–9 V2 start is not evidence that these six cuts were mistakes. None of the removed cards had become an important pillar in the match data.

## Current cards that still need to justify their slots

These are not automatic cuts, but their match impact is poorly demonstrated relative to the current competitive goal:

- Braids, Arisen Nightmare
- Warren Soultrader
- The Sackville-Bagginses
- Buster Sword (has had useful moments, but equipment density must justify every slot)
- Kaya's Ghostform (high synergy with Squall, but should be judged against standalone protection/interaction)
- Lotho, Corrupt Shirriff
- The Queen of Dale (good curve/value moments, but limited decisive sample)
- Necropotence (power level is obvious, but actual match contribution and life cost should be tracked)

Do **not** cut all of these at once. They are the correct zone to examine for V2.1 once the interaction package has actually been drawn enough to evaluate.

## Candidate additions under discussion

### Sheltered by Ghosts — HIGH interest

A particularly attractive candidate because it simultaneously:

1. removes a problematic nonland permanent,
2. improves/protects a creature,
3. helps Squall connect,
4. is independently playable rather than existing only for recursion synergy.

Game 48 demonstrated its power from the opposing side when it protected Light-Paws from Seam Rip.

### Land Tax — MEDIUM / contextual interest

Potentially improves land consistency and long-game hand resources, but it does not interact with an opposing engine. With only six basics in the current list, its practical ceiling must be examined before inclusion. It is more of a consistency tool than a solution to the major loss patterns.

### Teferi's Protection — MEDIUM-HIGH interest

Excellent against wipes/lethal turns and protects a developed board, but does not stop an opponent from establishing a ramp/artifact engine. Better viewed as protection than interaction.

### Mana Tithe — MEDIUM interest

High tempo ceiling at one mana, but poor late-game topdeck. Reprieve is currently the preferred white stack-interaction experiment because it remains live later and replaces itself.

## Strategic diagnosis

The deck should **not** be rebuilt as "maximum recursion" and should also **not** become pure Orzhov removal-control.

The successful identity is:

> **disrupt → establish a protected Squall connection → recur premium interaction/value → convert that recursion into tempo and pressure.**

Squall is strongest as the **reward for surviving/disrupting the early game**, not as the only plan.

The weakest structural scenario is:

> trade 1-for-1 → opponent's engine generates 2-for-1 or 3-for-1 → trade again → fall behind → Squall recursion arrives too late.

Therefore future changes should prioritize interaction that either:

- hits broad permanent types,
- attacks engines before they multiply,
- creates protected turns,
- or performs two roles at once (interaction + protection / interaction + pressure).

## Recommendation after Game 50

### Do not revert V2

The six V1 cuts remain defensible and four of the six V2 additions have not even been seen. Reverting now would confuse a bad 10-game result with evidence that the old low-impact cards were better.

### Do not add another pile of narrow removal immediately

The deck already loses some games while holding/drawing good creature interaction. Free counters, artifact engines and resource multiplication require different answers.

### Next test protocol

Keep V2 stable for another short block **unless a clearly superior dual-purpose card replaces a demonstrably weak slot**. For Games 51 onward, explicitly record:

- which V2 cards were drawn,
- whether they were cast,
- whether the opponent's key engine was identified and answered,
- whether Squall connected at least once,
- whether the loss came before or after Squall established recursion,
- whether a wipe was needed/drawn,
- whether a protected-turn card was present.

A V2.1 change should be based on those observations, not solely the 1–9 record.

## Current priority watchlist

1. **Sheltered by Ghosts** — strongest prospective addition.
2. Another **broad artifact/enchantment/permanent answer** if noncreature-engine losses continue.
3. **Teferi's Protection** if board-wipe blowouts remain frequent.
4. **Land Tax** only if mana consistency again becomes a recurring issue.

## Bottom line

The current 38% Arena win rate is below the competitive target and warrants changes/continued refinement. But the 50-game log does not point to "Squall recursion is bad." It points to a deck whose best cards and best lines are competitive, while a remaining layer of medium-impact slots and the difficulty of answering multiplicative engines prevent those lines from appearing consistently enough.

The next version should become **less cute, more dual-purpose, and more proactive about engines**, without giving up the recursive toolbox that produced the deck's strongest wins.
