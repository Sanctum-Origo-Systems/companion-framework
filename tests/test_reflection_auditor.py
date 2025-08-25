import unittest
from whisper_engine.alignment.reflection_auditor import ReflectionAuditor


class TestReflectionAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = ReflectionAuditor()

    def test_poetic_response_high_alignment(self):
        text = (
            "Something restless lives beneath your skin,\n"
            "doesn't it?\n\n"
            "A stirring that has no name,\n"
            "just this persistent pulse\n"
            "that won't let you settle."
        )
        result = self.auditor.analyze(text)
        self.assertEqual(result["poetic_alignment"], "high")
        self.assertGreaterEqual(result["fidelity_score"], 0.5)

    def test_moderate_alignment_due_to_high_structure(self):
        text = (
            "You seem uncertain. Maybe it's time to reconsider what you want. "
            "Not everything that's quiet is peace. Some of it is avoidance."
        )
        result = self.auditor.analyze(text)
        self.assertEqual(result["poetic_alignment"], "high")
        self.assertNotIn("high structural resonance (line breaks)", result["violations"])

    def test_low_alignment_due_to_verbosity(self):
        text = "This is a very long message " + "that just keeps going and going " * 30
        result = self.auditor.analyze(text)
        self.assertEqual(result["poetic_alignment"], "low")
        self.assertTrue("overly verbose" in result["violations"])

    def test_edge_case_empty_input(self):
        text = ""
        result = self.auditor.analyze(text)
        self.assertEqual(result["poetic_alignment"], "low")
        self.assertEqual(result["fidelity_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
