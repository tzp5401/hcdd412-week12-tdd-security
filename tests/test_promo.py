"""Your TDD workspace. The first test is deliberately RED -- that is step one."""
from datetime import date

from tdd_lab.promo import apply_promo

TODAY = date(2026, 11, 9)


# Test 1 - SAVE10 applies a 10% discount.
def test_save10_takes_ten_percent_off():
    # Test that the SAVE10 promo code correctly applies a 10% discount.
    assert apply_promo(10_000, "SAVE10", TODAY) == 9_000

    # A zero subtotal should remain zero.
    assert apply_promo(0, "SAVE10", TODAY) == 0

# Next: write a failing test for the next rule, make it pass, refactor. Repeat.
# Think edge cases: rounding, case/whitespace, minimums, expiry date boundary,
# unknown code, and a total that would otherwise go negative.
