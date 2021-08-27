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
from typing      import Iterable, Iterator


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

    children: list[DnaBagNode | None]
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

    def __init__(self, items: Iterable[str] | None = None) -> None:
        """Initialize the DNABag.

        Args:
            items: DNA strings to add to the trie

        """
        self.root = DnaBagNode()
        if items is not None:
            for item in items:
                self.add(item)

    def add(self, key: str) -> int:
        """Insert key into the bag and return the number of times the key appears.

        Examples:
            >>> bag = DnaBag()
            >>> bag.add('A')
            1
            >>> bag.add('A')
            2
            >>> bag.add('ACGT')
            1
            >>> bag.add('GGG')
            1
            >>> bag.add('AC')
            1
            >>> bag.add('A')
            3

        """
        assert self.root is not None  # tells mypy about the invariant

        node: DnaBagNode = self.root

        for index in translate_dna(key):
            node.prefix_count += 1

            child = node.children[index]
            if child is None:
                child = node.children[index] = DnaBagNode()
            node = child

        node.prefix_count += 1
        node.value_count  += 1

        return node.value_count

    def __getitem__(self, key: str) -> int:
        """Get count of times key appears in the bag.

        Examples:
            >>> bag = DnaBag()
            >>> bag.add('A')
            1
            >>> bag.add('A')
            2
            >>> bag['A']
            2

        """
        node = self.root

        for index in translate_dna(key):
            child = node.children[index]
            if child is None:
                return 0
            node = child

        return node.value_count


def translate_dna(s: str) -> Iterator[int]:
    """Translate string characters to node child indexes.

    Examples:
        >>> list(translate_dna('C'))
        [1]
        >>> list(translate_dna('CAA'))
        [1, 0, 0]
        >>> list(translate_dna('ACGTN'))
        [0, 1, 2, 3, 4]
        >>> list(translate_dna('acgtn'))
        [0, 1, 2, 3, 4]

    """
    for character in s:
        yield DNA_MAP[character]


def traverse(node: DnaBagNode) -> Iterator[tuple[str, DnaBagNode]]:
    """Traverse the layers of the trie yielding base, node tuples.

    Args:
        node: node to begin traverse

    Yields:
        tuples of base and child node

    """
    for base, child in zip('ACGTN', node.children):
        if child:
            yield base, child
            yield from traverse(child)


def process_strings(strings: Iterable[str], targets: Iterable[str]) -> tuple[int, int]:
    """Calculate number of times a target character appears in one of the input strings using a DnaBag.

    Args:
        strings: list of DNA strings
        targets: target bases to count

    Examples:
        >>> strings = ['ACTG', 'AACT', 'TCAGG', 'TTGGA']
        >>> targets = ['C', 'G']
        >>> process_strings(strings, targets)
        (8, 18)

    """
    trie = DnaBag(strings)

    counts: dict[str, int] = defaultdict(int)
    for base, node in traverse(trie.root):
        counts[base] += node.prefix_count

    target_count = sum(counts[base] for base in targets)
    total_count  = sum(counts.values())

    return target_count, total_count


def run() -> None:
    """Run test case."""
    dna_strings = ['ACTGA', 'TAA', 'CTAA', 'TAAT', 'TAATT', 'ACT', 'ACTG']
    targets     = ['A', 'T']

    target_count, total_count = process_strings(dna_strings, targets)

    print(f"{', '.join(targets)} Fraction: {round(target_count / total_count, 2)} ({target_count}/{total_count})")


if __name__ == '__main__':
    run()
