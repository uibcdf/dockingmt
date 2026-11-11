"""Public BindingMT catalog exception identities.

Use this namespace to catch library-owned diagnostics. Provider exceptions and
native resource/process-control failures retain their own identities.
"""

from bindingmt._private.smonitor import (
    ArgumentError,
    BindingMTException,
    BindingMTViewerError,
    CapabilityMismatchError,
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
    'BindingMTException',
    'LibraryNotFoundError',
    'ArgumentError',
    'CapabilityMismatchError',
    'BindingMTViewerError',
    'ViewerPoseCountError',
    'ViewerStructureCountError',
    'ViewerInputMissingError',
    'ViewerPosePositionError',
    'ViewerShapeOwnershipError',
    'ViewerStateError',
    'ViewerCapabilityError',
    'ViewerActionError',
]
