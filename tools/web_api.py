"""Validated writes for the local Arena Brawl Lab web form."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ALLOWED = {
    "result": {"win", "loss"},
    "play_draw": {"play", "draw", "unknown"},
    "mana_issue": {"none", "missed_land_drop", "color_screw_white", "color_screw_black", "land_denial", "flood", "unknown"},
    "squall_cast": {"yes", "no", "unknown"},
    "squall_connected": {"yes", "no", "unknown"},
}


def _clean(value: Any, default: str = "Unknown") -> str:
    return str(value).strip() or default


def _choice(payload: dict[str, Any], field: str) -> str:
    value = _clean(payload.get(field), "unknown").lower()
    if value not in ALLOWED[field]:
        raise ValueError(f"{field} must be one of: {', '.join(sorted(ALLOWED[field]))}")
    return value


def _filename_part(value: str) -> str:
    return re.sub(r"[\\/:*?\"<>|]", "-", value).strip() or "Unknown opponent"


def _next_id(matches: Path) -> int:
    existing = [int(note.name[:3]) for note in matches.glob("[0-9][0-9][0-9] - *.md")]
    return max(existing, default=0) + 1


def create_game(root: Path, payload: dict[str, Any], today: str | None = None) -> dict[str, Any]:
    """Persist a web-submitted match as JSONL and as an Obsidian note."""
    matches = root / "Decks" / "Squall" / "Matches"
    matches.mkdir(parents=True, exist_ok=True)
    game_id = _next_id(matches)
    opponent = _clean(payload.get("opponent"))
    mvp = payload.get("mvp", [])
    if isinstance(mvp, str):
        mvp = [item.strip() for item in mvp.split(",") if item.strip()]
    if not isinstance(mvp, list):
        raise ValueError("mvp must be a list or comma-separated string")
    try:
        mulligans = int(payload.get("mulligans", 0))
        turns = int(payload["turns"]) if str(payload.get("turns", "")).strip() else None
    except (TypeError, ValueError) as error:
        raise ValueError("mulligans and turns must be numbers") from error
    game = {
        "id": game_id,
        "played_at": today or date.today().isoformat(),
        "deck": "Squall, SeeD Mercenary",
        "deck_version": "V2.1",
        "result": _choice(payload, "result"),
        "opponent": opponent,
        "archetype": _clean(payload.get("archetype")),
        "rank": _clean(payload.get("rank")),
        "play_draw": _choice(payload, "play_draw"),
        "mulligans": mulligans,
        "turns": turns,
        "mana_issue": _choice(payload, "mana_issue"),
        "squall_cast": _choice(payload, "squall_cast"),
        "squall_connected": _choice(payload, "squall_connected"),
        "primary_cause": _clean(payload.get("primary_cause"), "unknown"),
        "mvp": [_clean(card, "") for card in mvp if _clean(card, "")],
        "source_note": f"Decks/Squall/Matches/{game_id:03d} - {_filename_part(opponent)}.md",
    }
    data = root / "data"
    data.mkdir(exist_ok=True)
    with (data / "manual_games.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(game, ensure_ascii=False) + "\n")
    note = matches / f"{game_id:03d} - {_filename_part(opponent)}.md"
    note.write_text(
        "---\n" + "\n".join([
            f"game: {game_id}", "deck: Squall, SeeD Mercenary", "deck_version: V2.1",
            f"result: {game['result']}", f"opponent: {opponent}", f"archetype: {game['archetype']}",
            f"rank: {game['rank']}", f"play_draw: {game['play_draw']}", f"mulligans: {mulligans}",
            f"turns: {turns or ''}", f"mana_issue: {game['mana_issue']}",
            f"squall_cast: {game['squall_cast']}", f"squall_connected: {game['squall_connected']}",
            f"primary_cause: {game['primary_cause']}", "mvp:", *[f"  - {card}" for card in game["mvp"]], "---",
        ]) + f"\n\n# Game {game_id:03d} — {opponent}\n\n## Turning point\n\n{_clean(payload.get('turning_point'), '')}\n",
        encoding="utf-8",
    )
    return game
