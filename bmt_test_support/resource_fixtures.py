"""Finite shared test factories relocated from tests/test_molecular_variant_ownership.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""


class UnavailableResource:
    def __deepcopy__(self, memo):
        raise RuntimeError('test resource cannot be copied')
