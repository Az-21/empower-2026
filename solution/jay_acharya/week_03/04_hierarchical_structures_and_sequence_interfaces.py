"""
GOAL / INTENT
-------------
Re-express a nested-data task two ways: first as explicit recursion over the tree structure (the direct approach), then again as a chain of sequence operations (map / filter / reduce) — and see how much clearer the second version is once the traversal problem has been solved once.


TASK / IMPLEMENTATION
----------------------
Implement every function below. Do "Version A" (explicit recursion) first, then "Version B" (sequence operations), and keep both — do not delete Version A once Version B works.
"""

from functools import reduce
from typing import TypeVar

T = TypeVar("T")

type Tree = T | list


# --- Version A: explicit recursion -------------------------------------------

def count_leaves_by_recursion(tree) -> int:
    """Count every leaf in the tree using direct recursion."""
    if not isinstance(tree, list):
        return 1

    return sum(count_leaves_by_recursion(subtree) for subtree in tree)


def flatten_tree(tree) -> list:
    """Flatten arbitrary nesting into a single flat list of leaves."""

    if not isinstance(tree, list):
        return [tree]

    result = []

    for subtree in tree:
        result.extend(flatten_tree(subtree))

    return result


# --- Version B: sequence operations, built on top of flatten_tree -----------

def count_leaves_by_sequence_operations(tree) -> int:
    """Count leaves using sequence operations only."""
    return len(flatten_tree(tree))


"""
REAL-WORLD SEQUENCE TASK
"""

organization_chart = [
    "Chief Executive Officer",
    [["Vice President of Engineering"],
     ["Staff Engineer A", "Staff Engineer B", ["Intern"]]],
    [["Vice President of Sales"],
     ["Account Executive One", "Account Executive Two"]],
]


def titles_matching(tree, keyword: str) -> list:
    """Return every title containing keyword (case-insensitive)."""
    keyword = keyword.lower()

    return [
        title
        for title in flatten_tree(tree)
        if keyword in title.lower()
    ]


def count_titles_matching(tree, keyword: str) -> int:
    """Count matching titles without new recursion."""

    return len(titles_matching(tree, keyword))


# Tests

print(count_leaves_by_recursion(organization_chart))  # 8

print(count_leaves_by_sequence_operations(
    organization_chart
))  # 8

print(flatten_tree(organization_chart))

print(titles_matching(organization_chart, "Engineer"))

print(count_titles_matching(
    organization_chart,
    "Engineer"
))  # 3