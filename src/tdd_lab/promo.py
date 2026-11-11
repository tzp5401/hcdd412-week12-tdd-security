"""Promo-code pricing -- the feature you will build with TDD (Red-Green-Refactor).

Business rules (from the product owner):

* ``SAVE10``  - 10% off the subtotal (round the discount DOWN to a whole cent).
* ``FLAT5``   - $5.00 off, but only when the subtotal is at least $20.00.
* ``WELCOME`` - 15% off, valid only on or before 2026-12-31.
* Codes are case-insensitive and surrounding whitespace is ignored.
* An unknown, expired, or ineligible code must raise ``PromoError`` -- never
  silently return the full price.
* The total can never go below zero.

All money is integer cents. Dates are ``datetime.date``.

Right now this is only a stub. Write failing tests FIRST (Red), then make them
pass (Green), then clean up (Refactor).
"""
from datetime import date


class PromoError(ValueError):
    """Raised when a promo code cannot be applied."""

SAVE10_CODE = "SAVE10"

FLAT5_CODE = "FLAT5"
FLAT5_MINIMUM_CENTS = 2_000
FLAT_DISCOUNT_CENTS = 500

WELCOME_CODE = "WELCOME"
WELCOME_LAST_DAY = date(2026, 12, 31)
WELCOME_DISCOUNT_PERCENT = 15

def _percentage_discount(subtotal_cents: int, percentage: int) -> int:
    """Calculate a percentage discount, rounded down to a whole cent."""
    return subtotal_cents * percentage // 100

def _normalize_code(code: str) -> str:
    """Normalize a promo code by removing surrounding whitespace and uppercasing it."""
    return code.strip().upper()

def apply_promo(subtotal_cents: int, code: str, today: date) -> int:
    """Return the new total in cents after applying ``code``."""

    normalized_code = _normalize_code(code)

    if normalized_code == SAVE10_CODE:
        discount_cents = _percentage_discount(subtotal_cents, 10)
        return subtotal_cents - discount_cents

    elif normalized_code == FLAT5_CODE:
        if subtotal_cents < FLAT5_MINIMUM_CENTS:
            raise PromoError("FLAT5 requires a minimum subtotal of $20.00")
        
        return subtotal_cents - FLAT_DISCOUNT_CENTS

    elif normalized_code == WELCOME_CODE:
        if today > WELCOME_LAST_DAY:
            raise PromoError("WELCOME has expired")
        
        discount_cents = _percentage_discount(
            subtotal_cents, 
            WELCOME_DISCOUNT_PERCENT
        )
        
        return subtotal_cents - discount_cents

    raise PromoError("Unknown promotion code.")
