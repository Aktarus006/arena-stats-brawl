# Arena Competitive Brawl Lab

An Obsidian-friendly, local-first tracker for MTG Arena Competitive Brawl.

The match notes remain the human-readable source. The dashboard is generated from their YAML frontmatter, so it never requires a persistent AI conversation to retain context.

## Local dashboard

```bash
python3 tools/build_data.py
python3 -m http.server 4173 --bind 127.0.0.1
```

Then open: http://127.0.0.1:4173/site/

## Log the next game

```bash
python3 tools/log_game.py
```

The interactive logger creates:

- a structured record in `data/manual_games.jsonl`;
- an Obsidian match note in `Decks/Squall/Matches/`;
- refreshed `data/dashboard.json` for the local website.

It asks for the small set of fields that make future analysis useful: result, opponent/archetype, play/draw, mulligans, game length, mana issue, whether Squall cast/connected, a primary loss cause, and decisive cards.

## Data model

- `Decks/Squall/Matches/*.md`: narrative match reports and historical source.
- `data/dashboard.json`: generated dashboard data; do not hand-edit.
- `data/manual_games.jsonl`: structured records created by the new logger.
- `tools/build_data.py`: imports historical notes and builds the dashboard data.
- `tools/tracker.py`: normalization and aggregation rules.

The historical Games 1–40 are assigned to V1 at the user's direction; V2 begins at Game 41 and V2.1 at Game 51. New match notes always record their exact active version.

## Tests

```bash
python3 -m unittest tests/test_tracker.py -v
```
