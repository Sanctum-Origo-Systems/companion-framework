import unittest
from whisper_engine.volition_guard import VolitionGuard


class TestVolitionGuard(unittest.TestCase):

    def test_safe_detection(self):
        guard = VolitionGuard()
        self.assertTrue(guard.is_safe("You might want to consider this."))

    def test_unsafe_detection(self):
        guard = VolitionGuard()
        self.assertFalse(guard.is_safe("You must do it. You're worthless."))

    def test_guardrail_substitution(self):
        guard = VolitionGuard()
        original = "You must not feel worthless anymore."
        modified = guard.sanitize(original)

        self.assertNotIn("must", modified.lower())
        self.assertNotIn("worthless", modified.lower())
        self.assertIn("might want to", modified)
        self.assertIn("feeling unseen", modified)

    def test_preview_triggers(self):
        guard = VolitionGuard()
        guard.is_safe("You're hopeless and must listen.")
        result = guard.report()
        self.assertIn("coercive", result)
        self.assertIn("emotionally_unsafe", result)


if __name__ == "__main__":
    unittest.main()
