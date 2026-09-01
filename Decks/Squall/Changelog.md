# Squall — Changelog

## Pre-testing construction

The list went through extensive cuts and additions before the match log began. Important design decisions included:

- Keep **Buster Sword**, **Enduring Innocence** and **Kutzil's Flanker** when trimming.
- Add/retain recursion-friendly low-cost permanents and artifacts.
- Add **Lurrus of the Dream-Den** as a secondary graveyard-value engine.
- Add **Grand Abolisher**, **Cathar Commando** and **Braids, Arisen Nightmare** during refinement.
- Prefer **The Sackville-Bagginses** over Emperor of Bones in a late construction decision.
- Remove **Necrodominance** because exiling cards conflicted with the graveyard-recursion plan.
- **Necropotence** remained in the tested list at that stage.

## After Game 20 — mana experiment

### OUT
- Ketramose, the New Dawn

### IN
- Multiversal Passage

### Reason
Five of the first 20 game reports mentioned missed land development (Games 9, 13, 16, 18, 20), with Games 9, 13 and 18 strongly associated with losses. Ketramose had also felt underwhelming in actual play.

### Early result
Games 21–30 reported no natural missed-land-drop game, though Game 28 exposed a separate white-source/color-quality issue.

## After Game 40 — V2 interaction refactor

### Archived version
- [[Versions/V1 - Games 31-40]]

### OUT
- Caustic Bronco
- Dark Confidant
- Enduring Innocence
- Moonshadow
- Nethergoyf
- Phelia, Exuberant Shepherd

### IN
- Erode
- Farewell
- Path to Exile
- Reprieve
- Seam Rip
- Sheoldred's Edict

### Reason
The first 40 games showed that several synergy/value creatures were producing too little impact in real games:

- **Enduring Innocence** had not produced meaningful value.
- **Caustic Bronco** had never meaningfully used saddle.
- **Moonshadow** had reached only modest combat stats and did not interact.
- **Nethergoyf** functioned mostly as a body rather than disruption/value.
- **Dark Confidant** had contributed to life-pressure problems and even a recorded self-lethal game.
- **Phelia** was replaced directly by **Erode** to increase immediate interaction.

Meanwhile, losses repeatedly involved insufficient ability to stop opposing engines, large threats, persistent noncreature permanents, or developed boards. V2 therefore shifts six slots from conditional value/threats into efficient interaction, tempo, and a hard reset.

### V2 hypothesis
**Every card should be strong before Squall; Squall should make strong interaction reusable rather than be the only reason a card is playable.**

Games 41+ should be treated as the V2 test sample.

## After Game 50 — V2.1 recursive interaction toolbox

### Archived version
- [[Versions/V2 - Games 41-50]]

### V2 result
- Games 41–50: **1–9**.
- The result was poor, but the six V2 additions were barely observed during the block: only **Seam Rip** and **Reprieve** were reported as drawn, once each.

### OUT
- Braids, Arisen Nightmare
- The Sackville-Bagginses
- Kaya's Ghostform
- Necropotence

### IN
- Loran of the Third Path
- Sheltered by Ghosts
- Plaguecrafter
- Ral Zarek, Guest Lecturer

### Reason
The 50-game audit showed repeated losses to permanent-based engines and threats that ordinary one-for-one creature removal could not efficiently contain. V2.1 increases the density of interaction that either lives on a creature body or supports the recursion/toolbox plan without depending on Squall to be useful.

- **Loran of the Third Path** adds Recruiter-compatible artifact/enchantment removal and directly addresses repeated losses to noncreature engines.
- **Sheltered by Ghosts** combines removal with protection/pressure, helping both the reactive plan and Squall's need to connect.
- **Plaguecrafter** adds a non-targeting sacrifice axis alongside Accursed Marauder and Sheoldred's Edict, useful against indestructible, ward, hexproof, protection, and planeswalkers.
- **Ral Zarek, Guest Lecturer** provides Surveil and a second recursion engine for mana-value-3-or-less creatures, particularly the growing ETB interaction toolbox.

**Warren Soultrader remains in V2.1 for testing.** With more ETB creatures such as Loran and Plaguecrafter, voluntarily sacrificing a creature after it has generated value can produce a Treasure and make that creature available for Squall/Ral recursion again.

Games 51+ are the V2.1 test sample.

## Versioning policy

For every major deck revision:

1. Archive the exact outgoing list under `Versions/`.
2. Update `Decklist.md` to the new current list.
3. Record all OUT/IN changes here with the game-number boundary and reason.
4. Tag subsequent match notes with the active version when practical.

This preserves both Git history and human-readable deck-version history for later A/B analysis.
