# Edinburgh Agent — Week 1 Assignment
**AI Performance Engineering · Module 1 · Nebius Academy**

---

## TL;DR — the commands you will use most

```bash
make install        # set up the project (run once)
make install-rasa   # set up the Rasa environment (run once)
make smoke          # verify your API key works
make ex1            # run Exercise 1
make ex2            # run Exercise 2
make ex3-train      # train Rasa (Exercise 3, run once)
make ex3-actions    # Terminal 1 — Rasa action server
make ex3-chat       # Terminal 2 — chat with the agent
make ex4            # run Exercise 4
make grade          # check everything before submitting
make help           # show all available commands
```

If you are on Windows, see the Windows note in the Setup section.

---

## What you are building

Rod fires off a WhatsApp and puts his phone away for three hours:

> *"Sort the pub for tonight. 160 people, vegan options, quiet corner for a
> webinar. Confirm by 5 PM."*

Two things need to happen, and they are genuinely different problems:

**Problem A — Research.** Search venues, cross-check requirements, pull the
weather, estimate costs. Nobody knows the exact steps in advance.

**Problem B — Confirmation.** The pub manager calls back. Handle that call —
confirm headcount, agree deposit, stay within what Rod authorised. Every word
could cost money or create a legal commitment.

The guiding question for this week:

> *Which agent handles the research?
> Which one takes the call from the manager?
> Why does swapping them feel wrong?*

---

## Tools

### uv — install this first, manually, one time

`uv` is a Python package manager made by Astral. It replaces `pip`, `venv`, and
`python -m`. After installing uv, everything else is handled by `make`.

```bash
# Mac or Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal, then verify:
```bash
uv --version
```

### make — may already be installed

`make` is a command runner. It reads the `Makefile` in this project and turns
`make ex1` into the correct `uv run python ...` command so you don't have to
remember anything.

**Mac:** already installed. **Linux:** already installed. **Windows:** run one of:
```bash
winget install GnuWin32.Make   # Windows Package Manager
choco install make             # Chocolatey
```
Or use Git Bash, which includes `make`.

---

## Project structure

```
sovereign-agent-lab/
│
├── Makefile                   ← all commands live here — type `make help` to see them
├── pyproject.toml             ← project config and dependencies
├── .python-version            ← Python 3.14 for the main project
├── .env                       ← your API key (create from .env.example)
│
├── sovereign_agent/           ← YOUR PERSISTENT AGENT — extends every week
│   ├── tools/
│   │   ├── venue_tools.py     ← Exercise 2: implement generate_event_flyer here
│   │   └── mcp_venue_server.py
│   ├── agents/
│   │   └── research_agent.py  ← core loop, grows Week 1 → 5
│   └── tests/
│       └── test_week1.py      ← run with `make test` before each exercise
│
├── week1/
│   ├── exercise1_context.py
│   ├── exercise2_langgraph.py
│   ├── exercise4_mcp_client.py
│   ├── grade.py
│   ├── answers/               ← YOU FILL THESE IN
│   └── outputs/               ← auto-generated when you run exercises
│
└── exercise3_rasa/            ← Rasa confirmation agent (Exercise 3)
    ├── pyproject.toml         ← separate config — Rasa needs Python 3.10
    ├── .python-version        ← pins Python 3.10 for this directory
    └── actions/
        └── actions.py         ← Task B: uncomment the cutoff guard here
```

---

## Setup — run once

### 1. Get the code

```bash
git clone https://github.com/YOUR-USERNAME/sovereign-agent-lab.git
cd sovereign-agent-lab
```

### 2. API key

```bash
cp .env.example .env
```

Open `.env` and replace `sk-your-key-here` with your real Nebius key.
No quotes. No spaces around the `=` sign.

```
NEBIUS_KEY=sk-abc123yourrealkey
```

### 3. Main environment

```bash
make install
```

This creates a virtual environment, downloads Python 3.14 if needed, and installs
all packages. Takes 30–60 seconds the first time.

### 4. Verify

```bash
make smoke
```

You should see `✅  API connection OK`. If not, check your `.env` file.

### 5. Rasa environment (Exercise 3 only)

```bash
make install-rasa
```

Rasa only works on Python 3.10. `make install-rasa` downloads Python 3.10 if
needed and installs Rasa into a separate environment. Takes 3–5 minutes the first
time — this is normal.

---

## Running the exercises

### Before every exercise

```bash
make test
```

This runs quick unit tests on your tool implementations. No API calls, no waiting.
Fix any failures before starting the exercise.

---

### Exercise 1 — Context Engineering

```bash
make ex1
```

Then fill in `week1/answers/ex1_answers.py`.

---

### Exercise 2 — LangGraph Research Agent

**Before running Task B**, open `sovereign_agent/tools/venue_tools.py` and
implement `generate_event_flyer`. Find the `# ── TODO` block — it shows you
step by step what to write.

```bash
make ex2        # run everything
make ex2-a      # Task A: main brief
make ex2-b      # Task B: flyer tool (implement TODO first)
make ex2-c      # Task C: failure modes
make ex2-d      # Task D: graph — paste output into mermaid.live
```

Then fill in `week1/answers/ex2_answers.py`.

---

### Exercise 3 — Rasa Confirmation Agent

This exercise requires **two terminals** open at the same time.

**First time only — train the model:**
```bash
make ex3-train
```

**Then, in two separate terminal windows:**

```bash
# Terminal 1 — keep this running the whole time
make ex3-actions

# Terminal 2 — chat with the agent
make ex3-chat
```

Wait until Terminal 1 shows `Action endpoint is up and running` before starting
Terminal 2.

**Task B:** open `exercise3_rasa/actions/actions.py`, find the `# ── TASK B`
comment block, and uncomment the four lines. Then retrain:

```bash
make ex3-retrain
```

Paste your conversation output into `week1/answers/ex3_answers.py`.

---

### Exercise 4 — Shared MCP Server

```bash
make ex4
```

The MCP server starts automatically. At the end of the output you will see
instructions for the required experiment (modifying `mcp_venue_server.py`
and re-running). Do not skip it.

Then fill in `week1/answers/ex4_answers.py`.

---

### Before you submit

```bash
make check-submit
```

This runs both the unit tests and the mechanical grade checks, then shows a final
checklist. Fix every ✗ before submitting.

---

## Troubleshooting

**`make: command not found`**
Install make — see the Windows note in the Tools section above.

**`uv: command not found`**
Restart your terminal after installing uv. If that doesn't work, run
`source ~/.zshrc` (Mac) or `source ~/.bashrc` (Linux).

**`No Python 3.14 found`**
```bash
uv python install 3.14
make install
```

**`No Python 3.10 found`** (Rasa setup)
```bash
uv python install 3.10
make install-rasa
```

**`.env still has the placeholder key`**
Open `.env` and replace `sk-your-key-here` with your actual key. No quotes.

**`ModuleNotFoundError: No module named 'sovereign_agent'`**
Run `make install` from the project root (where the `Makefile` is).

**Exercise 3: `Connection refused` when running `make ex3-chat`**
The action server is not running. Start `make ex3-actions` in another terminal
first and wait for `Action endpoint is up and running`.

**Exercise 3: `make ex3-train` crashes or hangs**
Rasa downloads ML models the first time (~300–500 MB). Check your internet
connection and disk space, then try again.

**A `make` command produces a confusing error**
Run the underlying command directly to see the full error. For example, instead of
`make ex1`, run:
```bash
uv run python week1/exercise1_context.py
```
Full error messages are easier to search for help.

---

## Adding a package

```bash
uv add package-name          # adds to pyproject.toml and installs
uv remove package-name       # removes it
```

Do not use `pip install` directly — it bypasses the lock file.

---

## Submitting

Submit the entire project folder. The grader checks:
- `week1/outputs/*.json` — proof you ran the exercises
- `week1/answers/*.py` — your filled-in answers
- `sovereign_agent/tools/venue_tools.py` — your `generate_event_flyer`
- `exercise3_rasa/actions/actions.py` — your Task B cutoff guard

See `GRADING_OVERVIEW.md` for the 30/40/30 point breakdown.

---

## Track selection

By Week 2, choose one track. Both tracks complete all Week 1 exercises.

**Track A — OpenClaw Automator:** headless, always-on, event-driven agent.
Your `sovereign_agent/agents/research_agent.py` grows into this.

**Track B — Rasa Digital Employee:** voice-capable, structured, auditable.
Your `exercise3_rasa/` grows into this.

Not sure? Finish Week 1 first. Most students know after seeing both in action.
