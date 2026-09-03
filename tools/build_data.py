#!/usr/bin/env python3
"""Build dashboard data from Obsidian game notes plus newly logged JSON records."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from tracker import normalize_game, summarize_games  # noqa: E402

MATCHES = ROOT / "Decks" / "Squall" / "Matches"
DECKLIST = ROOT / "Decks" / "Squall" / "Decklist.md"
DATA = ROOT / "data"


def scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"\d+", value):
        return int(value)
    return value.strip('"\'')


def parse_frontmatter(text: str) -> dict[str, Any]:
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    data: dict[str, Any] = {}
    current_list: str | None = None
    for line in match.group(1).splitlines():
        list_item = re.match(r"^\s+-\s+(.*)$", line)
        if list_item and current_list:
            data.setdefault(current_list, []).append(scalar(list_item.group(1)))
            continue
        key_value = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if key_value:
            key, value = key_value.groups()
            current_list = key if value == "" else None
            data[key] = [] if value == "" else scalar(value)
    return data


def current_decklist() -> dict[str, Any]:
    """Read the active Obsidian decklist without duplicating it by hand."""
    text = DECKLIST.read_text(encoding="utf-8")
    commander_match = re.search(r"## Commander\n\n```text\n\d+ (.+?)\n```", text)
    deck_match = re.search(r"## Deck\n\n```text\n(.*?)```", text, re.DOTALL)
    if not commander_match or not deck_match:
        raise ValueError("Current decklist is missing a Commander or Deck text block")
    cards = []
    for line in deck_match.group(1).splitlines():
        match = re.fullmatch(r"(\d+) (.+)", line.strip())
        if match:
            cards.append({"quantity": int(match.group(1)), "name": match.group(2)})
    return {
        "commander": commander_match.group(1),
        "cards": cards,
        "total_cards": 1 + sum(card["quantity"] for card in cards),
    }


def inferred_version(game_id: int, version: str) -> str:
    if version:
        return version
    if game_id <= 40:
        return "V1"
    if 41 <= game_id <= 50:
        return "V2"
    if game_id >= 51:
        return "V2.1"
    return "Legacy / unversioned"


def note_games() -> list[dict[str, Any]]:
    games = []
    for path in sorted(MATCHES.glob("*.md")):
        raw = parse_frontmatter(path.read_text(encoding="utf-8"))
        game = normalize_game(raw, str(path.relative_to(ROOT)))
        game["deck_version"] = inferred_version(game["id"], game["deck_version"] if game["deck_version"] != "Legacy / unversioned" else "")
        games.append(game)
    return games


def manual_games() -> list[dict[str, Any]]:
    path = DATA / "manual_games.jsonl"
    if not path.exists():
        return []
    games = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            games.append(json.loads(line))
    return games


def build() -> dict[str, Any]:
    games_by_id = {game["id"]: game for game in note_games()}
    games_by_id.update({game["id"]: game for game in manual_games()})
    games = [games_by_id[key] for key in sorted(games_by_id)]
    return {
        "deck": {
            "name": "Squall, SeeD Mercenary",
            "format": "MTG Arena Competitive Brawl",
            "current_version": "V2.1",
            "source": "Decks/Squall/Decklist.md",
            "list": current_decklist(),
        },
        "games": games,
        "summary": summarize_games(games),
    }


def main() -> None:
    DATA.mkdir(exist_ok=True)
    payload = build()
    target = DATA / "dashboard.json"
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built {target.relative_to(ROOT)}: {len(payload['games'])} games")


if __name__ == "__main__":
    main()
