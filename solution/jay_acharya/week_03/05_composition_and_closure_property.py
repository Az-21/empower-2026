"""
GOAL / INTENT
-------------
Find a place where the closure property — an operation's output can be fed back in as its own input — lets small combinators build arbitrarily complex results, the same way Henderson's picture language builds complex images out of simple picture combinators (Lecture 3A).


TASK / IMPLEMENTATION
----------------------
Implement every function below. compose_transformations is the key closure operation: it takes Transformations and returns a Transformation, so its own output can always be passed right back into it or into another combinator.
"""

from collections.abc import Callable

Transformation = Callable[[str], str]


def compose_transformations(*transformations):
    """
    compose_transformations(f, g, h)(x)
    = f(g(h(x)))
    """

    def composed(value):
        result = value

        for transformation in reversed(transformations):
            result = transformation(result)

        return result

    return composed


def repeat_transformation(count: int):
    """Returns a Transformation that repeats its input string count times."""

    def repeat(text: str) -> str:
        return text * count

    return repeat


def join_with_separator(separator: str):
    """
    Returns a Transformation that joins a string with itself.
    Example:
    join_with_separator("-")("hi")
    -> "hi-hi"
    """

    def join(text: str) -> str:
        return f"{text}{separator}{text}"

    return join


def make_bold(text: str) -> str:
    """Markdown bold."""
    return f"**{text}**"


def make_italic(text: str) -> str:
    """Markdown italic."""
    return f"_{text}_"


def make_uppercase(text: str) -> str:
    """Uppercase text."""
    return text.upper()


"""
REAL-WORLD SEQUENCE TASK
"""


def format_all_headings(
    headings: list[str],
    formatting: Transformation,
) -> list:
    """Apply formatting to every heading."""
    return [formatting(heading) for heading in headings]


# Tests

emphasize = compose_transformations(
    make_bold,
    make_italic
)

print(emphasize("hello"))
# **_hello_**

shout_and_repeat = compose_transformations(
    repeat_transformation(2),
    make_uppercase
)

print(shout_and_repeat("go"))
# GOGO

headings = [
    "Introduction",
    "Methods",
    "Results",
    "Discussion",
]

print(format_all_headings(headings, emphasize))