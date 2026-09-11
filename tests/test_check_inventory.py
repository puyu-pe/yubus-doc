import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.build_production import production_url
from scripts.check_inventory import check, local_targets, nav_paths, validate_inventory
from scripts.source_config import source_dir


VALID_INVENTORY = """version: 1
review_status: inventory_only
review_note: Navigation coverage only.
pages:
  - id: home
    path: index.md
    status: registered
    reviewed: false
"""


class InventoryCheckTest(unittest.TestCase):
    def test_nav_paths_flattens_nested_navigation(self):
        self.assertEqual(nav_paths([{"Group": [{"Page": "page.md"}]}]), ["page.md"])

    def test_check_rejects_invalid_navigation_value(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "documentation").mkdir()
            (root / "mkdocs.yml").write_text("nav:\n  - Group: 42\n", encoding="utf-8")
            (root / "documentation/inventory.yml").write_text(VALID_INVENTORY, encoding="utf-8")
            self.assertIn("Unsupported navigation value: 42", check(root))

    def test_local_targets_ignores_external_and_anchors(self):
        targets = local_targets("[local](page.md) ![image](img/example.png) [web](https://example.test) [jump](#here)")
        self.assertEqual(targets, ["page.md", "img/example.png"])

    def test_check_reports_missing_navigation_target(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "documentation").mkdir()
            (root / "mkdocs.yml").write_text("nav:\n  - Missing: missing.md\n", encoding="utf-8")
            (root / "documentation/inventory.yml").write_text(
                VALID_INVENTORY.replace("index.md", "missing.md"), encoding="utf-8"
            )
            self.assertIn("navigation target does not exist: missing.md", check(root))

    def test_check_reports_missing_image(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "documentation").mkdir()
            (root / "docs/index.md").write_text("![missing](img/missing.png)\n", encoding="utf-8")
            (root / "mkdocs.yml").write_text("nav:\n  - Home: index.md\n", encoding="utf-8")
            (root / "documentation/inventory.yml").write_text(VALID_INVENTORY, encoding="utf-8")
            self.assertIn("index.md has a missing local reference: img/missing.png", check(root))

    def test_check_reports_missing_local_anchor(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "documentation").mkdir()
            (root / "docs/index.md").write_text("[missing](#missing)\n", encoding="utf-8")
            (root / "mkdocs.yml").write_text("nav:\n  - Home: index.md\n", encoding="utf-8")
            (root / "documentation/inventory.yml").write_text(VALID_INVENTORY, encoding="utf-8")
            self.assertIn("index.md has a missing local anchor: #missing", check(root))

    def test_inventory_contract_rejects_invalid_page_fields_and_duplicate_ids(self):
        inventory = {
            "version": 1,
            "review_status": "inventory_only",
            "review_note": "Navigation coverage only.",
            "pages": [
                {"id": "same", "path": "index.md", "status": "registered", "reviewed": False},
                {"id": "same", "path": "../outside.md", "status": "registered", "reviewed": "no"},
            ],
        }
        errors = validate_inventory(inventory)
        self.assertIn("inventory contains duplicate page ids", errors)
        self.assertIn("inventory page 2 path must be a safe relative Markdown path", errors)
        self.assertIn("inventory page 2 reviewed must be a boolean", errors)

    def test_check_rejects_schema_invalid_inventory_without_custom_validation(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "documentation").mkdir()
            (root / "docs/index.md").write_text("# Home\n", encoding="utf-8")
            (root / "mkdocs.yml").write_text("nav:\n  - Home: index.md\n", encoding="utf-8")
            invalid_inventory = VALID_INVENTORY.replace(
                "pages:\n", "unexpected: value\npages:\n"
            )
            (root / "documentation/inventory.yml").write_text(invalid_inventory, encoding="utf-8")

            with patch("scripts.check_inventory.validate_inventory", return_value=[]):
                errors = check(root)

            self.assertTrue(
                any(error.startswith("inventory schema:") for error in errors),
                errors,
            )

    def test_check_reports_navigation_inventory_mismatch(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "documentation").mkdir()
            (root / "docs/index.md").write_text("# Home\n", encoding="utf-8")
            (root / "mkdocs.yml").write_text("nav:\n  - Home: index.md\n", encoding="utf-8")
            (root / "documentation/inventory.yml").write_text(
                VALID_INVENTORY.replace("index.md", "other.md"), encoding="utf-8"
            )
            self.assertIn("inventory pages must exactly match published navigation", check(root))

    def test_production_url_requires_exact_yubus_manual_path(self):
        self.assertEqual(
            production_url("https://yubus.puyu.pe/manual"),
            "https://yubus.puyu.pe/manual/",
        )
        for value in (
            "http://yubus.puyu.pe/manual/",
            "https://user:pass@yubus.puyu.pe/manual/",
            "https://yubus.puyu.pe:443/manual/",
            "https://yubus.puyu.pe/manual/?preview=true",
            "https://yubus.puyu.pe/manual/#section",
            "https://yubus.puyu.pe/manual%2f",
            "https://yubus.puyu.pe/manual/../manual/",
            "https://yubus.puyu.pe/storage/manual/",
            "https://docs.example.test/manual/",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                production_url(value)

    def test_source_dir_prefers_environment_over_dotenv(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            dotenv_dir = root / "dotenv-source"
            environment_dir = root / "environment-source"
            dotenv_dir.mkdir()
            environment_dir.mkdir()
            (root / ".env").write_text(f"YUBUS_SOURCE_DIR={dotenv_dir}\n", encoding="utf-8")
            self.assertEqual(source_dir(root, {"YUBUS_SOURCE_DIR": str(environment_dir)}), environment_dir)

    def test_source_dir_rejects_invalid_environment_and_dotenv_values(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / ".env").write_text("YUBUS_SOURCE_DIR=relative/source\n", encoding="utf-8")
            self.assertIsNone(source_dir(root, {}))
            self.assertIsNone(source_dir(root, {"YUBUS_SOURCE_DIR": "/does/not/exist"}))
