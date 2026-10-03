"""Owned meanings of the four retained columns of Vina.energies()."""


def score_components(scoring):
    return {
        scoring: 'total docking score',
        'inter': 'intermolecular term',
        'intra': 'intramolecular term',
        'torsion': 'torsional term',
    }
