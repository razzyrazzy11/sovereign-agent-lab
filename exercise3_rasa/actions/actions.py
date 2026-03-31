"""
Exercise 3 — Rasa Custom Actions
==================================

WHAT THIS FILE DOES
--------------------
Two action classes that contain all the business logic for the
Edinburgh booking confirmation agent.

  1. ValidateBookingConfirmationForm
     Runs during slot collection. Called automatically by Rasa each time
     the user responds to an utter_ask_<slot_name> question.
     Its job: extract a number from whatever the user typed.

  2. ActionValidateBooking
     Runs once, after the form has collected all three slots.
     Its job: apply Rod's business constraints and either confirm
     or escalate the booking.

WHY BUSINESS LOGIC IS HERE AND NOT IN THE PROMPT
-------------------------------------------------
If you wrote Rod's limits into a system prompt ("only confirm if the deposit
is under £300") the model could reason its way around them — maybe the
manager says "it's really just a £50 holding fee plus £300 insurance, so
really it's under the limit", and the model agrees. That kind of semantic
flexibility is a feature in a research agent. In a confirmation agent that
makes legally binding commitments, it is a liability.

Python code doesn't negotiate. `if deposit > MAX_DEPOSIT_GBP: escalate()`
runs the same way every time, regardless of how the deposit was described.

TASK B — CUTOFF GUARD
----------------------
Your task is to uncomment the four-line block marked "TASK B" below.

It adds a time-based guard: if it is past 16:45, the agent escalates
immediately after collecting the slots — there isn't enough time to
process the booking before Rod's 5 PM deadline.

Steps:
  1. Uncomment the block (remove the # from each of the four lines)
  2. Save this file
  3. Retrain: cd exercise3_rasa && rasa train
  4. Restart the action server: rasa run actions
  5. Test by temporarily making the condition always True:
         if True:   # ← temporary
     Run a conversation, verify it escalates, then revert.
  6. Set TASK_B_DONE = True in week1/answers/ex3_answers.py
"""

import datetime
import re
from typing import Any, Dict, List, Optional, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

# ── Business constraints ───────────────────────────────────────────────────────
# Written as Python constants, not prompt text.
# Change them here; they take effect on the next restart. No retraining needed.

MAX_GUESTS      = 170    # venue hard capacity ceiling
MAX_DEPOSIT_GBP = 300    # Rod's maximum authorised deposit
MAX_VEGAN_RATIO = 0.80   # flag if more than 80% of guests need vegan meals


# ── Utility ───────────────────────────────────────────────────────────────────

def _parse_number(text: Any) -> Optional[float]:
    """
    Extract the first number from whatever the user typed.

    Examples that all return 160.0:
      "160"
      "about 160 guests"
      "we have 160 confirmed"
      "160 people, maybe a few more"

    Returns None if no number found, which causes the form to re-ask.
    """
    match = re.search(r"\d+(?:\.\d+)?", str(text))
    return float(match.group()) if match else None


# ── Form validation ───────────────────────────────────────────────────────────

class ValidateBookingConfirmationForm(FormValidationAction):
    """
    Validates each slot as the form collects it.

    Rasa calls validate_<slot_name>() automatically after the user responds
    to utter_ask_<slot_name>.

    Return {slot_name: value}  →  accepted, form moves to next slot
    Return {slot_name: None}   →  rejected, form re-asks the question
    """

    def name(self) -> Text:
        return "validate_booking_confirmation_form"

    def validate_guest_count(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        number = _parse_number(slot_value)
        if number and number > 0:
            return {"guest_count": number}
        dispatcher.utter_message(
            text="I need a number for the guest count. How many guests are attending?"
        )
        return {"guest_count": None}

    def validate_vegan_count(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        number = _parse_number(slot_value)
        if number is not None and number >= 0:
            return {"vegan_count": number}
        dispatcher.utter_message(
            text="I need a number — how many guests require vegan meals?"
        )
        return {"vegan_count": None}

    def validate_deposit_amount_gbp(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        number = _parse_number(slot_value)
        if number is not None and number >= 0:
            return {"deposit_amount_gbp": number}
        dispatcher.utter_message(
            text="I need a GBP amount for the deposit. How much are you proposing?"
        )
        return {"deposit_amount_gbp": None}


# ── Post-form business logic ──────────────────────────────────────────────────

class ActionValidateBooking(Action):
    """
    Applies Rod's constraints after the form collects all slots.
    Guards run in order. The first that fails causes escalation.
    If all pass, the booking is confirmed immediately.
    """

    def name(self) -> Text:
        return "action_validate_booking"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        guests  = float(tracker.get_slot("guest_count")       or 0)
        vegans  = float(tracker.get_slot("vegan_count")       or 0)
        deposit = float(tracker.get_slot("deposit_amount_gbp") or 0)

        def escalate(reason: str) -> List[Dict]:
            """Send the escalation message and record the reason."""
            dispatcher.utter_message(
                text=(
                    "I need to check one thing with the organiser before I can confirm. "
                    f"The issue is: {reason}. "
                    "Can I call you back within 15 minutes?"
                )
            )
            return [
                SlotSet("booking_valid", False),
                SlotSet("rejection_reason", reason),
            ]

        # ── TASK B: Cutoff Guard ──────────────────────────────────────────────
        # Uncomment these four lines to implement the time-based escalation.
        #
        # HOW IT WORKS:
        # If the current time is past 16:45 (4:45 PM), the agent escalates
        # immediately — not enough time remains to process a confirmation
        # before Rod's 5 PM deadline.
        #
        # TO TEST WITHOUT WAITING UNTIL 4:45 PM:
        # Temporarily change the condition to: if True:
        # Run a conversation and verify it escalates after the form completes.
        # Then revert to the real condition before submitting.
        #
        # now = datetime.datetime.now()
        # if now.hour > 16 or (now.hour == 16 and now.minute >= 45):
        #     return escalate(
        #         "it is past 16:45 — insufficient time to process the confirmation"
        #         " before the 5 PM deadline"
        #     )

        # ── Guard 1: Capacity ─────────────────────────────────────────────────
        if guests > MAX_GUESTS:
            return escalate(
                f"the guest count ({int(guests)}) exceeds the venue's "
                f"maximum capacity of {MAX_GUESTS}"
            )

        # ── Guard 2: Deposit ──────────────────────────────────────────────────
        if deposit > MAX_DEPOSIT_GBP:
            return escalate(
                f"a deposit of £{deposit:.0f} exceeds the organiser's "
                f"authorised limit of £{MAX_DEPOSIT_GBP}"
            )

        # ── Guard 3: Vegan ratio ──────────────────────────────────────────────
        vegan_ratio = vegans / guests if guests > 0 else 0
        if vegan_ratio > MAX_VEGAN_RATIO:
            return escalate(
                f"{int(vegans)} of {int(guests)} guests requiring vegan meals "
                f"({vegan_ratio:.0%}) is unusually high — needs organiser confirmation"
            )

        # ── All guards passed ─────────────────────────────────────────────────
        dispatcher.utter_message(
            text=(
                f"Thank you — booking confirmed. "
                f"{int(guests)} guests, {int(vegans)} requiring vegan meals, "
                f"£{deposit:.0f} deposit accepted. "
                f"I'll send written confirmation to the organiser shortly."
            )
        )
        return [SlotSet("booking_valid", True)]
