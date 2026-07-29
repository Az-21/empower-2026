"""
GOAL / INTENT
-------------
Build interval arithmetic as a data abstraction (a value paired with its uncertainty range), then use it to define a real list-processing task cleanly over a sequence — never by reaching into an interval's bounds by hand.

TASK / IMPLEMENTATION
----------------------
Implement every function below. Everything after the constructor/selector section must be built exclusively out of make_interval, lower_bound, and upper_bound.
"""

from dataclasses import dataclass
from functools import reduce


@dataclass(frozen=True, slots=True)
class Interval:
  """An interval of possible values, from a lower bound to an upper bound."""
  
  _lower_bound: float
  _upper_bound: float


def make_interval(lower_value: float, upper_value: float) -> Interval:
  if lower_value > upper_value:
    raise ValueError("Lower bound cannot be greater than upper bound.")
  return Interval(lower_value, upper_value)
  """Constructor. Raise ValueError if lower_value > upper_value."""

  raise NotImplementedError


def lower_bound(interval_value: Interval) -> float:
  return interval_value._lower_bound
  """Selector."""
  raise NotImplementedError


def upper_bound(interval_value: Interval) -> float:
  return interval_value._upper_bound
  """Selector. """
  raise NotImplementedError


def add_interval(first_interval: Interval, second_interval: Interval) -> Interval:
  lower = lower_bound(first_interval) + lower_bound(second_interval)
  upper = upper_bound(first_interval) + upper_bound(second_interval)
  return make_interval(lower, upper)
  """ make_interval works as a abstraction between our code and constructor"""
  raise NotImplementedError


def multiply_interval(first_interval: Interval, second_interval: Interval) -> Interval:
    products =[ 
      lower_bound(first_interval) * lower_bound(second_interval),
      lower_bound(first_interval) * upper_bound(second_interval),
      upper_bound(first_interval) * lower_bound(second_interval),
      upper_bound(first_interval) * upper_bound(second_interval)
    ]
    """Result bounds are the min/max over all four combinations of the input bounds (needed because bounds may be negative)."""
    return make_interval(min(products), max(products))
    raise NotImplementedError


def divide_interval(first_interval: Interval, second_interval: Interval) -> Interval:
    if lower_bound(second_interval) <=0 and upper_bound(second_interval) >=0:
        raise ValueError("cannot divide by zero")
    reciprocal = make_interval( 
        1/upper_bound(second_interval),
        1/lower_bound(second_interval)
    )
    return multiply_interval(first_interval, reciprocal)
   
    """
    Divide by multiplying by the reciprocal interval. Raise ValueError if second_interval spans zero (i.e. lower_bound <= 0 <= upper_bound)."""
    raise NotImplementedError


def width_of_interval(interval_value: Interval) -> float:
    return (upper_bound(interval_value) - lower_bound(interval_value)) / 2
    """
    Half the distance between the bounds — a measure of uncertainty."""
    raise NotImplementedError


"""
REAL-WORLD SEQUENCE TASK
-------------------------
You are computing the combined resistance of an arbitrary number of resistors wired in parallel, where each resistor's true resistance is only known within a tolerance range (an Interval). The parallel-resistance formula is:

    R_parallel = 1 / (1/R_1 + 1/R_2 + ... + 1/R_n)

Implement this over a list of Interval values, using ONLY the interval operations defined above (no direct access to _lower_bound/_upper_bound).
"""


def parallel_resistance(resistors: list[Interval]) -> Interval:
  if not resistors:
        raise ValueError("Need at least one resistor")

  reciprocals = []

  for resistor in resistors:
        if lower_bound(resistor) <= 0 <= upper_bound(resistor):
            raise ValueError("Resistance interval cannot span zero")

        reciprocals.append(
            make_interval(
                1 / upper_bound(resistor),
                1 / lower_bound(resistor),
            )
        )

  reciprocal_sum = reduce(add_interval, reciprocals)

  return divide_interval(
        make_interval(1, 1),
        reciprocal_sum,
    )
  """Combine an arbitrary-length list of resistor Intervals into one equivalent-resistance Interval, wired in parallel."""
  raise NotImplementedError

  """1/10.2 = 0.0980, 1/9.8 = 0.1020, order changes, reciprocal happens, like 10.2->0.98, 9.8->0.102"""
resistor_one = make_interval(9.8, 10.2)
resistor_two = make_interval(19.7, 20.3)

combined = add_interval(resistor_one, resistor_two)
print(lower_bound(combined), upper_bound(combined))  # expect ~29.5, 30.5

result = parallel_resistance([resistor_one, resistor_two])
print(lower_bound(result), upper_bound(result))
print(width_of_interval(result))
