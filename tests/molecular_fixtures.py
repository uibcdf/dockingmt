"""Copies of the existing explicitly declared 181L workflow for contract tests.

This reuses the qualified public MolSysMT workflow; it supplies no replacement
molecular algorithm. HIE and charged termini remain fixture hypotheses.
"""

from copy import deepcopy
from functools import lru_cache


@lru_cache(maxsize=1)
def _named_181l_pair():
    from devtools.qualify_181l_receptor import prepare_case

    receptor, ligand, _, _ = prepare_case()
    return receptor, ligand


def named_181l_pair():
    """Detach every test's mutable preparations from the shared fixture."""
    return deepcopy(_named_181l_pair())
