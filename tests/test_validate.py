"""Tests for the minimal manifest-overlay policy."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "manifest_validate", ROOT / "validate.py")
VALIDATE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATE)


class ManifestValidationTest(unittest.TestCase):
    def write(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "manifest.xml"
        path.write_text(text, encoding="utf-8")
        return path

    def test_committed_overlay_is_minimal_and_valid(self):
        VALIDATE.validate_overlay()

    def test_floating_project_revision_is_rejected(self):
        path = self.write("""<manifest>
          <remote name="diamaneos" fetch="https://codeberg.org/DiamaneOS/" />
          <project name="device" path="device/fairphone/FP6"
                   remote="diamaneos" revision="refs/heads/main" />
        </manifest>""")
        with self.assertRaisesRegex(VALIDATE.ManifestError,
                                    "exact 40-character commit"):
            VALIDATE.validate_overlay(path)

    def test_upstream_repin_is_rejected(self):
        path = self.write("""<manifest>
          <remote name="diamaneos" fetch="https://codeberg.org/DiamaneOS/" />
          <project name="platform_frameworks_base" path="frameworks/base"
                   remote="grapheneos"
                   revision="1111111111111111111111111111111111111111" />
        </manifest>""")
        with self.assertRaisesRegex(VALIDATE.ManifestError,
                                    "must use the diamaneos remote"):
            VALIDATE.validate_overlay(path)

    def test_duplicate_checkout_path_is_rejected(self):
        path = self.write("""<manifest>
          <remote name="diamaneos" fetch="https://codeberg.org/DiamaneOS/" />
          <project name="one" path="device/fairphone/FP6" remote="diamaneos"
                   revision="1111111111111111111111111111111111111111" />
          <project name="two" path="device/fairphone/FP6" remote="diamaneos"
                   revision="2222222222222222222222222222222222222222" />
        </manifest>""")
        with self.assertRaisesRegex(VALIDATE.ManifestError,
                                    "duplicate project path"):
            VALIDATE.validate_overlay(path)

    def test_resolved_manifest_requires_commits_and_unique_paths(self):
        valid = self.write("""<manifest>
          <project name="a" path="a"
                   revision="1111111111111111111111111111111111111111" />
          <project name="b" path="b"
                   revision="2222222222222222222222222222222222222222" />
        </manifest>""")
        self.assertEqual(2, VALIDATE.validate_resolved(valid))
        floating = self.write("""<manifest>
          <project name="a" path="a" revision="refs/heads/main" />
        </manifest>""")
        with self.assertRaisesRegex(VALIDATE.ManifestError,
                                    "exact 40-character commit"):
            VALIDATE.validate_resolved(floating)


if __name__ == "__main__":
    unittest.main()
