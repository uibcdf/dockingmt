# Configure PyUnitWizard for DockingMT
#
# The MolSysSuite libraries share one PyUnitWizard kernel inside a process, so
# whichever of them configured it last used to win -- and with lazy imports
# "last" can be a notebook cell run much later, silently undoing what the user
# chose. They therefore all declare the same policy, and each one applies it
# only when no policy is active yet.

import pyunitwizard

STANDARD_UNITS = [
    'nm',  # length: nanometer
    'ps',  # time: picosecond
    'K',  # temperature: kelvin
    'mole',  # amount of substance
    'dalton',  # mass
    'e',  # charge: elementary charge
    'kJ/mol',  # energy
    'kJ/(mol*nm)',  # force
    'kJ/(mol*nm**2)',  # force constant
    'radians',  # angle
]

# Only when nobody has decided yet. An active policy belongs to whoever set it:
# another suite library, or the user.
if not pyunitwizard.configure.has_active_policy():
    pyunitwizard.configure.set_pint_registry_cache(True)
    pyunitwizard.configure.set_default_form('pint')
    pyunitwizard.configure.set_default_parser('pint')
    pyunitwizard.configure.set_standard_units(STANDARD_UNITS, provenance='dockingmt')

# Fast tracks are named converters, not policy: `to_nanometers` means
# nanometers whatever the active standard units are. Registering them is
# idempotent across the suite, so it is unconditional.
pyunitwizard.register_fast_track('nanometers', pyunitwizard.unit('nm'))
pyunitwizard.register_fast_track('picoseconds', pyunitwizard.unit('ps'))
pyunitwizard.register_fast_track('kelvin', pyunitwizard.unit('K'))
pyunitwizard.register_fast_track('angstroms', pyunitwizard.unit('angstrom'))
