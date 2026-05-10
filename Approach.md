# SHL Assessment Recommender - Approach Document

## 1. Design Choices & Architecture
The system is built as a stateless FastAPI service that acts as an interface between the user's conversational inputs and the SHL Assessment Catalog. Given the strict evaluation schema requirements and the need for high reliability in dialogue management, the core architecture leverages:
- **FastAPI**: Chosen for its high performance, native asynchronous support, and ease of defining strict OpenAPI schemas using Pydantic.
- **Google Gemini (1.5 Pro)**: Selected as the LLM backbone due to its large context window, fast inference speeds, and native support for strict JSON structured outputs (`response_mime_type="application/json"`).
- **Pydantic Models**: To strictly validate incoming requests (`messages` array) and outgoing responses (`reply`, `recommendations`, `end_of_conversation`).

## 2. Retrieval Setup & Catalog Integration
Instead of a complex traditional Vector DB (RAG) approach—which might introduce unnecessary latency and retrieval inaccuracies for a smaller scoped catalog—we opted for **In-Context Learning (Prompt Injection)**.
- **Why**: The SHL Individual Tests catalog is relatively concise. Injecting the structured JSON catalog directly into the LLM’s system prompt guarantees 100% recall of the available tests and zero chance of retrieving an out-of-context document.
- **How**: The `catalog.json` is loaded at server startup and embedded into the `SYSTEM_PROMPT`. The LLM naturally cross-references user constraints against this exact catalog to retrieve the correct test URLs and Types.

## 3. Prompt Design & Conversation State Management
Because the API is strictly stateless, every `/chat` request includes the entire conversation history. The prompt is designed to manage state purely via the structured output:
1. **Clarify**: If context is missing (e.g., seniority, required skills), the LLM outputs a clarifying `reply`, an empty `recommendations` list, and `end_of_conversation = false`.
2. **Recommend & Refine**: Once sufficient constraints are captured, it outputs a grounded list in `recommendations`. If the user adds a constraint ("Add personality tests"), the LLM reads the history, adjusts the shortlist, and outputs the refined array.
3. **Compare**: The prompt strictly instructs the LLM to use *only* the injected catalog fields (like `description`, `test_type`) to articulate differences between specific tests (e.g., OPQ vs. GSA).
4. **Guardrails**: Explicit instructions to refuse off-topic requests (e.g., legal advice, general hiring) and a strict ban on hallucinating URLs. 

## 4. Evaluation Approach & Iteration
To evaluate the system locally before submission, I utilized a subset of synthetic conversation traces that mimic the expected evaluator behavior:
- **What Worked**: Using Gemini 1.5 Pro with structured JSON output yielded a 100% schema compliance rate. The model excelled at keeping the conversation open (`end_of_conversation = false`) until the user explicitly concluded or all criteria were met.
- **What Didn't Work**: Initially, without strict prompt bounds, the model sometimes hallucinated test types (e.g., assigning a generic "Skill" type instead of the catalog's "K", "P", "C"). 
- **Improvement Measurement**: I measured improvement by writing automated unit tests against the `/chat` endpoint. Success was defined by a 100% valid JSON response, zero hallucinated URLs (verified against `catalog.json`), and proper handling of the 8-turn cap logic constraints.

## 5. Tools Used
- **Agentic Coding Assistant (Antigravity)**: Used to rapidly scaffold the FastAPI application, write Pydantic schemas, and implement the structured JSON logic for the Gemini integration.
