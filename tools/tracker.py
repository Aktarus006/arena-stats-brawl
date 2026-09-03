"""Structured-data helpers for the Arena Competitive Brawl tracker.

The markdown notes remain the narrative record. This module turns their
frontmatter into deliberately small, validated data for the local dashboard.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

RESULTS = {"w": "win", "win": "win", "l": "loss", "loss": "loss"}
MANA_ISSUES = {
    "": "none",
    "false": "none",
    "none": "none",
    "true": "unknown",
    "missed_land_drop": "missed_land_drop",
    "missed_land_drops": "missed_land_drop",
    "white_color_screw": "color_screw_white",
    "black_color_screw": "color_screw_black",
    "land_denial": "land_denial",
}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_game(raw: dict[str, Any], source_note: str) -> dict[str, Any]:
    """Normalize historic free-form YAML while keeping unknowns explicit."""
    result_raw = _clean(raw.get("result")).lower()
    result = RESULTS.get(result_raw, "unknown")
    mana_raw = _clean(raw.get("mana_issue")).lower()
    mana_issue = MANA_ISSUES.get(mana_raw, mana_raw or "none")
    game_id = int(raw.get("game", 0))
    mvp = raw.get("mvp", [])
    if not isinstance(mvp, list):
        mvp = []
    return {
        "id": game_id,
        "result": result,
        "opponent": _clean(raw.get("opponent")) or "Unknown",
        "archetype": _clean(raw.get("archetype")) or "Unknown",
        "deck": _clean(raw.get("deck")) or "Squall, SeeD Mercenary",
        "deck_version": _clean(raw.get("deck_version")) or "Legacy / unversioned",
        "rank": _clean(raw.get("rank")) or "Unknown",
        "mana_issue": mana_issue,
        "mvp": [str(card) for card in mvp],
        "source_note": source_note,
    }


def record(games: list[dict[str, Any]]) -> dict[str, Any]:
    wins = sum(game["result"] == "win" for game in games)
    losses = sum(game["result"] == "loss" for game in games)
    counted = wins + losses
    return {
        "games": len(games),
        "wins": wins,
        "losses": losses,
        "win_rate": round((wins / counted * 100) if counted else 0, 1),
    }


def summarize_games(games: list[dict[str, Any]]) -> dict[str, Any]:
    """Return dashboard-ready aggregates without drawing causal conclusions."""
    versions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    archetypes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    mana = Counter()
    card_mentions = Counter()
    for game in games:
        versions[game["deck_version"]].append(game)
        archetypes[game["archetype"]].append(game)
        if game["mana_issue"] != "none":
            mana[game["mana_issue"]] += 1
        card_mentions.update(game.get("mvp", []))
    return {
        "overall": record(games),
        "versions": {name: record(rows) for name, rows in sorted(versions.items())},
        "archetypes": {name: record(rows) for name, rows in sorted(archetypes.items())},
        "mana_issues": dict(sorted(mana.items())),
        "mvp_mentions": dict(card_mentions.most_common()),
        "data_quality": {
            "version_known": sum(g["deck_version"] != "Legacy / unversioned" for g in games),
            "archetype_known": sum(g["archetype"] != "Unknown" for g in games),
            "rank_known": sum(g.get("rank", "Unknown") != "Unknown" for g in games),
        },
    }
