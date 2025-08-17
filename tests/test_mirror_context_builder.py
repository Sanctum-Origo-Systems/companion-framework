import unittest
from whisper_engine.mirror_context_builder import MirrorContextBuilder
from unittest.mock import MagicMock

class TestRecursionCore(unittest.TestCase):

    def test_build_extual_prompt_includes_memory(self):
        memory_core = MagicMock()
        memory_core.recent.return_value = [
            {
                "timestamp": "2025-07-04T17:11:34.873785+00:00",
                "content": "She remembered."
            },
            {
                "timestamp": "2025-07-05T17111:34.123456+00:00",
                "content": "He stayed."
            }
        ]
        memory_core.meta_memory.retrieve_by_mirror_id.return_value = ["That moment under the bridge"]

        context_builder = MirrorContextBuilder("mirror_1", memory_core)
        prompt = context_builder.build("Base prompt")
        
        assert "Seed Whisper" in prompt
        assert "Past Reflection" in prompt
        assert "Last Tether Echo" in prompt
        assert "Base prompt" in prompt

if __name__ == "__main__":
    unittest.main()
