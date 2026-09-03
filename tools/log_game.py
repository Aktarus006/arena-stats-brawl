#!/usr/bin/env python3
"""Fast local post-game logger. It creates both a structured record and a readable note."""

from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "manual_games.jsonl"
MATCHES = ROOT / "Decks" / "Squall" / "Matches"


def ask(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def choice(label: str, allowed: set[str], default: str) -> str:
    while True:
        value = ask(label, default).lower()
        if value in allowed:
            return value
        print(f"Choose one of: {', '.join(sorted(allowed))}")


def next_id() -> int:
    existing = [int(match.name[:3]) for match in MATCHES.glob("[0-9][0-9][0-9] - *.md")]
    return max(existing, default=0) + 1


def filename_part(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]", "-", value).strip()
    return cleaned or "Unknown opponent"


def main() -> None:
    game_id = next_id()
    result = choice("Result (win/loss)", {"win", "loss"}, "win")
    opponent = ask("Opponent commander", "Unknown")
    archetype = ask("Archetype", "Unknown")
    rank = ask("Rank", "Unknown")
    play_draw = choice("Play/draw/unknown", {"play", "draw", "unknown"}, "unknown")
    mulligans = ask("Mulligans", "0")
    turns = ask("Game length in turns", "")
    mana = choice("Mana issue (none/missed_land_drop/color_screw_white/color_screw_black/land_denial/flood/unknown)", {"none", "missed_land_drop", "color_screw_white", "color_screw_black", "land_denial", "flood", "unknown"}, "none")
    squall_cast = choice("Squall cast? (yes/no/unknown)", {"yes", "no", "unknown"}, "unknown")
    squall_connected = choice("Squall connected? (yes/no/unknown)", {"yes", "no", "unknown"}, "unknown")
    cause = ask("Primary loss cause (engine/ramp/aggro/commander_snowball/stack_interaction/wipe/mana/life_total/pilot_error/unknown)", "unknown")
    mvp = [card.strip() for card in ask("Decisive cards, comma-separated", "").split(",") if card.strip()]
    summary = ask("One-sentence turning point", "")

    game = {
        "id": game_id, "played_at": date.today().isoformat(), "deck": "Squall, SeeD Mercenary",
        "deck_version": "V2.1", "result": result, "opponent": opponent, "archetype": archetype,
        "rank": rank, "play_draw": play_draw, "mulligans": int(mulligans or 0), "turns": int(turns) if turns.isdigit() else None,
        "mana_issue": mana, "squall_cast": squall_cast, "squall_connected": squall_connected,
        "primary_cause": cause, "mvp": mvp,
        "source_note": f"Decks/Squall/Matches/{game_id:03d} - {filename_part(opponent)}.md",
    }
    DATA.parent.mkdir(exist_ok=True)
    with DATA.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(game, ensure_ascii=False) + "\n")

    note = MATCHES / f"{game_id:03d} - {filename_part(opponent)}.md"
    note.write_text(
        "---\n" + "\n".join([
            f"game: {game_id}", "deck: Squall, SeeD Mercenary", "deck_version: V2.1",
            f"result: {result}", f"opponent: {opponent}", f"archetype: {archetype}", f"rank: {rank}",
            f"play_draw: {play_draw}", f"mulligans: {game['mulligans']}", f"turns: {game['turns'] or ''}",
            f"mana_issue: {mana}", f"squall_cast: {squall_cast}", f"squall_connected: {squall_connected}",
            f"primary_cause: {cause}", "mvp:", *[f"  - {card}" for card in mvp], "---",
        ]) + f"\n\n# Game {game_id:03d} — {opponent}\n\n## Turning point\n\n{summary}\n",
        encoding="utf-8",
    )
    subprocess.run(["python3", str(ROOT / "tools" / "build_data.py")], check=True)
    print(f"Logged Game {game_id:03d}: {note.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
