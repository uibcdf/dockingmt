"""Public aliases for DockingMT's existing catalog exception identities.

Use this namespace to catch library-owned diagnostics. Provider exceptions and
native resource/process-control failures retain their own identities. The
implementation module paths remain unchanged for existing consumers and records.
"""

from dockingmt._private.smonitor import (
    ArgumentError,
    CapabilityMismatchError,
    DockingMTException,
    DockingMTViewerError,
    LibraryNotFoundError,
    ViewerActionError,
    ViewerCapabilityError,
    ViewerInputMissingError,
    ViewerPoseCountError,
    ViewerPosePositionError,
    ViewerShapeOwnershipError,
    ViewerStateError,
    ViewerStructureCountError,
)

__all__ = [
    'DockingMTException',
    'LibraryNotFoundError',
    'ArgumentError',
    'CapabilityMismatchError',
    'DockingMTViewerError',
    'ViewerPoseCountError',
    'ViewerStructureCountError',
    'ViewerInputMissingError',
    'ViewerPosePositionError',
    'ViewerShapeOwnershipError',
    'ViewerStateError',
    'ViewerCapabilityError',
    'ViewerActionError',
]
