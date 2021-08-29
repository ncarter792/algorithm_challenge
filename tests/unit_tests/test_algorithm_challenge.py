"""This module contains unit test code for algorithm_challenge.py."""

from __future__ import annotations

from collections import defaultdict
from typing      import Any, Iterable

from pytest import mark, raises

from algorithm_challenge.algorithm_challenge import DnaTrie, translate_dna, traverse, process_trie


@mark.parametrize('test_input, expected_output', [
    # Test single strings
    ('a', [0]),
    ('A', [0]),

    # Test simple conversions
    ('AAA', [0, 0, 0]),
    ('ACG', [0, 1, 2]),
    ('CGT', [1, 2, 4]),

    # Test empty
    ('', []),
])
def test_translate_dna(test_input: str, expected_output: Iterable[int]) -> None:
    """Verify translate_dna function behaves as expected."""
    assert list(translate_dna(test_input)) == expected_output


@mark.parametrize('test_input, expected_error', [
    # Test non-allowed inputs
    ('B',  KeyError),
    (1,    TypeError),
    (None, TypeError),
])
def test_translate_dna_fails(test_input: Any, expected_error: Any) -> None:
    """Verify that translate_dna fails when given a disallowed input."""
    with raises(expected_error):
        list(translate_dna(test_input))


def test_DnaTrie() -> None:
    """Verify a DnaTrie is setup as expected.

    Note - Child attribute indexes are: [A, C, G, N, T]

    """
    test_strs = ['AAC', 'AA', 'TG', 'C']
    bag = DnaTrie(test_strs)

    # Test top level node
    assert bag.root.item_count == 4    # Three strings generate suffixes from the root node
    assert bag.root.value_count  == 0    # root has no value

    assert not bag.root.children[2]  # Test G
    assert not bag.root.children[3]  # Test N

    # Test sub-node A
    a = bag.root.children[0]
    assert a
    assert a.item_count == 2
    assert a.value_count  == 0

    aa = a.children[0]
    assert aa
    assert aa.item_count == 2
    assert aa.value_count  == 1

    aac = aa.children[1]
    assert aac
    assert aac.item_count == 1
    assert aac.value_count  == 1

    # Test sub-node C
    c = bag.root.children[1]
    assert c
    assert c.item_count == 1
    assert c.value_count  == 1

    # Test sub-node T
    t = bag.root.children[4]
    assert t
    assert t.item_count == 1
    assert t.value_count  == 0

    tg = t.children[2]
    assert tg
    assert tg.item_count == 1
    assert tg.value_count  == 1


@mark.parametrize('test_strs, expected_counts', [
    (['A'],       {'A': 1}),
    (['A', 'T'],  {'A': 1, 'T': 1}),
    (['AA'],      {'A': 2}),
    (['AA', 'A'], {'A': 3}),
    (['AA', 'A', 'TA'],        {'A': 4, 'T': 1}),
    (['AAC', 'AA', 'TG', 'C'], {'A': 4, 'C': 2, 'T': 1, 'G': 1}),
    (['ACTGA', 'TAA', 'CTAA', 'TAAT', 'TAATT', 'ACT', 'ACTG'], {'A': 12, 'C': 4, 'T': 10, 'G': 2}),
])
def test_traverse(test_strs: Iterable[str], expected_counts: dict[str, int]) -> None:
    """Verify that traverse unpacks a trie as expecetd."""
    bag = DnaTrie(test_strs)

    counts: dict[str, int] = defaultdict(int)
    for base, node in traverse(bag.root):
        counts[base] += node.item_count

    assert counts == expected_counts


@mark.parametrize('test_nodes, targets, expected_counts', [
    (DnaTrie(['A']),       ['A'], (1, 1)),
    (DnaTrie(['A']),       ['G'], (0, 1)),
    (DnaTrie(['A', 'T']),  ['A'], (1, 2)),
    (DnaTrie(['AA']),      ['A'], (2, 2)),
    (DnaTrie(['AA']),      ['C'], (0, 2)),
    (DnaTrie(['AA', 'A']), ['A'], (3, 3)),

    (DnaTrie(['A', 'T']),               ['A', 'T'], (2, 2)),
    (DnaTrie(['AA', 'A', 'TA']),        ['T'],      (1, 5)),
    (DnaTrie(['AAC', 'AA', 'TG', 'C']), ['T', 'C'], (3, 8)),

    (DnaTrie(['ACTGA', 'TAA', 'CTAA', 'TAAT', 'TAATT', 'ACT', 'ACTG']), ['T', 'C'], (14, 28)),
    (DnaTrie(['ACTGA', 'TAA', 'CTAA', 'TAAT', 'TAATT', 'ACT', 'ACTG']), ['T', 'A'], (22, 28)),
    (DnaTrie(['ACTGA', 'TAA', 'CTAA', 'TAAT', 'TAATT', 'ACT', 'ACTG']), ['N'],      (0, 28)),
])
def test_process_trie(test_nodes: DnaTrie, targets: Iterable[str], expected_counts: tuple[int, int]) -> None:
    """Verify that proces_strings generates the correct counts."""
    assert process_trie(test_nodes, targets) == expected_counts
