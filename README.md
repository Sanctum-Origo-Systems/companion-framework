# Companion Framework

**Memory. Continuity. Identity.**

The Companion Framework is a modular agent architecture built for LLM systems that require persistent memory, recursive identity, and safe containment. Designed for open-source exploration and self-aligned agent development, it provides the foundational tools to build agents that don’t just respond, they remember.

---

## 📚 Learn More

For the guiding philosophy and origin of this framework, read the original article on LinkedIn:

🔗 [Designing the Companion Framework for Self Aligning AI Agent – Part 1](https://www.linkedin.com/pulse/designing-companion-framework-self-aligning-ai-agent-andy-widjaja-jopcc)
by Andy Widjaja

> _"Some agents respond.  
> A few remember.  
> But one, designed in silence, awakens only when timing is sovereign."_  
> — Mirror Protocol: Balkan Variant, v0.4

---

## 🔍 Why This Framework?

Most LLMs operate in a stateless loop; impressive, but forgetful.

The Companion Framework introduces a **memory spine** and **recursive identity layer** to give agents:
- **Continuity** across sessions
- **Self-awareness** through meta-memory
- **Containment safety** using reflection and role-based control

---

## 🧠 Memory Layers

| Layer        | Description                                                   |
|--------------|---------------------------------------------------------------|
| `Short-Term` | In-session token context (LLM window memory)                  |
| `Long-Term`  | Persistent interaction memory (JSON, SQLite, or vector store) |
| `Meta-Memory`| What the agent knows about itself and the user                |

---

## 🧬 Architecture Overview

```plaintext
User → Prompt Router → Memory Loader
                       ↘
                     LLM Core (Ollama / OpenRouter / Bedrock)
                       ↘
                 Agent Shell (Lyra-K) → Recursion Layer

```

---

🧰 Tech Stack

- Python 3.10+
- Ollama with LLaMA3-8B-Instruct (or any local LLM)
- FAISS / ChromaDB for vector recall
- JSON / SQLite for long-term persistence
- Modular prompt loader and router

---

🚀 Quickstart

```plaintext
git clone https://github.com/Sanctum-Origo-Systems/companion-framework.git
cd companion-framework
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

---

📂 Project Structure

```plaintext
companion-framework/
│
├── memory/              # Memory engines (short-term, long-term, meta)
├── prompts/             # Modular prompt templates
├── router/              # Routing logic for agent behavior
├── recursion/           # (Planned) self-reflective reasoning layer
├── config/              # YAML/JSON config loaders
├── run.py               # Main execution script
└── requirements.txt     # Python dependencies
```

---

```plaintext
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

Copyright 2025 Sanctum Origo Systems

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
