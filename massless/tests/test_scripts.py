"""Tests for script.py"""

import sys

import pytest

from massless import scripts


@pytest.fixture
def dummy_fixture():
    # To allow pytest to be in the test dependencies.
    pass


def test_get_parser(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["this_program"])
    parser = scripts.get_parser()
    # As a test, we just check one option. That's enough.
    options = parser.parse_args()
    assert options.verbose is False
