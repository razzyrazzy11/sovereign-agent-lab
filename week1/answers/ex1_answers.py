"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.

Note: All exercises use Llama 3.3 70B Instruct via the Nebius API. Results may differ if you used a different model.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER = "The Haymarket Vaults"
PART_A_XML_ANSWER = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT = True   # True or False
PART_A_XML_CORRECT = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All of the three formatting conditions - plain text, XML tags and sandwich - returned a correct venue in Part A with clean data.
The PLAIN condition selected The Haymarket Vaults while XML and SANDWICH both selected The Albanach. Both are valid answers since both venues meet the constraints of 160-guests, vegan and available.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER = "The Haymarket Vaults"
PART_B_XML_ANSWER = "The Albanach The Haymarket Vaults"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT = True
PART_B_XML_CORRECT = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = True

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
Note: All exercises use Llama 3.3 70B Instruct via the Nebius API. Results may differ if you used a different model.
The Holyrood Arms is defined in the context as a near-miss distractor added to the VENUES_WITH_DISTRACTORS, it's designed as a trap.
It is also the hardest distractor because it satisfies two of the three constraints - it has capacity 160 (meets the minimum) and vegan options - but its status is FULL, making it unavailable.
The Holyrood Arms also appears immediately before the correct answer in the list, so a model doing pattern-matching on capacity and vegan without checking status could pick it instead of the correct answer.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True   # True or False

PART_C_PLAIN_ANSWER = "The Haymarket Vaults"
PART_C_XML_ANSWER = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C ran the same distractor dataset as Part B but using a smaller 8B model. All three conditions (PLAIN, XML and SANDWICH) returned correct answers, The Haymarket Vaults each time.
Although the smaller model could've been more easily distracted by the near-miss distractor, it still managed to pick the correct answer despite the presence of the Holyrood Arms, which is a strong distractor. 
This suggests that the model is able to understand and apply the constraints successfully.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the model and dataset are weaker - specifically when near-miss distractors are present and the model is smaller. 
In the run conducted, the 70B model answered correctly under the three formats in both clean and distractor conditions. The smaller 8B model also answered correctly under the formats.
Past a model size threshold, structural formatting may not be as necessary to get the right answer, but it can still be a useful tool to guide the model's attention and reasoning.
Context formatting may also matter more for a more complex dataset with more distractors, where the model needs more guidance to navigate information.
In my run, there was an interesting signal from the XML condition in Part B: it returned both The Albanach and The Haymarket Vaults rather than just one.
This suggested the the structured tags may have caused the model to treat the question slightly differently, as a listing task rather than a selection task. 
The formatting-induced behaviour change appeared even with the 70B model, which was somewhat unexpected.
"""
