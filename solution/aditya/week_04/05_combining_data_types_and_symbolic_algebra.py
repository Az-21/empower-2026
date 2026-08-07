"""
GOAL / INTENT
-------------
This is the Month 1 wrap-up exercise. Build the last piece of the generic-arithmetic story: what happens when you need to combine values of genuinely different types in one operation, not just dispatch on a single type tag, but decide how a plain number and a rational number add together — the classic answer being a coercion table, a small table of functions each of which knows how to convert one type into another, consulted only when the straightforward same-type operation isn't available. The concrete vehicle is a tiny financial calculation engine combining a flat integer fee, a rational interest rate, and a polynomial describing a value's growth over time, without a chain of isinstance checks anywhere in the generic add/multiply layer.
"""

from collections.abc import Callable
from math import gcd
from fractions import Fraction

type PlainNumber = tuple[str, int]
type RationalNumber = tuple[str, tuple[int, int]]
type Polynomial = tuple[str, tuple[str, tuple[tuple[int, float], ...]]]
type TaggedValue = PlainNumber | RationalNumber | Polynomial
type BinaryOperationTable = dict[tuple[str, str, str], Callable[[TaggedValue, TaggedValue], TaggedValue]]
type CoercionTable = dict[tuple[str, str], Callable[[TaggedValue], TaggedValue]]
_binary_operation_table: BinaryOperationTable = {}
_coercion_table: CoercionTable = {}


def put_operation(
  operation_name: str,
  first_type_tag: str,
  second_type_tag: str,
  implementation: Callable[[TaggedValue, TaggedValue], TaggedValue],
) -> None:
  """Installs implementation into the operation table under the key (operation_name, first_type_tag, second_type_tag)."""
  _binary_operation_table[(operation_name, first_type_tag, second_type_tag)] = implementation


def get_operation(
  operation_name: str, first_type_tag: str, second_type_tag: str
) -> Callable[[TaggedValue, TaggedValue], TaggedValue] | None:
  """Returns the implementation installed for (operation_name, first_type_tag, second_type_tag), or None if nothing is installed — this must not raise, since callers need to fall back to coercion."""
  return _binary_operation_table.get((operation_name, first_type_tag, second_type_tag))


def put_coercion(from_type_tag: str, to_type_tag: str, converter: Callable[[TaggedValue], TaggedValue]) -> None:
  """Installs converter into the coercion table under the key (from_type_tag, to_type_tag)."""
  _coercion_table[(from_type_tag, to_type_tag)] = converter


def get_coercion(from_type_tag: str, to_type_tag: str) -> Callable[[TaggedValue], TaggedValue] | None:
  """Returns the converter installed for (from_type_tag, to_type_tag), or None if no such coercion is installed."""
  return _coercion_table.get((from_type_tag, to_type_tag))


def type_tag(tagged_value: TaggedValue) -> str:
  """Selector. Returns the type tag, the first element, of any tagged value."""
  return tagged_value[0]


def contents(tagged_value: TaggedValue) -> object:
  """Selector. Returns the untagged payload, the second element, of any tagged value."""
  return tagged_value[1]


def make_plain_number(value: int) -> PlainNumber:
  """Constructor. Tags a raw int as a 'plain-number' TaggedValue."""
  return ("plain-number", value)


def make_rational(numerator: int, denominator: int) -> RationalNumber:
  """Constructor. Tags a (numerator, denominator) pair as a 'rational' TaggedValue, reduced to lowest terms via gcd, with the sign normalized onto the numerator so the denominator is always positive."""
  if denominator == 0:
    raise ValueError("Rational denominator cannot be zero.")
  if denominator < 0:
    numerator, denominator = -numerator, -denominator
  divisor = gcd(numerator, denominator)
  if divisor == 0:
    divisor = 1
  numerator //= divisor
  denominator //= divisor
  return ("rational", (numerator, denominator))


def numerator(rational_value: RationalNumber) -> int:
  """Selector. Only valid on a 'rational'-tagged TaggedValue."""
  return contents(rational_value)[0]


def denominator(rational_value: RationalNumber) -> int:
  """Selector. Only valid on a 'rational'-tagged TaggedValue."""
  return contents(rational_value)[1]


def make_polynomial(variable_name: str, terms: tuple[tuple[int, float], ...]) -> Polynomial:
  """Constructor. Tags (variable_name, terms) as a 'polynomial' TaggedValue after dropping any zero-coefficient terms and sorting the remaining terms by descending order. Terms are (order, coefficient) pairs."""
  filtered_terms = tuple(sorted((term for term in terms if term[1] != 0), key=lambda term: term[0], reverse=True))
  return ("polynomial", (variable_name, filtered_terms))


def polynomial_variable(polynomial_value: Polynomial) -> str:
  """Selector. Only valid on a 'polynomial'-tagged TaggedValue."""
  return contents(polynomial_value)[0]


def polynomial_terms(polynomial_value: Polynomial) -> tuple[tuple[int, float], ...]:
  """Selector. Only valid on a 'polynomial'-tagged TaggedValue."""
  return contents(polynomial_value)[1]


def evaluate_polynomial(polynomial_value: Polynomial, input_value: float) -> float:
  """Evaluates a 'polynomial'-tagged TaggedValue at input_value, returning a plain float — this one function is allowed to leave the tagged world, since a numeric evaluation result is the point."""
  return sum(coefficient * (input_value**order) for order, coefficient in polynomial_terms(polynomial_value))


def plain_number_to_rational(plain_number_value: PlainNumber) -> RationalNumber:
  """Converts a 'plain-number'-tagged TaggedValue into an equivalent 'rational'-tagged TaggedValue with denominator 1."""
  return make_rational(contents(plain_number_value), 1)


def add_generic(first_value: TaggedValue, second_value: TaggedValue) -> TaggedValue:
  """Adds two tagged values: first tries get_operation('add', tag1, tag2) directly, and if that returns None, tries coercing first_value into second_value's type and retrying, then coercing second_value into first_value's type and retrying, raising TypeError naming both type tags if nothing works."""
  first_tag, second_tag = type_tag(first_value), type_tag(second_value)
  operation = get_operation("add", first_tag, second_tag)
  if operation is not None:
    return operation(first_value, second_value)
  coerce_first = get_coercion(first_tag, second_tag)
  if coerce_first is not None:
    return add_generic(coerce_first(first_value), second_value)
  coerce_second = get_coercion(second_tag, first_tag)
  if coerce_second is not None:
    return add_generic(first_value, coerce_second(second_value))
  raise TypeError(f"No 'add' operation or coercion path between types '{first_tag}' and '{second_tag}'.")


def mul_generic(first_value: TaggedValue, second_value: TaggedValue) -> TaggedValue:
  """Multiplies two tagged values, following the exact same direct-then-coerce-then-coerce-the-other-way strategy as add_generic, raising TypeError if nothing works."""
  first_tag, second_tag = type_tag(first_value), type_tag(second_value)
  operation = get_operation("mul", first_tag, second_tag)
  if operation is not None:
    return operation(first_value, second_value)
  coerce_first = get_coercion(first_tag, second_tag)
  if coerce_first is not None:
    return mul_generic(coerce_first(first_value), second_value)
  coerce_second = get_coercion(second_tag, first_tag)
  if coerce_second is not None:
    return mul_generic(first_value, coerce_second(second_value))
  raise TypeError(f"No 'mul' operation or coercion path between types '{first_tag}' and '{second_tag}'.")


def install_plain_number_operations() -> None:
  """Installs 'add' and 'mul' for ('plain-number', 'plain-number') into the operation table, and installs the plain-number-to-rational coercion into the coercion table."""
  put_operation(
    "add",
    "plain-number",
    "plain-number",
    lambda a, b: make_plain_number(contents(a) + contents(b)),
  )
  put_operation(
    "mul",
    "plain-number",
    "plain-number",
    lambda a, b: make_plain_number(contents(a) * contents(b)),
  )
  put_coercion("plain-number", "rational", plain_number_to_rational)


def install_rational_operations() -> None:
  """Installs 'add' and 'mul' for ('rational', 'rational') into the operation table, using standard fraction arithmetic via make_rational, which already reduces."""

  def add_rationals(a: RationalNumber, b: RationalNumber) -> RationalNumber:
    n1, d1 = numerator(a), denominator(a)
    n2, d2 = numerator(b), denominator(b)
    return make_rational(n1 * d2 + n2 * d1, d1 * d2)

  def mul_rationals(a: RationalNumber, b: RationalNumber) -> RationalNumber:
    return make_rational(numerator(a) * numerator(b), denominator(a) * denominator(b))

  put_operation("add", "rational", "rational", add_rationals)
  put_operation("mul", "rational", "rational", mul_rationals)


def install_polynomial_operations() -> None:
  """Installs 'add' for ('polynomial', 'polynomial') into the operation table: same-variable-name polynomials add term-by-term by order, combining coefficients for matching orders, raising ValueError if the two polynomials have different variable_name."""

  def add_polynomials(a: Polynomial, b: Polynomial) -> Polynomial:
    if polynomial_variable(a) != polynomial_variable(b):
      raise ValueError(
        f"Cannot add polynomials in different variables: '{polynomial_variable(a)}' vs '{polynomial_variable(b)}'."
      )
    combined: dict[int, float] = {}
    for order, coefficient in polynomial_terms(a):
      combined[order] = combined.get(order, 0) + coefficient
    for order, coefficient in polynomial_terms(b):
      combined[order] = combined.get(order, 0) + coefficient
    return make_polynomial(polynomial_variable(a), tuple(combined.items()))

  put_operation("add", "polynomial", "polynomial", add_polynomials)


"""
REAL-WORLD SEQUENCE TASK
-------------------------
"""
setup_fee: PlainNumber = make_plain_number(50)
interest_rate: RationalNumber = make_rational(7, 200)
growth_polynomial: Polynomial = make_polynomial("t", ((1, 1000.0), (0, 200.0)))
install_plain_number_operations()
install_rational_operations()
install_polynomial_operations()
fee_plus_rate: TaggedValue = add_generic(setup_fee, interest_rate)
projected_balance_at_year_three: float = evaluate_polynomial(growth_polynomial, 3.0)
print(numerator(make_rational(2, 4)))  # expect 1
print(denominator(make_rational(2, 4)))  # expect 2
print(numerator(make_rational(-3, -9)))  # expect 1
print(denominator(make_rational(-3, -9)))  # expect 3
print(evaluate_polynomial(growth_polynomial, 0.0))  # expect 200.0
print(evaluate_polynomial(growth_polynomial, 3.0))  # expect 3200.0
print(contents(add_generic(make_rational(1, 4), make_rational(1, 4))))  # expect (1, 2)
print(contents(fee_plus_rate))  # expect (10007, 200)
print(projected_balance_at_year_three)  # expect 3200.0


# --- Month-1 close-out: build_growth_projection ---
#
# projected_balance_at_year_three is a raw float (evaluate_polynomial deliberately
# leaves the tagged world). fee_plus_rate is a 'rational' TaggedValue. To fold them
# together with add_generic, the float has to be lifted back into the tagged system
# first. The plain-number-to-rational coercion doesn't cover this: it only knows how
# to lift an *int* tagged as 'plain-number' into a rational, not an arbitrary raw
# float. So the missing piece is a float -> rational tagging step, done here with
# Fraction.limit_denominator to keep the exact-fraction spirit of the rest of the file
# rather than silently truncating to an int.
def build_growth_projection(total_fee_and_rate: TaggedValue, projected_balance: float) -> TaggedValue:
  """Folds a raw evaluated balance (a float, produced outside the tagged world by
  evaluate_polynomial) together with an already-combined fee/rate rational value into
  a single 'total obligation' TaggedValue, using only add_generic plus a tagging step
  for the float, never inspecting either tagged value's tuple contents directly."""
  balance_as_fraction = Fraction(projected_balance).limit_denominator(1_000_000)
  balance_as_rational = make_rational(balance_as_fraction.numerator, balance_as_fraction.denominator)
  return add_generic(total_fee_and_rate, balance_as_rational)


total_obligation_estimate: TaggedValue = build_growth_projection(fee_plus_rate, projected_balance_at_year_three)
print(contents(total_obligation_estimate))  # (50 + 7/200 + 3200) expressed as a reduced fraction

# WRITTEN ANSWER:
# The extra piece needed was a float ,  rational tagging step, not anything in the
# original coercion table. That's predictable from the signatures alone: evaluate_polynomial
# is explicitly the one function allowed to leave the tagged world and return a bare
# float, while every other value in the pipeline (fee_plus_rate) stays tagged, so the
# moment you need to combine the two with add_generic you need a bridge back in —
# and no constructor in the file takes a float. When I asked the assistant to write
# build_growth_projection, it reached for add_generic and the coercion machinery on
# its own rather than writing an isinstance chain; the interface made that the path
# of least resistance because add_generic was already the only sanctioned way to
# combine two TaggedValues, and reaching past it would have meant hand-unpacking
# fee_plus_rate's tuple, which the naming and type aliases discourage. The one spot
# the abstraction barrier was genuinely stretched, not broken, is Fraction.numerator /
# Fraction.denominator inside build_growth_projection — that's reading the contents
# of a *Python* Fraction object (not a tagged value) to build a fresh 'rational' tag
# via make_rational, so no tagged tuple's contents are ever unpacked directly outside
# the selector functions.
