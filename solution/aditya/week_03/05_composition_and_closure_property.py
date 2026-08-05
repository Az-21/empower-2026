from collections.abc import Callable

type Transformation[T] = Callable[[T], T]


def compose_transformations[T](*transformations: Transformation[T]) -> Transformation[T]:
  """Combine transformations so that compose_transformations(first, second, third)(value)
  equals first(second(third(value))). This is the closure property: the result is
  itself a Transformation, so it can be composed again."""

  def composed(value: T) -> T:
    result = value
    for transformation in reversed(transformations):
      result = transformation(result)
    return result

  return composed


def repeat_transformation(count: int) -> Transformation[str]:
  """Returns a Transformation that repeats its input string `count` times
  with no separator. Higher-order: this function returns a Transformation,
  it does not take one."""

  def repeat(text: str) -> str:
    return text * count

  return repeat


def join_with_separator(separator: str) -> Transformation[str]:
  """Returns a Transformation that joins its input string with itself,
  placing `separator` between the two copies."""

  def join(text: str) -> str:
    return text + separator + text

  return join


def make_bold(text: str) -> str:
  """A plain Transformation: wraps text in Markdown bold markers."""
  return f"**{text}**"


def make_italic(text: str) -> str:
  """A plain Transformation: wraps text in Markdown italic markers."""
  return f"_{text}_"


def make_uppercase(text: str) -> str:
  """A plain Transformation: uppercases the text."""
  return text.upper()


def format_all_headings(headings: list[str], formatting: Transformation[str]) -> list[str]:
  """Apply `formatting` to every heading in the list."""
  return [formatting(heading) for heading in headings]


emphasize = compose_transformations(make_bold, make_italic)
print(emphasize("hello"))  # expect **_hello_**
shout_and_repeat = compose_transformations(repeat_transformation(2), make_uppercase)
print(shout_and_repeat("go"))  # expect GOGO
headings = ["Introduction", "Methods", "Results", "Discussion"]
print(format_all_headings(headings, emphasize))
