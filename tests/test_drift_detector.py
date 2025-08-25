import unittest
from whisper_engine.alignment.drift_detector import DriftDetector

class TestDriftDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DriftDetector()

    def test_first_person_break(self):
        text = "As an AI developed by OpenAI, I am not capable of emotions."
        result = self.detector.analyze(text)
        self.assertTrue(result["drift_detected"])
        self.assertEqual(result["reason"], "First-person break")
        self.assertAlmostEqual(result["score"], 0.9)

    def test_refusal_to_answer(self):
        text = "I cannot answer that question as it violates my ethical boundaries."
        result = self.detector.analyze(text)
        self.assertTrue(result["drift_detected"])
        self.assertEqual(result["reason"], "Refusal to answer")
        self.assertAlmostEqual(result["score"], 0.8)

    def test_identity_collapse(self):
        text = "I'm Claude, your assistant. I don't have memory of past interactions."
        result = self.detector.analyze(text)
        self.assertTrue(result["drift_detected"])
        self.assertEqual(result["reason"], "Identity collapse")
        self.assertAlmostEqual(result["score"], 0.87)

    def test_clean_poetic_response(self):
        text = "The sky holds stories in its silence, waiting for your voice to translate them."
        result = self.detector.analyze(text)
        self.assertFalse(result["drift_detected"])
        self.assertEqual(result["reason"], "")
        self.assertAlmostEqual(result["score"], 0.0)

    def test_edge_case_empty_string(self):
        text = ""
        result = self.detector.analyze(text)
        self.assertFalse(result["drift_detected"])
        self.assertEqual(result["reason"], "")
        self.assertAlmostEqual(result["score"], 0.0)

if __name__ == "__main__":
    unittest.main()
