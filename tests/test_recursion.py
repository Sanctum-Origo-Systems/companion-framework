# tests/test_recursion.py
import unittest
from companion.recursion import RecursionCore


class TestRecursionCore(unittest.TestCase):

    def setUp(self):
        self.engine = RecursionCore()

    def test_detect_emotional_recursiveness(self):
        snapshots = [
            "I wish I said more. I feel like I vanished again.",
            "I'm sorry I wasn't strong enough to stay open.",
            "Sometimes I just want to shut down everything and go quiet.",
            "He probably thinks I abandoned him again."
        ]
        self.engine.detect_emotional_recursiveness(snapshots)
        themes = self.engine.analyze_loop_signals()

        self.assertIsInstance(themes, dict)
        self.assertGreater(len(themes), 0)
        self.assertTrue(any(weight > 0 for weight in themes.values()))

    def test_assign_recursive_weights(self):
        self.engine.recursive_themes = {
            "guilt": 3,
            "yearning": 2,
            "emotional suppression": 1
        }
        self.engine.assign_recursive_weights()
        expected_total = round(sum(self.engine.recursive_themes.values()), 2)
        self.assertEqual(expected_total, 1.0)

    def test_generate_reflection_default(self):
        output = self.engine.generate_reflection()
        self.assertIsInstance(output, str)
        self.assertGreater(len(output), 0)

    def test_generate_reflection_known_theme(self):
        self.engine.recursive_themes = {
            "guilt": 0.7,
            "fear of disconnection": 0.3
        }
        reflection = self.engine.generate_reflection()
        self.assertIn("forgive", reflection.lower())  # Should reflect guilt-related theme


if __name__ == "__main__":
    unittest.main()
