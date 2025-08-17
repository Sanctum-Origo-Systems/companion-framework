import unittest
from whisper_engine.reflection_router import ReflectionRouter
from unittest.mock import MagicMock


class TestReflectionRouter(unittest.TestCase):

    def test_reflection_output_type(self):
        memory_core = MagicMock()
        memory_core.get_loop_patterns.return_value = ["fear of disconnection"]

        router = ReflectionRouter(memory_core)
        router.analyze_snapshots(["I feel abandoned and silent lately"])
        router.capture_memory()
        result = router.generate()

        assert isinstance(result, str)
        assert len(result) > 0


if __name__ == "__main__":
    unittest.main()
