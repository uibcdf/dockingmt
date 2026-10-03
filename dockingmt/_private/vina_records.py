"""Owned column meanings of Vina docking and fixed-pose scoring records."""

SCORING_COMPONENTS = (
    'total',
    'lig_inter',
    'flex_inter',
    'other_inter',
    'flex_intra',
    'lig_intra',
    'torsions',
    'lig_intra_best_pose',
)


def fixed_score_components(score_name):
    """Names and meanings of the eight Vina/Vinardo Vina.score() columns."""
    return {
        score_name if index == 0 else f'{score_name}.{component}': component
        for index, component in enumerate(SCORING_COMPONENTS)
    }


def score_components(scoring):
    """Names and meanings of the four retained Vina.energies() columns."""
    return {
        scoring: 'total docking score',
        'inter': 'intermolecular term',
        'intra': 'intramolecular term',
        'torsion': 'torsional term',
    }
