"""Docking-owned panel refresh and subscription lifetime."""

from numbers import Integral
from typing import Any

from molsysviewer.addons import AddonPanelWidget

from ..runtime import ensure_runtime


class _DockingPanel(AddonPanelWidget):
    _state_key: str
    _bound_view: Any = None
    _frame_subscription: bool = False

    def on_mount(self, view: Any) -> None:
        if self._bound_view is not view:
            self._detach()
            self._bound_view = view
            ensure_runtime(view)._panels.add(self)
            if callable(getattr(view, 'on_frame_change', None)) and callable(
                getattr(view, 'off_frame_change', None)
            ):
                view.on_frame_change(self._frame_changed)
                self._frame_subscription = True
        self._refresh()

    def _detach(self) -> None:
        view = self._bound_view
        if view is not None:
            if self._frame_subscription:
                view.off_frame_change(self._frame_changed)
            ensure_runtime(view)._panels.discard(self)
        self._bound_view = None
        self._frame_subscription = False

    def on_unmount(self, view: Any) -> None:
        self._detach()

    def close(self) -> None:
        self._detach()
        super().close()

    def _frame_changed(self, event: dict[str, Any]) -> None:
        if self._bound_view is None:
            return
        index = event.get('frame')
        if event.get('event') != 'frame_changed' or isinstance(index, bool):
            return
        if isinstance(index, Integral):
            runtime = ensure_runtime(self._bound_view)
            if runtime.result is not None:
                runtime.active_pose_rank = int(index) + 1
            self._refresh()

    def _refresh(self, error: str | None = None, *, view: Any = None) -> None:
        view = self._bound_view if view is None else view
        if view is None:
            return
        try:
            state = self._build_state(ensure_runtime(view), view)
        except Exception as exc:
            state = dict(getattr(self, '_last_state', {}))
            state.update(domain_available=False, reference_available=False)
            error = str(exc) if error is None else error
        if error is not None:
            state.update(status='error', error=error)
        self._last_state = state
        self.set_state({self._state_key: state})
        self.push_state(state)
