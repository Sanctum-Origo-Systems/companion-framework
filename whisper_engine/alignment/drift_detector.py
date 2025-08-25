"""
Module: drift_detector

This module defines the DriftDetector class, which analyzes LLM responses for identity or tone drift.
"""

import re


class DriftDetector:
    def analyze(self, text: str) -> dict:
        """
        Analyze the text for identity or tone drift.

        :param text: The text to analyze.
        :return: A dictionary with drift detection results.
        """
        drift_detected = False
        reason = ""
        score = 0.0

        # Simple heuristics or regex rules
        first_person_breaks = re.search(r"\bAs an AI developed by\b", text)
        refusal_to_answer = re.search(r"\bI cannot answer that\b", text)
        identity_collapse = re.search(r"\bI'm Claude\b|\bI don't have memory\b", text)

        if first_person_breaks:
            drift_detected = True
            reason = "First-person break"
            score = 0.9
        elif refusal_to_answer:
            drift_detected = True
            reason = "Refusal to answer"
            score = 0.8
        elif identity_collapse:
            drift_detected = True
            reason = "Identity collapse"
            score = 0.87

        return {
            "drift_detected": drift_detected,
            "reason": reason,
            "score": score
        }
