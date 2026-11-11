"""Your TDD workspace. The starter's first test was deliberately RED.
The seven promotion tests were developed using Red-Green-Refactor.
"""

from datetime import date

import pytest

from tdd_lab import promo
from tdd_lab.promo import PromoError, apply_promo


TODAY = date(2026, 11, 9)


# Test 1 - SAVE10 applies a 10% discount.
def test_save10_takes_ten_percent_off():
    assert apply_promo(10_000, "SAVE10", TODAY) == 9_000

    # A zero subtotal should remain zero.
    assert apply_promo(0, "SAVE10", TODAY) == 0

# TDD process: write one failing test, implement the behavior, then refactor.
# Behaviors covered: rounding, case/whitespace, minimums, expiry boundary,
# unknown codes, and nonnegative totals.


# Test 2 - The discount rounds down to a whole cent.
def test_rounds_discount_down():
    # 10% of 1,005 is 100.5, so the discount rounds down to 100.
    assert apply_promo(1_005, "SAVE10", TODAY) == 905


# Test 3 - Promo codes ignore case and surrounding whitespace.
def test_codes_ignore_case_and_whitespace():
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


# Test 6 - An unknown promo code raises PromoError.
def test_unknown_code_raises_promo_error():
    with pytest.raises(PromoError):
        apply_promo(10_000, "NOTREAL", TODAY)


# Test 7 - The total never goes below zero.
def test_total_never_goes_below_zero(monkeypatch):
    # Simulate an unusually large discount.
    monkeypatch.setattr(
        promo,
        "FLAT5_DISCOUNT_CENTS",
        5_000
    )

    # A $20 subtotal minus a simulated $50 discount must equal zero.
    assert promo.apply_promo(2_000, "FLAT5", TODAY) == 0
