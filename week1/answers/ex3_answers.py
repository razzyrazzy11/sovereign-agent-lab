"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?

Note: All exercises use Llama 3.3 70B Instruct via the Nebius API. Results may differ if you used a different model.
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                         
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                           
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                  
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                                                         
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->   
"""

CONVERSATION_1_OUTCOME = "confirmed"  # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                         
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                           
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                  
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit  
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->                 
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
# the reason the agent gave for escalating
CONVERSATION_2_REASON = "The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input -> calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  can you arrange parking for the speakers?                                                                                                                            
I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->   
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
When asking about parking for the speakers mid-flow, CALM immediately recognised this as outside the scope of the booking confirmation task. 
Rather than attempting to answer or reason about parking, it responded with a fixed message stating it can only help with tonight's venue booking, and offered to continue with the booking confirmation rather than ending the conversation.
This shows the deterministic flow structure of CALM: the out-of-scope trigger led to the handle_out_of_scope flow being triggered, rather than a response from emergent reasoning at runtime as in the LangGraph agent.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
In LangGraph Scenario 3, the agent received a train times query and responded by stating it could not execute the task as it could not execute the task as it exceeds its function limitations.
This came from the model reasoning about its capabilities at runtime. In CALM Conversation 3, the parking question triggered the handle_out_of_scope flow, which returned a fixed response with no reasoning involved.
The key difference is that LangGraph's response was emergent from the LLM's own judgement, while CALM's response was deterministic - a specific flow triggered and a specific message was returned, with no variation or hallucination.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Temporarily changed the deposit guard condition to if True: and ran a new rasa shell conversation, providing valid guest count and vegan count, then any deposit amount. 
The bot escalated as expected, confirming the cutoff logic triggers after all three slots are collected.
The bot gave the escalation message as follows:
I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 - insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
The LLM now handles what Python previously did: intent classification, entity extraction, and slot filling are replaced from_llm mappings and natural language flow descriptions.
You no longer write nlu.yml examples or rules.yml dialogue paths.
Python still handles business rules in ActionValidateBooking: the deposit limit check, the confirmation message and the escalation decision. 
These require deterministic, auditable logic that an LLM cannot be trusted to execute reliably. 
The tradeoff is that CALM is faster to setup and more robust to paraphrase, but you lose control over how user inputs are interpreted.
In the old approach, you could inspect exactly which regex or intent matched whereas with CALM, the LLM's extraction is a black box, making it harder to debug when it goes wrong.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
CALM still requires config.yml, domain.yml, flows.yml, endpoints.yml, a rasa train step, two terminals and a Rasa Pro license.
The old Rasa also needed nlu.yml, rules.yml, and a FormValidationAction, so CALM is actually simpler.
However, it still is significantly more infrastructure than LangGraph: you need a running actions server, a trained model artifact, and the Rasa Pro license just to start. 
That kind of setup is a deterministic flow control: the agent cannot go off-script, it cannot improvise a response it wasn't trained on, and it cannot call a tool that wasn't defined in flows.yml.
For the booking confirmation use case, this is a feature as the organiser wants to behave identically every time. However, for more a more open-ended assistant, it would be be a limitation.
"""
