"""Internal conversion utilities between PDB representations and MolSysMT."""

from __future__ import annotations

import os
import tempfile
from typing import Any


def pdb_text_to_molsys(pdb_text: str) -> Any:
    """Convert PDB-formatted text to a MolSysMT MolSys system via a temporary file."""
    import molsysmt as msm

    with tempfile.NamedTemporaryFile(suffix='.pdb', mode='w', delete=False) as f:
        f.write(pdb_text)
        temp_path = f.name
    try:
        return msm.convert(temp_path, to_form='molsysmt.MolSys')
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
