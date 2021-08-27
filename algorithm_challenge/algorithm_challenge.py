"""Algorithm challenge for Delfi Diagnostics.

This module implements a method that generates a trie given a set of characters, and returns the fraction of letters
in the list of strings used to build the trie that are members of the target set of characters.

Challenge description:
    "A trie is a data structure that can be used to represent a collection of strings. Implement a trie
    that in addition tracks the number of times each string occurred in the set used to construct the
    trie. Python can be very memory inefficient; please consider memory efficiency in your trie
    implementation, so that it can be used to represent large collections of strings. For purposes of
    this exercise, assume that the trie will represent DNA sequences, and all strings will be built
    from the alphabet {A,C,G,T,N}."

Note - this module is written using Python 3.9. It can be run with both flake8 and mypy to verify style and typing.
Doctests can be executed via: `python -m doctest -v algorithm_challenge_.py`.

"""

from __future__ import annotations

from collections import defaultdict
from typing      import Dict, Iterable, Iterator, Optional, Tuple


# Store map from base to child index
DNA_MAP = {
    'a': 0, 'A': 0,
    'c': 1, 'C': 1,
    'g': 2, 'G': 2,
    't': 3, 'T': 3,
    'n': 4, 'N': 4,
}


class DnaBagNode:
    """Data structure to store node metrics and children.

    Children is instantiated as a list of 5 items - one index for each possible nucleotide. These indexes are defined by
    DNA_MAP. As nucleotides are observed, child nodes are generated at the corresponding index.

    The class attributes include:
        children: child nodes, if present
        prefix_count: observations of given node
        value_count: complete string count

    """

    __slots__ = (
        'children',
        'prefix_count',
        'value_count',
    )

    children: Iterable[DnaBagNode | None]
    prefix_count: int
    value_count: int

    def __init__(self) -> None:
        """Initialize an empty DnaBagNode."""
        self.children = [None] * 5
        self.prefix_count = 0
        self.value_count = 0


class DnaBag:
    """Data structure to store and process DNABagNodes, where the root is the top node.

    Background for the trie data structure implemented in this object is available here: https://en.wikipedia.org/wiki/Trie.

    """

    def __init__(self, items: Iterable[str] | None) -> None:
        """Initialize the DNABag.

        Args:
            items: DNA strings to add to the trie

        """
        self.root = DnaBagNode()
        if items is not None:
            for item in items:
                self.add(item)

    def add(self, key: str) -> None:
        """Insert key into node."""
        node = self.root

        child_index = translate_dna(key)

        for index in child_index:
            node.prefix_count += 1

            if not node.children[index]:
                node.children[index] = DnaBagNode()

            node = node.children[index]

        node.value_count += 1
        node.prefix_count += 1

    def find(self, key: str) -> Optional[int]:
        """Find value by key in node."""
        for character in key:
            if character in self.root.children:
                node = self.root.children[character]
            else:
                return None

        return node.value


def translate_dna(s: str) -> Iterator[int]:
    """Translate string characters to node child indexes.

    Examples:
        >>> translate_dna('C')
        1
        >>> list(translate_dna('CAA')
        [1, 0, 0]

    """
    for character in s:
        yield DNA_MAP[character]


def traverse(node: DnaBagNode) -> Iterable[Tuple[str, DnaBagNode]]:
    """Traverse the layers of the trie yielding base, node tuples."""
    for base, child in zip('ACGTN', node.children):
        if child:
            yield (base, child)
            yield from traverse(child)


def process_strings(strings: Iterable[str], targets: Iterable[str]) -> Tuple[int, int]:
    """Calculate processed string target count.

    # FIXME - Doctest failing.
    Example:
    >>> strings = ['ACTG', 'AACT', 'TCAGG', 'TTGGA']
    >>> targets = ['C', 'G']
    >>> process_strings(strings, targets)
    (8, 18)

    Args:
        strings: list of DNA strings
        targets: target bases to count

    """
    trie = DnaBag(strings)

    counts: Dict[str, int] = defaultdict(int)
    for base, node in traverse(trie.root):
        counts[base] += node.prefix_count

    target_count = sum(counts[base] for base in targets)
    total_count  = sum(counts.values())

    return target_count, total_count


def run() -> None:
    """Recipe function."""
    dna_strings = ['ACTGA', 'TAA', 'CTAA', 'TAAT', 'TAATT', 'ACT', 'ACTG']
    targets     = ['A', 'T']

    target_count, total_count = process_strings(dna_strings, targets)

    print(f"{', '.join(targets)} Fraction: {round(target_count / total_count, 2)} ({target_count}/{total_count})")


if __name__ == '__main__':
    run()
