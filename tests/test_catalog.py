import unittest
from pathlib import Path

from aegisforge.catalog import discover_skills


ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    def test_catalog_is_sorted_and_has_core_fields(self):
        skills = discover_skills(ROOT)
        self.assertGreaterEqual(len(skills), 10)
        self.assertEqual(skills, sorted(skills, key=lambda item: item["path"]))
        for skill in skills:
            self.assertTrue(skill["name"])
            self.assertTrue(skill["description"])
            self.assertTrue(skill["family"])
            self.assertTrue(skill["path"].startswith("skills/"))


if __name__ == "__main__":
    unittest.main()
