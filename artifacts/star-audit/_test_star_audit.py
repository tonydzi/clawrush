"""Тест star_audit.py на синтетике, без сети. Запуск: python3 -m unittest _test_star_audit"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import star_audit as sa  # noqa: E402

BOT = {"public_repos": 0, "followers": 0, "following": 0, "bio": None, "blog": "",
       "company": None, "location": None, "name": None, "created_at": "2024-07-01T00:00:00Z"}
HUMAN = {"public_repos": 25, "followers": 40, "following": 10, "bio": "dev", "blog": "",
         "company": None, "location": "Lisbon", "name": "Ana", "created_at": "2015-03-01T00:00:00Z"}


class T(unittest.TestCase):
    def test_bot_is_suspect(self):
        sig = sa.user_signals(BOT, "2024-07-05T10:00:00Z")
        self.assertEqual(len(sig), 5)
        self.assertTrue(sa.is_suspect(sig))

    def test_human_is_clean(self):
        sig = sa.user_signals(HUMAN, "2024-07-05T10:00:00Z")
        self.assertEqual(sig, [])
        self.assertFalse(sa.is_suspect(sig))

    def test_burst_found(self):
        ts = ["2024-07-0{}T1{}:00:00Z".format(d, h) for d in range(1, 8) for h in range(3)]
        ts += ["2024-07-09T05:{:02d}:00Z".format(m) for m in range(40)]
        b = sa.find_bursts(ts)
        self.assertEqual(b[0], ("2024-07-09 05:00", 40))

    def test_no_burst_when_flat(self):
        ts = ["2024-07-{:02d}T10:00:00Z".format(d) for d in range(1, 29)]
        self.assertEqual(sa.find_bursts(ts), [])

    def test_verdict_levels(self):
        self.assertTrue(sa.verdict(5, 5, []).startswith("не могу судить"))
        self.assertTrue(sa.verdict(50, 30, []).startswith("красный"))
        self.assertTrue(sa.verdict(50, 10, []).startswith("жёлтый"))
        self.assertTrue(sa.verdict(50, 2, []).startswith("зелёный"))


if __name__ == "__main__":
    unittest.main()
