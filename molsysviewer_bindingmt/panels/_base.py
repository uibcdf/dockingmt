"""Docking-owned panel refresh and subscription lifetime."""

from numbers import Integral
from typing import Any

from molsysviewer.addons import AddonPanelWidget
from smonitor.integrations import context_extra

from bindingmt._private.smonitor import signal

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
            if runtime.result is not None and runtime.interaction_binding is None:
                runtime.active_pose_rank = int(index) + 1
            self._refresh()

    def handle_action(self, view: Any, action_id: str, payload: dict[str, Any]) -> None:
        try:
            self._apply_action(view, action_id, payload)
            self._refresh(view=view)
        except Exception as exc:
            self._refresh(exc, view=view)

    @signal(
        tags=['addon', 'viewer', 'action'],
        extra_factory=lambda args, kwargs: context_extra(
            provider='molsysviewer', operation='panel_action'
        ),
    )
    def _apply_action(self, view: Any, action_id: str, payload: dict[str, Any]) -> None:
        self._handle_action(view, action_id, payload)

    @signal(
        tags=['addon', 'viewer', 'inspection'],
        extra_factory=lambda args, kwargs: context_extra(
            provider='molsysviewer', operation='read_panel_state'
        ),
    )
    def _read_state(self, view: Any) -> dict[str, Any]:
        return self._build_state(ensure_runtime(view), view)

    def _refresh(
        self, error: Exception | str | None = None, *, view: Any = None
    ) -> None:
        view = self._bound_view if view is None else view
        if view is None:
            return
        try:
            state = self._read_state(view)
        except Exception as exc:
            state = dict(getattr(self, '_last_state', {}))
            state.update(domain_available=False, reference_available=False)
            if ensure_runtime(view).interaction_binding is not None:
                state.update(
                    interaction_geometry_available=False,
                    interaction_geometry_reason=str(exc),
                    interaction_analyses=[],
                )
                if 'poses' in state:
                    state['poses'] = [
                        {
                            **row,
                            'geometry_available': False,
                            'geometry_reason': str(exc),
                        }
                        for row in state['poses']
                    ]
            error = exc if error is None else error
        state['error_code'] = None
        if error is not None:
            state.update(
                status='error',
                error=str(error),
                error_code=getattr(error, 'code', None),
            )
        self._last_state = state
        self.set_state({self._state_key: state})
        self.push_state(state)
