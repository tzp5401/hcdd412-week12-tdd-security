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

This file started as a stub and was completed using TDD:
write failing tests FIRST (Red), make them pass (Green),
then clean up (Refactor).
"""

from datetime import date


class PromoError(ValueError):
    """Raised when a promo code cannot be applied."""


# Promotion constants
SAVE10_CODE = "SAVE10"

FLAT5_CODE = "FLAT5"
FLAT5_MINIMUM_CENTS = 2_000
FLAT5_DISCOUNT_CENTS = 500

WELCOME_CODE = "WELCOME"
WELCOME_LAST_DAY = date(2026, 12, 31)
WELCOME_DISCOUNT_PERCENT = 15


def _percentage_discount(subtotal_cents: int, percentage: int) -> int:
    """Calculate a percentage discount, rounded down to a whole cent."""
    return subtotal_cents * percentage // 100


def _normalize_code(code: str) -> str:
    """Remove surrounding whitespace and uppercase the promo code."""
    return code.strip().upper()


def _non_negative_total(
    subtotal_cents: int,
    discount_cents: int
) -> int:
    """Calculate a discounted total that cannot be negative."""
    return max(subtotal_cents - discount_cents, 0)


def apply_promo(subtotal_cents: int, code: str, today: date) -> int:
    """Return the new total in cents after applying a promo code."""

    normalized_code = _normalize_code(code)

    if normalized_code == SAVE10_CODE:
        discount_cents = _percentage_discount(subtotal_cents, 10)

    elif normalized_code == FLAT5_CODE:
        if subtotal_cents < FLAT5_MINIMUM_CENTS:
            raise PromoError("FLAT5 requires a minimum subtotal of $20.00")

        discount_cents = FLAT5_DISCOUNT_CENTS

    elif normalized_code == WELCOME_CODE:
        if today > WELCOME_LAST_DAY:
            raise PromoError("WELCOME has expired")

        discount_cents = _percentage_discount(
            subtotal_cents,
            WELCOME_DISCOUNT_PERCENT
        )

    else:
        raise PromoError(
            f"Unknown promotion code: {normalized_code!r}"
        )

    return _non_negative_total(subtotal_cents, discount_cents)
