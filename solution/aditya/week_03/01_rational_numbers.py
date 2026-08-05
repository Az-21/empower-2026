from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True, slots=True)
class RationalNumber:
  """A rational number, always stored in lowest terms with a positive denominator."""

  _numerator: int
  _denominator: int


def make_rational(
  numerator_value: int,
  denominator_value: int,
) -> RationalNumber:
  """Constructor."""

  if denominator_value == 0:
    raise ValueError("Denominator cannot be zero")

  common_divisor = gcd(numerator_value, denominator_value)

  numerator_value //= common_divisor
  denominator_value //= common_divisor

  if denominator_value < 0:
    numerator_value = -numerator_value
    denominator_value = -denominator_value

  return RationalNumber(numerator_value, denominator_value)


def numerator(rational_number: RationalNumber) -> int:
  """Selector."""

  return rational_number._numerator


def denominator(rational_number: RationalNumber) -> int:
  """Selector."""

  return rational_number._denominator


def add_rational(
  first_rational: RationalNumber,
  second_rational: RationalNumber,
) -> RationalNumber:
  """first_rational + second_rational, returned in lowest terms."""

  new_numerator = numerator(first_rational) * denominator(second_rational) + numerator(second_rational) * denominator(
    first_rational
  )

  new_denominator = denominator(first_rational) * denominator(second_rational)

  return make_rational(new_numerator, new_denominator)


def multiply_rational(
  first_rational: RationalNumber,
  second_rational: RationalNumber,
) -> RationalNumber:
  """first_rational * second_rational, returned in lowest terms."""

  new_numerator = numerator(first_rational) * numerator(second_rational)

  new_denominator = denominator(first_rational) * denominator(second_rational)

  return make_rational(new_numerator, new_denominator)


def equal_rational(
  first_rational: RationalNumber,
  second_rational: RationalNumber,
) -> bool:
  """True if the two rational numbers represent the same value."""

  return numerator(first_rational) == numerator(second_rational) and denominator(first_rational) == denominator(
    second_rational
  )


def rational_to_string(rational_number: RationalNumber) -> str:
  """e.g. RationalNumber(1, 2) -> "1/2"."""

  return f"{numerator(rational_number)}/{denominator(rational_number)}"


def total_claimed_share(
  shares: list[RationalNumber],
) -> RationalNumber:
  """Sum every share in the list into a single RationalNumber."""

  total = make_rational(0, 1)

  for share in shares:
    total = add_rational(total, share)

  return total


def is_bill_fully_claimed(
  shares: list[RationalNumber],
) -> bool:
  """True if total_claimed_share(shares) equals exactly one whole (1/1)."""

  return equal_rational(
    total_claimed_share(shares),
    make_rational(1, 1),
  )


# Quick manual checks
half = make_rational(1, 2)
third = make_rational(1, 3)

print(rational_to_string(add_rational(half, third)))  # 5/6
print(rational_to_string(multiply_rational(half, third)))  # 1/6
print(equal_rational(make_rational(2, 4), make_rational(1, 2)))  # True

diners = [
  make_rational(1, 4),
  make_rational(1, 4),
  make_rational(1, 2),
]

print(rational_to_string(total_claimed_share(diners)))  # 1/1
print(is_bill_fully_claimed(diners))  # True
