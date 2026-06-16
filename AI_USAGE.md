# AI Usage Evaluation Note

This document outlines the collaborative engineering workflow between the development team and artificial intelligence assistants (Google Gemini / ChatGPT) used during the building of the **Backup Verification Simulator**.

---

## 1. What AI Helped With (Accelerated Development)

AI assistants were utilized as force multipliers to accelerate boilerplate generation, layout prototyping, and complex API schema mapping across the following modules:

* **Streamlit UI Layout Design (`main.py`):** AI helped establish the basic structure for session state management (`st.session_state`) ensuring that dynamically generated validation outputs and PDF download triggers did not cause disruptive screen refreshes.
* **Pydantic Structured Output Schemas (`app/verifier.py`):** The AI generated the rigorous Pydantic baseline schemas needed to enforce clean JSON syntax arrays from the Gemini 2.5 Flash API endpoint, saving significant manual structuring time.
* **ReportLab Document Prototyping (`app/pdf_generator.py`):** Generating multi-page flowables, custom table formatting layouts, and canvas-based header/footer boundaries via the ReportLab Platypus library was heavily streamlined using AI boilerplate generation.

---

## 2. What AI Got Wrong (Engineering Overrides & Corrections)

While highly efficient, the AI introduced critical logical fallacies and architectural bugs that required deep code interventions and structural rewrites:

* **The Deprecated API Syntax Bug:** The AI consistently hallucinated and generated deprecated legacy syntax for the `google-genai` SDK interface. It repeatedly failed to correctly map structured JSON schema requirements using the newest generation client libraries, requiring the team to manually refactor the API call wrappers using the latest official documentation.
* **ReportLab Layout Overflows:** In `app/pdf_generator.py`, the AI-generated styling script constantly triggered catastrophic layout crashes (`LayoutFailure: Spacer height too large`) when long SQL query strings were printed. The team had to override the design with automated text wrap wrappers and paragraph styles.
* **Stateful Streamlit Triggers:** The AI initially drafted a completely stateless design where generating a new backup deleted previously validated results from the dashboard. The team completely rewrote the execution path to enforce an immutable backend session cache layer.

---

## 3. Best Prompts Used (Prompt Engineering Catalog)

### Core Prompt 1: Orchestrating the Dynamic SQL Generation Schema (Two-Pass Validation)
> **Context:** Sent to the LLM to initialize the code-generation agent logic.
> **Prompt:** > "You are an elite database reliability engineer. I am going to pass you a JSON representation of an arbitrary SQLite schema fetched from `sqlite_master`. Your goal is to analyze the tables and columns, look for data relationships (such as transactions matching to users), and generate an array of strict validation queries checking for common silent anomalies: orphaned records, negative financial amounts, or duplicate unique fields. You must strictly output this data conforming to the following structure..."

### Core Prompt 2: Context-Aware Anomaly Summarization
> **Context:** Sent to the LLM during the second pass execution layer.
> **Prompt:**
> "Review the attached execution array containing raw SQL outputs and database runtime exceptions from our sandbox runtime testing. Synthesize these engineering findings into a professional, human-readable executive overview. If empty rows or schema mismatches are present, flag the severity as CRITICAL, highlight the exact failure root cause, and draft an incident summary narrative suitable for engineering alert logs."