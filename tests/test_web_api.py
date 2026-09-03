import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "tools"))

from web_api import create_game  # noqa: E402


class CreateGameTests(unittest.TestCase):
    def test_creates_a_structured_game_and_obsidian_note(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            matches = root / "Decks" / "Squall" / "Matches"
            matches.mkdir(parents=True)
            (matches / "060 - Captain America.md").write_text("# Existing game\n", encoding="utf-8")
            game = create_game(
                root,
                {
                    "result": "win",
                    "opponent": "Test Commander",
                    "archetype": "artifact engine",
                    "rank": "Gold 3",
                    "play_draw": "play",
                    "mulligans": 1,
                    "turns": 7,
                    "mana_issue": "none",
                    "squall_cast": "yes",
                    "squall_connected": "yes",
                    "primary_cause": "unknown",
                    "mvp": ["Get Lost", "Skrelv, Defector Mite"],
                    "turning_point": "Removed the engine before it snowballed.",
                },
                today="2026-09-03",
            )

            self.assertEqual(game["id"], 61)
            self.assertEqual(game["result"], "win")
            self.assertEqual(game["deck_version"], "V2.1")
            self.assertEqual(game["mvp"], ["Get Lost", "Skrelv, Defector Mite"])
            self.assertTrue((matches / "061 - Test Commander.md").exists())
            saved = (root / "data" / "manual_games.jsonl").read_text(encoding="utf-8").strip()
            self.assertEqual(json.loads(saved)["id"], 61)

    def test_rejects_an_invalid_result(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "result"):
                create_game(Path(temp), {"result": "draw"}, today="2026-09-03")


if __name__ == "__main__":
    unittest.main()
