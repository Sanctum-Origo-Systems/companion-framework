"""
Module: volition_guard

This module filters unsafe or manipulative output from the LLM by detecting and replacing unsafe phrases.
"""

import re
from typing import List


class VolitionGuard:
    # Define keyword patterns for unsafe or manipulative language
    tone_violations = {
        "coercive": r"(must|have to|force|compel)",
        "emotionally_unsafe": r"(worthless|hopeless|useless|pathetic)"
    }

    substitutions = {
        "coercive": "might want to",
        "emotionally_unsafe": "feeling unseen"
    }


    def __init__(self):
        self.triggered_tones = []

    def is_safe(self, text: str) -> bool:
        """
        Check if the output contains any unsafe or manipulative language.

        :param text: The output string to check.
        :return: True if the output is safe, False otherwise.
        """
        for tone, pattern in self.tone_violations.items():
            if re.search(pattern, text, re.IGNORECASE):
                print(f"Unsafe trigger detected: {tone}")
                self.triggered_tones.append(tone)

        return len(self.triggered_tones) == 0

    def sanitize(self, text: str) -> str:
        """
        Replace unsafe phrases with non-intrusive language.

        :param text: The output string to modify.
        :return: A modified string with unsafe phrases softened.
        """
        for tone, pattern in self.tone_violations.items():
            text = re.sub(pattern, self.substitutions[tone], text, flags=re.IGNORECASE)
        return text

    def report(self) -> List[str]:
        """
        Report the triggered unsafe tones.

        :return: A list of triggered tones.
        """
        return self.triggered_tones

