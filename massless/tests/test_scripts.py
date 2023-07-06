# -*- coding: utf-8 -*-
"""Tests for script.py"""
import sys

from massless import scripts


def test_get_parser(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["this_program"])
    parser = scripts.get_parser()
    # As a test, we just check one option. That's enough.
    options = parser.parse_args()
    assert options.verbose is False
