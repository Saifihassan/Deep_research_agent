# Deep Research Agent

Lightweight agent pipeline that plans web searches, runs searches, composes a written report, and can send the report by email.

Features
- Planner agent: generates a list of web search terms for a query.
- Search agent: performs web searches (DuckDuckGo) and summarizes results.
- Writer agent: synthesizes a final report from search results (schema-validated).
- Email sender: sends the report via the Resend API (optional).
- Minimal Gradio UI (optional) for running the workflow from a web interface.

Quick start
1. Create a virtual environment and activate it:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example and fill in your keys:

```bash
cp .env.example .env
# then edit .env and add real API keys
```

Required environment variables (see `.env.example`):
- `GROQ_API_KEY`, `GROQ_BASE_URL`
- `GEMINI_API_KEY`, `GEMINI_BASE_URL`
- `OLLAMA_API_KEY`, `OLLAMA_BASE_URL`
- `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`
- `RESEND_APIKEY` (for email sending)
- Optional: `EMAIL_FROM`, `OPENAI_DEBUG`, `OAICLIENT_DEBUG`

Usage
- Run the pipeline from the command line:

```bash
python main.py
```

- Launch the minimal Gradio UI (if present):

```bash
python ui.py
```

Project structure
- `main.py` — orchestration and async workflow functions: `plan_searches`, `perform_Searches`, `search`, `write_report`, `emailsender`.
- `ai_agents.py` — agent and tool definitions, model clients, and Pydantic schemas (`WebSearchTerm`, `WebSearchPlan`, `reportSchema`).
- `ui.py` — minimal Gradio UI to run the workflow interactively.
- `requirements.txt` — Python dependencies.
- `.env.example` — template environment variables (copy to `.env`).
- `PROJECT_SUMMARY.txt` — human-readable summary of project structure and tips.

Troubleshooting
- Parsing errors when generating reports: the writer agent is configured to return JSON that matches `reportSchema`. If the model wraps its JSON in Markdown fences (```json ... ```), the agents runtime will raise a parsing error. To mitigate:
  - Ensure `writer_agent` instructions request strictly raw JSON output (no backticks or surrounding text).
  - Reduce model randomness (temperature) for the writer agent.
  - A sanitizer fallback is included in `main.write_report()` to extract JSON from code fences when possible.

- Missing API keys or incorrect base URLs will raise client initialization errors. Check `.env` and ensure the corresponding variables are set.

Security
- Do not commit `.env` or secrets to version control. `.gitignore` excludes `.env` and common secrets.

Next improvements (suggested)
- Harden model-output handling: stricter instructions + deterministic generation.
- Add logging/tracing to capture raw model responses for debugging.
- Improve the UI to show live progress and full report download.

License
- No license specified. Add a `LICENSE` file if you intend to open-source this project.

Contact
- For questions about this workspace, inspect `PROJECT_SUMMARY.txt` or open issues in the repo where this project is hosted.
