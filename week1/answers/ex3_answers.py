"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────
# 160 guests, ~50 vegan, £200 deposit. Expected outcome: confirmed.

CONVERSATION_1_TRACE = """
PASTE YOUR rasa shell TERMINAL OUTPUT HERE
"""

CONVERSATION_1_OUTCOME = "FILL_ME_IN"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────
# Same as above but with a deposit above MAX_DEPOSIT_GBP.

CONVERSATION_2_TRACE = """
PASTE YOUR rasa shell TERMINAL OUTPUT HERE
"""

CONVERSATION_2_OUTCOME = "FILL_ME_IN"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "FILL_ME_IN"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────
# Try asking for parking, AV equipment, or anything not in the domain
# while the form is collecting slots.

CONVERSATION_3_TRACE = """
PASTE YOUR rasa shell TERMINAL OUTPUT HERE
"""

# Describe what Rasa did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
FILL ME IN
"""

# Compare Rasa's handling to LangGraph's (Exercise 2 Scenario 3). Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
FILL ME IN
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = None   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = []

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
FILL ME IN
"""

# How does the cutoff guard compare to implementing the same logic in LangGraph?
# Min 30 words.
TASK_B_RASA_VS_LANGGRAPH = """
FILL ME IN
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The setup cost (config.yml, domain.yml, nlu.yml, rules.yml, actions.py,
# rasa train, two terminals) bought you something specific.
# What was it? Min 40 words.
SETUP_COST_VALUE = """
FILL ME IN
"""
