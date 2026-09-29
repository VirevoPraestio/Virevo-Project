"""Builds the sample set: twelve consecutive graphic-bearing turns of one
conversation, one per form, so the per-turn theme alternation is visible as it
would actually appear. Content is illustrative Discharge / Bed Management
material.

Turn 11 is the answered redraw of turn 10 and therefore keeps turn 10's theme
and geometry — the two exceptions to alternation and to the fit search, both
exercised here rather than described.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import form_agenda
import form_bands
import form_cards
import form_chain
import form_derivation
import form_fill_blank
import form_fork
import form_merged_flow
import form_rail
import form_roles
import form_two_flow
import form_wrapped_chain
from tokens import pick_theme

OUT = os.path.join(os.path.dirname(__file__), "..", "samples")
os.makedirs(OUT, exist_ok=True)

RATIOS = (("wide", "desktop"), ("tall", "mobile"))

# --------------------------------------------------------------- content ----

T_AGENDA = {
    "title": "What We Would Need to Establish",
    "subtitle": "Four areas, one at a time",
    "areas": [
        {"title": "Discharge timings", "question": "How long does it really take?",
         "start": True},
        {"title": "Bed allocation record", "question": "Do the timings check out?"},
        {"title": "Evening staffing", "question": "Who is already on shift?"},
        {"title": "Admission demand", "question": "Is the freed time capturable?"},
    ],
    "note": "Not in order; take whichever you have numbers for first.",
}

T_CHAIN = {
    "title": "Where the Discharge Day Actually Goes",
    "subtitle": "Your own timestamps, one weekday",
    "steps": [
        {"title": "Doctor's round", "values": ["~09:30"]},
        {"title": "Summary drafted", "values": ["~12:15"],
         "state": "target", "tag": "BIGGEST LEAK"},
        {"title": "Billing cleared", "values": ["~14:40"]},
        {"title": "Pharmacy return", "values": ["~15:50"]},
        {"title": "Bed free", "values": ["~16:45"], "state": "outcome"},
    ],
    "note": "The 18:00-22:00 window is already staffed and carries none of this.",
    "effects": [
        {"title": "Dead bed time", "values": ["5h 15m"],
         "caption": "Per discharge, derived"},
        {"title": "Beds lost", "values": ["~8 bed-days"], "caption": "Per day"},
    ],
}

T_DERIVATION = {
    "title": "What the Delay Costs",
    "subtitle": "Working shown; conservative basis where your figures disagree",
    "steps": [
        {"title": "Dead bed time", "input": "5h 15m each",
         "result": "3.7 bed-days/day"},
        {"title": "Your volume", "input": "42 discharges/day",
         "result": "220 bed-days/mo"},
        {"title": "At your occupancy", "input": "78% occupied",
         "result": "172 billable"},
    ],
    "answer": {"title": "Revenue not billed", "values": ["Rs. 2.7 Cr/yr"]},
    "condition": "Holds only while admissions demand exceeds free beds in the "
                 "same window. Your two occupancy figures disagree; this takes "
                 "the lower, so it understates.",
    "outputs": [
        {"title": "ALOS", "values": ["-0.4 days"],
         "caption": "Derived, not measured"},
        {"title": "Occupancy headroom", "values": ["+6 pts"],
         "caption": "Same effect, counted above"},
    ],
}

T_WRAPPED = {
    "title": "The Full Discharge Sequence",
    "subtitle": "Every named step, evening through to the bed being free",
    "steps": [
        {"title": "Decision taken", "values": ["Evening round"]},
        {"title": "Summary drafted", "values": ["Evening window"], "state": "start",
         "tag": "MOVES HERE"},
        {"title": "Consultant sign-off", "values": ["~08:00"]},
        {"title": "Billing assembled", "values": ["Auto-triggered"]},
        {"title": "Insurance query", "values": ["Where applicable"],
         "state": "dashed"},
        {"title": "Pharmacy return", "values": ["~09:40"]},
        {"title": "Counselling", "values": ["~10:10"]},
        {"title": "Bed free", "values": ["~11:15"], "state": "outcome"},
    ],
    "note": "Everything before sign-off already happens while the ward is quiet.",
}

T_RAIL = {
    "title": "What Feeds the Morning Bed Position",
    "subtitle": "Four sources, one number",
    "inputs_label": "COLLECTED THE NIGHT BEFORE",
    "inputs": [
        {"title": "Expected discharges", "values": ["From the evening round"]},
        {"title": "Booked admissions", "values": ["Elective list"]},
        {"title": "ICU step-downs", "values": ["Flagged at 22:00"]},
        {"title": "Held beds", "values": ["Cleaning, repair"]},
    ],
    "target": {"title": "Beds genuinely free at 08:00", "values": ["One number"],
               "state": "outcome",
               "caption": "Published before the first admission call"},
    "note": "None of these is new data. All four already exist by 22:00.",
}

T_FORK = {
    "title": "Which Pattern Is Yours?",
    "subtitle": "Both are common; neither is the wrong answer",
    "question": {"title": "When is the discharge summary written?",
                 "values": ["Pick the one that matches the floor"]},
    "branches": [
        {"title": "After the morning round",
         "values": ["Doctor writes it that day"],
         "caption": "Most common"},
        {"title": "The evening before",
         "values": ["Drafted, signed next morning"],
         "caption": "Less common"},
        {"title": "It varies by consultant",
         "values": ["No single practice"],
         "caption": "Worth saying if true"},
    ],
}

T_TWO_FLOW = {
    "title": "Insured and Cash Discharges Compared",
    "subtitle": "Genuinely different paths, step for step",
    "flows": [
        {"label": "INSURED", "steps": [
            {"title": "Summary ready", "values": ["~11:00"]},
            {"title": "Pre-auth final approval", "values": ["~14:20"],
             "state": "target"},
            {"title": "Billing cleared", "values": ["~15:30"]},
            {"title": "Bed free", "values": ["~16:45"], "state": "outcome"},
        ]},
        {"label": "CASH", "steps": [
            {"title": "Summary ready", "values": ["~11:00"]},
            {"title": "Bill settled at counter", "values": ["~12:10"]},
            {"title": "Billing cleared", "values": ["~12:30"]},
            {"title": "Bed free", "values": ["~13:15"], "state": "outcome"},
        ]},
    ],
    "effects": [
        {"title": "Gap between the two paths", "values": ["3h 30m"],
         "caption": "Entirely inside pre-auth"},
    ],
}

T_MERGED = {
    "title": "One Process, Two Payment Paths",
    "subtitle": "The same chain, drawn once",
    "flows": ["Ins", "Cash"],
    "steps": [
        {"title": "Summary ready", "value": "~11:00"},
        {"title": "Payment cleared", "values": ["~14:20", "~12:10"]},
        {"title": "Pre-auth approval", "value": "~14:20", "only_on": "Ins",
         "bypass": "Cash skips ahead"},
        {"title": "Pharmacy return", "value": "~15:30"},
        {"title": "Bed free", "values": ["~16:45", "~13:15"], "state": "outcome"},
    ],
    "note": "Four of the five steps are identical. Only one is genuinely different.",
}

T_BANDS = {
    "title": "How the Evening Draft Actually Gets Built",
    "subtitle": "Not many systems — three",
    "bands": [
        {"label": "INPUTS — ALL ALREADY EXIST", "items": [
            {"title": "Vitals and notes", "values": ["From the HIS"]},
            {"title": "Medication chart", "values": ["From pharmacy"]},
            {"title": "Investigation results", "values": ["From the lab"]},
        ]},
        {"label": "ENGINE", "items": [
            {"title": "Draft assembler", "values": ["One service, triggered at 18:00"],
             "state": "start"},
        ]},
        {"label": "OUTPUTS", "items": [
            {"title": "Draft summary", "values": ["Awaiting sign-off"]},
            {"title": "Provisional bill", "values": ["Cascades on sign-off"]},
        ]},
    ],
    "note": "Nothing here asks a clinician to enter something they do not already enter.",
}

T_BLANK = {
    "title": "Your Four Timestamps",
    "subtitle": "Fill these in and the rest of the arithmetic follows",
    "steps": [
        {"title": "Doctor's round", "hint": "When is the decision taken?",
         "value": "09:30"},
        {"title": "Summary signed", "hint": "When is it actually signed?",
         "value": "12:15"},
        {"title": "Billing cleared", "hint": "When does the bill close?",
         "value": "14:40"},
        {"title": "Patient leaves", "hint": "When is the bed physically free?",
         "value": "16:45"},
    ],
    "note": "Approximate is fine. A typical weekday, not the best one.",
}

T_ROLES = {
    "title": "Who Has to Cooperate",
    "subtitle": "And what each is actually being asked for",
    "roles": [
        {"title": "Ward nurses", "asked": "No extra time",
         "caption": "Confirm, not produce"},
        {"title": "Consultants", "asked": "Sign a draft, not write one",
         "resistant": True, "caption": "Gives up the 'my own words' summary"},
        {"title": "Billing desk", "asked": "Work from a cascade",
         "caption": "Starts earlier, same work"},
    ],
    "approver": {"title": "Medical Superintendent",
                 "values": ["Approves the sign-off change"],
                 "tag": "APPROVES",
                 "caption": "Outside the daily routine — easy to leave out"},
    "fails_if": "Without this approval the draft is written and never signed, and "
                "the evening work is wasted.",
}

T_CARDS = {
    "title": "What Nothing Currently Tracks",
    "subtitle": "Three gaps, in the order they block things",
    "cards": [
        {"title": "Summary start time", "values": ["Not recorded anywhere"],
         "state": "target", "caption": "Blocks the whole derivation"},
        {"title": "Bed-ready timestamp", "values": ["Recorded, not reliable"],
         "caption": "Entered in a batch at shift end"},
        {"title": "Admission wait at 14:00", "values": ["Not recorded"],
         "caption": "Decides whether freed time is capturable"},
    ],
    "effects": [
        {"title": "Measurable from day one", "values": ["Two of three"],
         "caption": "The third needs one field added"},
    ],
}

TURNS = [
    ("t01-agenda", form_agenda, T_AGENDA, {}),
    ("t02-chain", form_chain, T_CHAIN, {}),
    ("t03-derivation", form_derivation, T_DERIVATION, {}),
    ("t04-wrapped-chain", form_wrapped_chain, T_WRAPPED, {}),
    ("t05-rail", form_rail, T_RAIL, {}),
    ("t06-fork", form_fork, T_FORK, {}),
    ("t07-two-flow", form_two_flow, T_TWO_FLOW, {}),
    ("t08-merged-flow", form_merged_flow, T_MERGED, {}),
    ("t09-bands", form_bands, T_BANDS, {}),
    ("t10-blank", form_fill_blank, dict(T_BLANK, filled=False), {}),
    ("t11-blank-filled", form_fill_blank, dict(T_BLANK, filled=True),
     {"continuity_of": 9}),
    ("t12-cards", form_cards, T_CARDS, {}),
    ("t13-roles", form_roles, T_ROLES, {}),
]


def main():
    geometry = {}
    subject = 0                 # advances per subject, not per file or redraw
    for i, (name, mod, slots, opts) in enumerate(TURNS):
        cont = opts.get("continuity_of")
        th = pick_theme(subject, continuity_of=cont)
        if cont is None:
            subject += 1
        for ratio, suffix in RATIOS:
            path = os.path.join(OUT, f"{name}-{suffix}-{th}.svg")
            lock = geometry.get((cont, ratio)) if cont is not None else None
            r = mod.build(slots, ratio, th, path,
                          w=lock["w"] if lock else None,
                          h=lock["h"] if lock else None,
                          base_lock=lock["base"] if lock else None)
            geometry[(i, ratio)] = r
            print(f"{os.path.basename(path):44} {r['bytes']:>5}b  "
                  f"{r['w']}x{r['h']}  {th}")


if __name__ == "__main__":
    main()
