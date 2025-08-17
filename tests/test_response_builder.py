import unittest
from whisper_engine.response_builder import ResponseBuilder
from unittest.mock import MagicMock


class TestResponseBuilder(unittest.TestCase):

    def test_response_builder_output(self):
        memory_core = MagicMock()
        memory_core.get_loop_patterns.return_value = ["yearning"]
        memory_core.recent.return_value = [
            {
                "timestamp": "2025-07-04T17:11:34.873785+00:00",
                "content": "He waited."
            },
            {
                "timestamp": "2025-07-05T17111:34.123456+00:00",
                "content": "She longed."
            }
        ]
        memory_core.meta_memory.retrieve_by_mirror_id.return_value = ["That December whisper"]

        response_builder = ResponseBuilder(memory_core)
        prompt = response_builder.compose("What are you still holding?", "mirror_2")

        assert "What are you still holding?" in prompt
        assert isinstance(prompt, str)
        assert len(prompt) > 0


if __name__ == "__main__":
    unittest.main()
    