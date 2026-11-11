"""Your TDD workspace. The first test is deliberately RED -- that is step one."""
from datetime import date

import pytest

from tdd_lab.promo import PromoError, apply_promo

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

# Test 2 - The discount rounds down to a whole cent.
def test_rounds_discount_down():
    # 10% of 1,005 is 100.5 -> discount rounds DOWN to 100 -> total 905
    assert apply_promo(1_005, "SAVE10", TODAY) == 905

# Test 3 - Promo codes ignore case and surrounding whitespace.
def test_codes_ignore_case_and_whitespace():
    # Test that leading and trailing whitespace is ignored.
    assert apply_promo(10_000, " save10 ", TODAY) == 9_000

# Test 4 - FLAT5 applies only when the subtotal is at least $20.00.
def test_flat5_minimum_boundary():
    # Exactly $20.00 qualifies.
    assert apply_promo(2_000, "FLAT5", TODAY) == 1_500

    # One cent below $20.00 must be rejected.
    with pytest.raises(PromoError):
        apply_promo(1_999, "FLAT5", TODAY)

# Test 5 - WELCOME applies only on or before December 31, 2026.
def test_welcome_expiry_boundary():
    # The last valid date is December 31, 2026.
    assert apply_promo(
        10_000,
        "WELCOME",
        date(2026, 12, 31)
    ) == 8_500

    # January 1, 2027 is too late.
    with pytest.raises(PromoError):
        apply_promo(
            10_000,
            "WELCOME",
            date(2027, 1, 1)
        )

