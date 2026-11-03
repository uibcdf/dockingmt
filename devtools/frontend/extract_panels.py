"""Read the shipped panel modules without importing scientific dependencies."""

import ast
import json
import sys
from pathlib import Path


def panel_sources(root: Path) -> dict[str, str]:
    """Return the literal production ESM; refuse unsupported declarations."""
    sources = {}
    for name in ('explorer', 'domain'):
        path = root / 'molsysviewer_dockingmt' / 'panels' / f'{name}.py'
        tree = ast.parse(path.read_text(), filename=str(path))
        values = [
            ast.literal_eval(node.value)
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == '_ESM' for t in node.targets)
        ]
        if len(values) != 1 or not isinstance(values[0], str) or not values[0]:
            raise ValueError(f'{name} needs one nonempty literal _ESM declaration')
        sources[name] = values[0]
    return sources


if __name__ == '__main__':
    json.dump(panel_sources(Path(__file__).resolve().parents[2]), sys.stdout)
