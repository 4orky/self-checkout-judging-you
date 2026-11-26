#!/usr/bin/env python3
# The Self-Checkout Is Judging You - one smug line from a judgmental till
# bounty slug: u-motasimfuad-the-self-checkout-is-judging-you-b71130d6
# This script drafts fourteen original single-line remarks in the voice of
# a smug self-checkout machine, scores each one by hand against the five
# measures the judge's brief weights (machine voice first, a real laugh on
# a single read, petty about the basket and the bagging, tight with no
# padding, fresh rather than the joke everyone has heard), keeps the best,
# and writes it to /output/entry.txt as UTF-8 without a trailing newline.
# Second pass, after the first run: the winning triple read "no spoon, no
# shame, no plan", and "no plan" was the weak word - vague, not about food.
# It now reads "no spoon, no shame, no meal", which lands the actual joke
# (twelve yoghurts is not a meal) and lifts the winner from 46 to 47; the
# crisis draft was also restored to its intended wording (ellipsis, price).
# The grading is fixed and deterministic, so the same line wins on every
# run, byte for byte. No network, no file reads outside this script.
from hashlib import sha256
from pathlib import Path
DRAFTS = [
    (("Twelve yoghurts. No spoon, no shame, no meal. ",
      "Please place your dignity in the bagging area."), 47),
    (("Congratulations: twelve yoghurts is not a diet, ",
      "it is a cry for help. Please take your receipt."), 44),
    (("Scanning twelve yoghurts\u2026 and one existential crisis. ",
      "The crisis is free. The yoghurts are \u00a39.48."), 44),
    (("Twelve yoghurts. I have run the numbers: you are not ",
      "meal-prepping, you are panicking."), 43),
    (("Twelve yoghurts. I checked twice - still not a personality. ",
      "Please bag your choices."), 43),
    (("Twelve yoghurts, zero meals. Even I can see the pattern, ",
      "and I am a till."), 42),
    (("Twelve yoghurts, no spoon in sight. I have alerted a human. ",
      "They are laughing too."), 42),
    (("You bought twelve yoghurts and a single carrot, ",
      "as if the carrot could save you. It cannot."), 42),
    (("You scanned twelve yoghurts. I scanned your life choices. ",
      "Mine were faster."), 41),
    (("Twelve yoghurts, no basket, no shame. I have seen things, ",
      "but never a meal plan this brave."), 41),
    (("Twelve yoghurts and nothing else. ",
      "Bold of you to call this a shop."), 40),
    (("I have seen your basket. Twelve yoghurts, one lonely banana. ",
      "The banana is judging you too."), 40),
    (("Your basket contains twelve yoghurts and the confidence ",
      "of a person who has given up."), 39),
    (("Please do not look at me like that. You bought twelve yoghurts. ",
      "I only work here."), 38),]
FORBIDDEN = ("unexpected item in the bagging area",)
def join(parts):
    return "".join(parts)
def vet(line):
    if not line.strip():
        raise ValueError("draft is blank")
    if "\n" in line or "\r" in line:
        raise ValueError("draft must stay on one line")
    if not 1 <= len(line) <= 200:
        raise ValueError("draft breaks the 1-200 character gate: %d" % len(line))
    lowered = line.lower()
    for bad in FORBIDDEN:
        if bad in lowered:
            raise ValueError("draft repeats the stock bagging-area joke")
def emit():
    champion = ""
    champion_key = None
    for parts, points in DRAFTS:
        line = join(parts)
        vet(line)
        key = (points, -len(line))
        if champion_key is None or key > champion_key:
            champion_key = key
            champion = line
    vet(champion)
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = champion.encode("utf-8")
    (out_dir / "entry.txt").write_bytes(payload)
    print("wrote %d chars, %d bytes, sha256=%s" % (len(champion), len(payload), sha256(payload).hexdigest()))
    print(champion)
if __name__.endswith("__main__"):
    emit()
