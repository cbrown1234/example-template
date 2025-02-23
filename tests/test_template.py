"""Tests for the copier template."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import pytest
from copier import run_copy


@pytest.fixture
def template_dir(pytestconfig: pytest.Config) -> str:
    root_dir = pytestconfig.rootdir
    return str(root_dir)


def test_copy_default(template_dir: str, tmp_path: Path) -> None:
    run_copy(
        template_dir,
        tmp_path,
        vcs_ref='HEAD',
        defaults=True,
    )
    assert (tmp_path / '.copier-answers-example-template.yml').exists()
