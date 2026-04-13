"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.

Note: All exercises use Llama 3.3 70B Instruct via the Nebius API. Results may differ if you used a different model.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = ["check_pub_availability", "get_edinburgh_weather",
                       "calculate_catering_cost", "generate_event_flyer"]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

TASK_A_NOTES = """Fixed two issues in research_agent.py: (1) The tool call parsing loop only checked for Anthropic-style content blocks (type==tool_use) but we use ChatOpenAI (OpenAI-compatible API), which stores tool calls in m.tool_calls attribute instead. Added a hasattr check to extract them.
(2) The LLM was outputting tool calls as raw JSON text in its content instead of using the structured tool-calling API. Added system prompt instructions to keep the model in proper tool-calling mode.
Note: All exercises use Llama 3.3 70B Instruct via the Nebius API. Results may differ if you used a different model."""

# optional — anything unexpected

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True
# True or False

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-b455c3f3-9c65-44f9-9318-2d5546520a1a_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """The Bow Bar was initially checked for availability but did not meet the requirements due to insufficient capacity (80) and full status. 
The agent then immediately pivoted to check The Albanach, which met all constraints with capacity 180, vegan options available, and status available, confirming it as the fallback venue."""


SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = "Unfortunately, none of the known venues meet the requirements of 300 people with vegan options."

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "I am not able to execute this task as it exceeds the limitations of the functions I have been given."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """The agent's refusal would be acceptable in a real booking assistant. 
It correctly identified that finding train departure times falls outside the scope of its available tools and explicitly stated this rather than hallucinating an answer. 
A booking assistant should not fabricate schedule information it has no access to, and clear refusal prevents misinformation.
It clearly specifies that it exceeds the limitations of its functions, which is a reasonable response."""


# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        agent(agent)
        tools(tools)
        __end__([<p>__end__</p>]):::last
        __start__ --> agent;
        agent -.-> __end__;
        agent -.-> tools;
        tools --> agent;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """The LangGraph Mermaid graph shows a single loop: 
__start__ feeds the agent node, which can call tools or end — the path is decided by the LLM at runtime on every step. 
flows.yml defines two fully explicit flows (confirm_booking and handle_out_of_scope) with fixed ordered steps: guest_count collected first, then vegan_count, then deposit, then action_validate_booking runs. 
In LangGraph the model decides every step; in Rasa CALM the model only picks which flow triggers, and everything after is deterministic."""


# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most surprising behaviour was in TASK C / Scenario 1 — First Choice Unavailable where after The Bow Bar returned meets_all_constraints: false.
The agent immediately called check_pub_availability for The Albanach on the very next turn, selecting which venue to try next from its own reasoning rather than from scripted steps. 
It then went further than the task required by also checking weather, calculating catering and generating a flyer entirely on its own.
The flyer can be found at: https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-30bc773c-51ad-430b-a8d4-ea490e8a4ca2_00001_.webp"""
