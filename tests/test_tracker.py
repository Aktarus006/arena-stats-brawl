import json
import sys
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "tools"))

from build_data import inferred_version, current_decklist  # noqa: E402
from tracker import normalize_game, summarize_games  # noqa: E402


class NormalizeGameTests(unittest.TestCase):
    def test_normalizes_legacy_result_and_mana_issue(self):
        game = normalize_game(
            {
                "game": 9,
                "result": "L",
                "opponent": "5C Phyrexian Omnath",
                "mana_issue": "missed_land_drops",
            },
            "Matches/009 - 5C Phyrexian Omnath.md",
        )

        self.assertEqual(game["id"], 9)
        self.assertEqual(game["result"], "loss")
        self.assertEqual(game["mana_issue"], "missed_land_drop")
        self.assertEqual(game["deck_version"], "Legacy / unversioned")
        self.assertEqual(game["source_note"], "Matches/009 - 5C Phyrexian Omnath.md")

    def test_keeps_structured_mvp_cards(self):
        game = normalize_game(
            {
                "game": 60,
                "result": "win",
                "opponent": "Captain America",
                "mvp": ["Skrelv, Defector Mite", "Get Lost"],
            },
            "Matches/060 - Captain America.md",
        )

        self.assertEqual(game["result"], "win")
        self.assertEqual(game["mvp"], ["Skrelv, Defector Mite", "Get Lost"])


class VersionInferenceTests(unittest.TestCase):
    def test_uses_v1_for_all_pre_v2_games(self):
        self.assertEqual(inferred_version(1, ""), "V1")
        self.assertEqual(inferred_version(31, ""), "V1")
        self.assertEqual(inferred_version(40, ""), "V1")


class DecklistImportTests(unittest.TestCase):
    def test_imports_current_deck_at_one_hundred_cards(self):
        decklist = current_decklist()
        self.assertEqual(decklist["total_cards"], 100)
        self.assertEqual(decklist["commander"], "Squall, SeeD Mercenary")
        self.assertTrue(any(card["name"] == "Get Lost" for card in decklist["cards"]))


class SummaryTests(unittest.TestCase):
    def test_summary_calculates_version_records_and_flags_unknowns(self):
        games = [
            {"id": 1, "result": "win", "deck_version": "V2.1", "archetype": "aggro", "mana_issue": "none"},
            {"id": 2, "result": "loss", "deck_version": "V2.1", "archetype": "aggro", "mana_issue": "none"},
            {"id": 3, "result": "loss", "deck_version": "V2", "archetype": "ramp", "mana_issue": "color_screw_white"},
        ]

        summary = summarize_games(games)

        self.assertEqual(summary["overall"], {"games": 3, "wins": 1, "losses": 2, "win_rate": 33.3})
        self.assertEqual(summary["versions"]["V2.1"]["win_rate"], 50.0)
        self.assertEqual(summary["archetypes"]["aggro"]["games"], 2)
        self.assertEqual(summary["mana_issues"]["color_screw_white"], 1)


if __name__ == "__main__":
    unittest.main()
