"""Tests for the copier template."""

from __future__ import annotations

from pathlib import Path

from copier import run_copy, run_update
from helpers import git_save

TEMPLATE_DIR = Path(__file__).parent.parent.absolute()
ANSWER_FILE_DEFAULT = '.copier-answers-example-template.yml'


def test_copy_default(tmp_path: Path) -> None:
    run_copy(
        str(TEMPLATE_DIR),
        tmp_path,
        vcs_ref='HEAD',
        defaults=True,
    )
    assert (tmp_path / ANSWER_FILE_DEFAULT).exists()


def test_update_default(tmp_path: Path) -> None:
    run_copy(
        str(TEMPLATE_DIR),
        tmp_path,
        defaults=True,
    )
    git_save(tmp_path)
    run_update(
        tmp_path,
        vcs_ref='HEAD',
        defaults=True,
        overwrite=True,  # The default when run via CLI
        answers_file=ANSWER_FILE_DEFAULT,
    )
    assert (tmp_path / ANSWER_FILE_DEFAULT).exists()
