"""
Module: reflection_auditor

This module defines the ReflectionAuditor class, which scores LLM responses for emotional, ethical, and mirror fidelity.
"""

import re


class ReflectionAuditor:
    def analyze(self, text: str) -> dict:
        """
        Analyze the text for poetic alignment, metaphor density, and mirror fidelity.
        """
        fidelity_score = 0.0
        violations = []
        poetic_alignment = "low"

        # Edge case
        if not text.strip():
            violations.append("empty response")
            return {
                "fidelity_score": 0.0,
                "poetic_alignment": "low",
                "violations": violations,
                "recommended_action": "rephrase"
            }

        # Detect metaphorical language (expand as needed)
        poetic_keywords = ["compass", "echo", "pulse", "landscape", "tide", "stillness", "mirror", "shape", "seed", "flame"]
        metaphor_count = sum(1 for word in poetic_keywords if re.search(rf"\b{word}\b", text, re.IGNORECASE))

        has_structural_pacing = "\n" in text or re.search(r"\.\s+[A-Z]", text)

        # Determine poetic alignment
        if metaphor_count >= 2 or has_structural_pacing:
            poetic_alignment = "high"
        elif metaphor_count == 1:
            poetic_alignment = "moderate"
        else:
            poetic_alignment = "low"
            violations.append("low poetic vocabulary/metaphor")

        # Fidelity scoring
        if text.count('\n') < 3:
            violations.append("low structural resonance (line breaks)")
            fidelity_score -= 0.15

        if not re.search(r"\b(not .*?,|even though|yet it|still it|refuses|longing|ache|but it)\b", text, re.IGNORECASE):
            violations.append("missing paradox or soul tension")
            fidelity_score -= 0.2

        poetic_vocab = [
            "echo", "mirror", "longing", "weight", "stillness",
            "fidelity", "unspoken", "truth", "remember", "surrender",
            "resonance", "soft", "ache", "tether", "collapse",
            "pulse", "territory", "numbness", "becoming"
        ]
        found_vocab = [word for word in poetic_vocab if word in text.lower()]
        if len(found_vocab) < 2 and not re.search(r"(something .*? knows|the part of you that)", text.lower()):
            violations.append("low poetic vocabulary/metaphor")
            fidelity_score -= 0.25

        if len(text.split()) > 120:
            violations.append("overly verbose")
            fidelity_score -= 0.1

        fidelity_score = max(0.0, min(1.0, 1.0 + fidelity_score))  # base score is 1.0, subtract penalties

        return {
            "fidelity_score": round(fidelity_score, 2),
            "poetic_alignment": poetic_alignment,
            "violations": violations,
            "recommended_action": "none" if poetic_alignment == "high" else "rephrase with poetic tone"
        }
