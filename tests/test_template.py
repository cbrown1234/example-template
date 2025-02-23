"""Tests for the copier template."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

from copier import run_copy


def test_copy_default(tmp_path: Path, pytestconfig: pytest.Config) -> None:
    root_dir = pytestconfig.rootdir
    run_copy(
        str(root_dir),
        tmp_path,
        vcs_ref='HEAD',
        defaults=True,
    )
    assert (tmp_path / '.copier-answers-example-template.yml').exists()
