"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER = "No venues were found that can accommodate 300 people and offer vegan options."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Before the change, search_venues(min_capacity=160, requires_vegan=True) returned 2 matches: The Albanach (2 Hunter Square, capacity 180) and The Haymarket Vaults (1 Dalry Road, capacity 160). 
After changing The Albanach's status to 'full' in mcp_venue_server.py, the same query returned only 1 match: The Haymarket Vaults. 
The mcp_venue_server.py file was the only file that needed updating: the agent code, the tool call logic, and the LangGraph client required no changes at all. 
This shows a key MCP property where the data layer is decoupled from the agent layer.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 113   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 0  # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
Exercise 2 required 113 lines of tool implementation code in venue_tools.py that had to be written, maintained, and deployed as part of the agent's own codebase. Every tool change would require touching agent code.
Exercise 4 required 0: the MCP client discovers tools at runtime from the server and never owns any tool logic itself. 
This means tool updates, new venues, or bug fixes in Exercise 4 require no agent redeployment at all. Multiple agents can share a single MCP server simultaneously, always getting current tool definitions and live data.
There was some proof of this in the experiment: changing The Albanach's status to full in mcp_venue_server.py changed what search_venues returned, with zero changes to the agent or client code.
The live data decoupling is what 113 lines gets you when they move to the server side.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- The LangGraph research agent handles open-ended venue discovery as it can chain tool calls adaptively. In Query 1, it called search_venues then followed up with get_venue_details autonomously, without being told to, showing it can reason about what information it needs.
- The Rasa CALM booking agent handles the structured confirmation flow because it enforces a deterministic slot-collection sequence (guest_count, vegan_count, deposit) and applies the £300 deposit cutoff unconditionally via Python, which an LLM agent cannot be relied on.
- The MCP venue server acts as a shared live data layer because changing The Albanach's status to 'full' immediately filtered it from search results without touching any agent code, proving the data layer is fully decoupled from the reasoning layer.
- A routing component directs incoming requests to the correct agent because two agents have non-overlapping strengths. CALM is not able to improvise a follow-up tool call when results are ambiguous, and LangGraph cannot guarantee it will always collect all three slots before checking the deposit limit.
- LangSmith or equivalent observability is placed across both agents as the Exercise 2 trace showed the model made a non-obvious decision to call get_venue_details on The Haymarket Vaults rather than The Albanach, and without the full trace, the reasoning is invisible and not debuggable.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph is better for research and CALM is more suited for the booking call. In Query 1, the LangGraph agent called search_venues, received two matches, and then independently decided to call get_venue details on The Haymarket Vaults, a follow-up reasoning step that was not instructed.
The adaptive chaining is exactly what open-ended researching needs. Swapping CALM for researching would not work because CALM can only follow pre-declared flows and cannot issue an unscripted second tool call based on what the first call returned.
Swapping in LangGraph for the booking confirmation would not work because the deposit cutoff must be deterministic. In Exercise 3, the Python action applied the £300 limit unconditionally every time, whereas an LLM agent might reason around it or apply it inconsistently.
The Rasa CALM agent also showed in Conversation 3 that out-of-scope requests trigger a specific fixed response rather than an improvised answer, which is the right behaviour for a booking commitment.
One observation unlikely to be replicated with CALM: in Query 2, the LangGraph agent called search_venues three times with identical parameters before concluding that no venue existed - a retry loop the trace revealed.
CALM would have collected the slot once and run the Python check once. The difference in failure behaviour is just as important as the difference in success behaviour.
In the context of this exercise, there is a 113 lines of code difference between Exercise 2 and Exercise 4, showing that the MCP moves a portion of code out of the agent entirely.
"""
