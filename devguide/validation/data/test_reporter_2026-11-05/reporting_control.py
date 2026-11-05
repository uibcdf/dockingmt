import warnings

import pytest

import dockingmt as dmt


def test_protocol_pass():
    assert dmt.VinaProtocol(cpu=1).cpu == 1


def test_warning_pass():
    warnings.warn('deliberate receiving warning', UserWarning)


def test_owned_failure():
    dmt.VinaProtocol(cpu=True)


@pytest.mark.skip(reason='deliberate receiving skip')
def test_explicit_skip():
    pass
