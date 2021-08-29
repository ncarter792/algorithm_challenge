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


# Store map from DNA base to child list index (in order save memory and avoid using dictionaries)
ALPHABET = 'ACGNT'

DNA_MAP = {
    'a': 0, 'A': 0,
    'c': 1, 'C': 1,
    'g': 2, 'G': 2,
    'n': 3, 'N': 3,
    't': 4, 'T': 4,
}


class TrieNode:
    """Trie node to store a character in a DNA string (ACGNT).

    The class attributes include:
        children: list of child nodes corresponding to DNA alphabet ACGNT (TrieNode or None)
        item_count: number of items that pass through this node (including ones that end at this node)
        value_count: number of items that end at this node

    Each node is empty when it is first instantiated, containing an item count, a terminating value count, and
    a children attribute. The children attribute is instantiated as a list of 5 NoneType items - one index for each
    possible nucleotide. The index position for each nucleotide is defined by `DNA_MAP`, ie::

                    0     1     2     3     4
                    A/a   C/c  G/g   N/n   T/t
        children:[None, None, None, None, None]


    Example 1 - In this visual example, an empty TrieNode is first instantiated as empty (step 1), and then
    given child nodes as 'G' (step 2) and 'T' (step 3). In this example, `**/-------` indicates visual cues
    for changes between steps::

        # Step 1 - instantiate empty node
        node = {children:[None, None, None, None, None], item_count: 0, value_count:0}

        # Step 2 - Add child (G)          **                          **
        node = {children:[None, None, TrieNode(), None, None], item_count: 1, value_count:0}
                                      ----------               -------------
            # Note - An empty node at children[2]. item_count is 1 because one item (G) has passed through this node.

        # Step 3 - Add child (T)                            **             **
        node = {children:[None, None, TrieNode(), None, TrieNode()], item_count: 2, value_count:0}
                                                        ----------   -------------
            # Note - An empty node at children[4]. item_count is 2 because two items (G, T), have passed through this node.

    """

    # Important to minimize memory usage
    __slots__ = (
        'children',
        'item_count',
        'value_count',
    )

    # Declare attribute types
    children: list[TrieNode | None]
    item_count: int
    value_count: int

    def __init__(self) -> None:
        """Initialize an empty TrieNode."""
        # Utilizing a list of defined length with specified index rather than dict to minimize memory usage
        self.children = [None] * 5

        self.item_count = 0
        self.value_count = 0


class DnaTrie:
    """Data structure to store and process TrieNodes, where the root is the top node.

    The implementation is a standard trie data structure with the following customizations:
      * the value of each node is the count of strings ending at that node (DnaTrieNode.value_count)
      * the number of strings that pass through each node is also stored (DnaTrieNode.item_count)

    Backround material:
      * tries: https://en.wikipedia.org/wiki/Trie

    """

    def __init__(self, items: Iterable[str] | None = None) -> None:
        """Initialize the DnaTrie.

        Args:
            items: DNA strings to add to the trie

        """
        self.root = TrieNode()
        if items is not None:
            for item in items:
                self.add(item)

    def add(self, key: str) -> int:
        """Insert key into the bag and return the number of times the key appears.

        Examples:
            >>> bag = DnaTrie()
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

        node: TrieNode = self.root

        for index in translate_dna(key):
            node.item_count += 1

            child = node.children[index]
            if child is None:
                child = node.children[index] = TrieNode()
            node = child

        node.item_count += 1
        node.value_count  += 1

        return node.value_count

    def __getitem__(self, key: str) -> int:
        """Get count of times key appears in the bag.

        Examples:
            >>> bag = DnaTrie()
            >>> bag.add('A')
            1
            >>> bag.add('A')
            2
            >>> bag['A']
            2
            >>> bag['T']
            0

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
        >>> list(translate_dna('ACGNT'))
        [0, 1, 2, 3, 4]
        >>> list(translate_dna('acgnt'))
        [0, 1, 2, 3, 4]

    """
    for character in s:
        yield DNA_MAP[character]


def traverse(node: TrieNode) -> Iterator[tuple[str, TrieNode]]:
    """Traverse the layers of the trie yielding base, node tuples.

    Args:
        node: node to begin traverse

    Yields:
        tuples of base and child node

    """
    for base, child in zip(ALPHABET, node.children):
        if child:
            yield base, child
            yield from traverse(child)


def process_trie(trie: DnaTrie, targets: Iterable[str]) -> tuple[int, int]:
    """Calculate number of times a target character appears in one of the input strings using a DnaTrie.

    Args:
        strings: list of DNA strings
        targets: target bases to count

    Examples:
        >>> from algorithm_challenge.algorithm_challenge import DnaTrie
        >>> test = DnaTrie(['ACTG', 'AACT', 'TCAGG', 'TTGGA'])
        >>> targets = ['C', 'G']
        >>> process_trie(test, targets)
        (8, 18)

    """
    counts: dict[str, int] = defaultdict(int)
    for base, node in traverse(trie.root):
        counts[base] += node.item_count

    target_count = sum(counts[base] for base in targets)
    total_count  = sum(counts.values())

    return target_count, total_count


def pretty_print(
    node: TrieNode,
    item_prefix: str = '',
    tree_prefix: str = '',
    last: bool = True,
    indent: int = 2,
) -> Iterator[str]:
    """Pretty print trie.

    This function is most helpful for debugging to visually make sure that the tree is built correctly.

    Args:
        node: node to start pretty print
        item_prefix: prefix of values up to current node
        tree_prefix: tree printing characters
        last: node is last child of parent
        indent: number of spaces to indent tree formatting

    """
    connector = '└─' if last else '├─'
    star = ' *' if node.value_count else ''

    check  = [c for c in node.children if c is not None]
    output = f'TrieNode(values={node.value_count}, items={node.item_count}, children={len(check)})'

    yield f'{tree_prefix}{connector} [{item_prefix}]: {output}{star}'

    tree_prefix += (' ' if last else '│') + ' '*indent
    children = [(base, child) for base, child in zip(ALPHABET, node.children) if child is not None]

    for i, (child_base, child) in enumerate(children, 1):
        yield from pretty_print(child, item_prefix + child_base, tree_prefix, i == len(children), indent)


def run() -> None:
    """Run test case."""
    dna_strings = ['ACTGA', 'TAA', 'CTAA', 'TAAT', 'TAATT', 'ACT', 'ACTG']
    targets     = ['A', 'T']

    trie = DnaTrie(dna_strings)

    # Debugging output - in a perfect example, this would be CLI configurable
    print('\n'.join(pretty_print(trie.root)))

    target_count, total_count = process_trie(trie, targets)

    print(f"{', '.join(targets)} Fraction: {round(target_count / total_count, 2)} ({target_count}/{total_count})")


if __name__ == '__main__':
    run()
