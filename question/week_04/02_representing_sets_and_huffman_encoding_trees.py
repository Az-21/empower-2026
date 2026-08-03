"""
GOAL / INTENT
-------------
Build two related skills: that "a set" is an interface — element_of_set, adjoin_set, union_set, intersection_set — that can be backed by different underlying representations, with the right choice depending on the access pattern you actually need rather than habit, and that a binary tree can itself be built from ordinary constructors and selectors, with Huffman encoding trees as a concrete worked example of choosing a representation specifically to exploit uneven frequencies in real data.

TASK / IMPLEMENTATION
----------------------
Sets of alert codes below are represented as sorted tuples rather than unordered lists or binary search trees: for a fixed-size, fairly small set of live alert codes on an embedded IoT gateway, checked for membership and deduplicated far more often than it is mutated, a sorted list gives near-logarithmic membership tests without the pointer bookkeeping a real tree representation would cost on constrained hardware, at the price of an O(n) adjoin_set where an unordered list would have made insertion O(1) — a trade worth making since membership and dedup are the hotter path here. Implement every function below. Everything from make_code_tree onward must be built exclusively out of make_leaf, is_leaf, symbol_leaf, weight_leaf, make_code_tree, left_branch, right_branch, symbols, and weight — never by indexing into a raw tuple directly.
"""

from collections.abc import Sequence

type HuffmanLeaf = tuple[str, str, int]
type HuffmanTree = tuple[str, HuffmanLeaf | HuffmanTree, HuffmanLeaf | HuffmanTree, list[str], int]


def element_of_set(alert_code: str, alert_set: Sequence[str]) -> bool:
  """True if alert_code appears in alert_set, which is assumed to already be sorted ascending."""
  raise NotImplementedError


def adjoin_set(alert_code: str, alert_set: Sequence[str]) -> tuple[str, ...]:
  """Return a new sorted tuple containing alert_set's elements plus alert_code, with no duplicate inserted if alert_code is already present."""
  raise NotImplementedError


def union_set(first_alert_set: Sequence[str], second_alert_set: Sequence[str]) -> tuple[str, ...]:
  """Return a new sorted tuple containing every alert code present in either input set, with no duplicates."""
  raise NotImplementedError


def intersection_set(first_alert_set: Sequence[str], second_alert_set: Sequence[str]) -> tuple[str, ...]:
  """Return a new sorted tuple containing only alert codes present in both input sets."""
  raise NotImplementedError


def make_leaf(symbol: str, weight: int) -> HuffmanLeaf:
  """Constructor. Tags a leaf node as 'leaf', holding one alert symbol and its observed frequency weight."""
  raise NotImplementedError


def is_leaf(node: HuffmanLeaf | HuffmanTree) -> bool:
  """True if node is a leaf per make_leaf's tag, False if it is an interior code-tree node."""
  raise NotImplementedError


def symbol_leaf(leaf: HuffmanLeaf) -> str:
  """Selector. Only valid when is_leaf(leaf) is True."""
  raise NotImplementedError


def weight_leaf(leaf: HuffmanLeaf) -> int:
  """Selector. Only valid when is_leaf(leaf) is True."""
  raise NotImplementedError


def make_code_tree(left: HuffmanLeaf | HuffmanTree, right: HuffmanLeaf | HuffmanTree) -> HuffmanTree:
  """Constructor. Builds an interior node from a left and right subtree, computing, and storing the combined symbol list and combined weight so symbols() and weight() do not need to re-walk the whole tree each call."""
  raise NotImplementedError


def left_branch(tree: HuffmanTree) -> HuffmanLeaf | HuffmanTree:
  """Selector."""
  raise NotImplementedError


def right_branch(tree: HuffmanTree) -> HuffmanLeaf | HuffmanTree:
  """Selector."""
  raise NotImplementedError


def symbols(node: HuffmanLeaf | HuffmanTree) -> list[str]:
  """Return every alert symbol reachable from node, whether node is a leaf or an interior node, dispatching on is_leaf rather than assuming node's shape."""
  raise NotImplementedError


def weight(node: HuffmanLeaf | HuffmanTree) -> int:
  """Return the total weight of node, whether node is a leaf or an interior node, dispatching on is_leaf rather than assuming node's shape."""
  raise NotImplementedError


def adjoin_leaf_set(
  leaf: HuffmanLeaf, leaf_set: Sequence[HuffmanLeaf | HuffmanTree]
) -> tuple[HuffmanLeaf | HuffmanTree, ...]:
  """Return a new tuple with leaf inserted into leaf_set, keeping the whole collection sorted ascending by weight() — this ordering is what lets generate_huffman_tree always merge the two lowest-weight items first."""
  raise NotImplementedError


def make_leaf_set(symbol_weight_pairs: Sequence[tuple[str, int]]) -> tuple[HuffmanLeaf, ...]:
  """Turn a sequence of (symbol, weight) pairs into a weight-sorted tuple of leaves, built by repeated adjoin_leaf_set calls."""
  raise NotImplementedError


def generate_huffman_tree(symbol_weight_pairs: Sequence[tuple[str, int]]) -> HuffmanLeaf | HuffmanTree:
  """Build the full Huffman tree: start from make_leaf_set, then repeatedly remove the two lowest-weight items and replace them with make_code_tree of the two, re-inserting via adjoin_leaf_set, until exactly one node remains, and return that node."""
  raise NotImplementedError


def choose_branch(bit: int, tree: HuffmanTree) -> HuffmanLeaf | HuffmanTree:
  """Return left_branch(tree) if bit == 0, right_branch(tree) if bit == 1, and raise ValueError for any other bit value."""
  raise NotImplementedError


def decode(bits: Sequence[int], tree: HuffmanLeaf | HuffmanTree) -> list[str]:
  """Decode a flat sequence of 0/1 bits against tree into the list of alert symbols it represents, by walking from the root down to a leaf, emitting that leaf's symbol, and restarting from the root for the next symbol, until bits is exhausted."""
  raise NotImplementedError


def encode_symbol(symbol: str, tree: HuffmanLeaf | HuffmanTree) -> list[int]:
  """Return the bits that encode a single symbol under tree, by searching from the root: at each interior node, recurse left if symbol is among symbols(left_branch(tree)), otherwise recurse right, raising ValueError if symbol is not present in the tree at all."""
  raise NotImplementedError


def encode(message: Sequence[str], tree: HuffmanLeaf | HuffmanTree) -> list[int]:
  """Encode a full sequence of alert symbols against tree by concatenating encode_symbol results in order."""
  raise NotImplementedError


"""
REAL-WORLD SEQUENCE TASK
-------------------------
An IoT gateway receives alert codes from two sensor clusters over the same minute. Combine the two clusters' active alerts with union_set and intersection_set, then compress this minute's alerts for transmission over the gateway's low-bandwidth uplink by building a Huffman tree from a month of historical alert frequencies and encoding the deduplicated alert set against it, confirming that decoding the transmission reconstructs the original list.
"""

cluster_a_alerts: tuple[str, ...] = ("LOW_BATTERY", "TEMP_HIGH", "OFFLINE")
cluster_b_alerts: tuple[str, ...] = ("TEMP_HIGH", "VIBRATION", "OFFLINE")
all_active_alerts: tuple[str, ...] = union_set(cluster_a_alerts, cluster_b_alerts)
alerts_on_both_clusters: tuple[str, ...] = intersection_set(cluster_a_alerts, cluster_b_alerts)

alert_frequencies: tuple[tuple[(str, int)], ...] = (
  ("LOW_BATTERY", 5),
  ("TEMP_HIGH", 30),
  ("OFFLINE", 10),
  ("VIBRATION", 55),
)
alert_huffman_tree: HuffmanTree | HuffmanLeaf = generate_huffman_tree(alert_frequencies)
encoded_transmission: list[int] = encode(list(all_active_alerts), alert_huffman_tree)
decoded_transmission: list[str] = decode(encoded_transmission, alert_huffman_tree)

print(element_of_set("TEMP_HIGH", ("LOW_BATTERY", "OFFLINE", "TEMP_HIGH")))  # expect True
print(adjoin_set("OFFLINE", ("LOW_BATTERY", "TEMP_HIGH")))  # expect ('LOW_BATTERY', 'OFFLINE', 'TEMP_HIGH')
print(union_set(cluster_a_alerts, cluster_b_alerts))  # expect ('LOW_BATTERY', 'OFFLINE', 'TEMP_HIGH', 'VIBRATION')
print(intersection_set(cluster_a_alerts, cluster_b_alerts))  # expect ('OFFLINE', 'TEMP_HIGH')

sample_tree = generate_huffman_tree((("A", 1), ("B", 1), ("C", 2)))
print(symbols(sample_tree))  # expect some ordering containing 'A', 'B', 'C'
print(weight(sample_tree))  # expect 4
print(decode(encode(["A", "B", "C", "A"], sample_tree), sample_tree))  # expect ['A', 'B', 'C', 'A']

print(all_active_alerts)  # expect ('LOW_BATTERY', 'OFFLINE', 'TEMP_HIGH', 'VIBRATION')
print(alerts_on_both_clusters)  # expect ('OFFLINE', 'TEMP_HIGH')
print(decoded_transmission == list(all_active_alerts))  # expect True
