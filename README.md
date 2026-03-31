# example-template-copier-template

A [Copier](https://copier.readthedocs.io/) template.

<!-- TODO: Describe what this template generates -->

## Install Copier

```bash
uv tool install copier --with copier-pydantic --with copier-template-extensions
# or
pipx install copier
pipx inject copier copier-pydantic copier-template-extensions
```

## Usage

### Create a new project

```bash
copier copy <template-url> /path/to/new/project --trust
```

### Update an existing project

```bash
cd /path/to/your/project
copier update --answers-file .copier-answers.example-template.yml --trust
```

## Demo

[![demo](https://asciinema.org/a/QOhPOyerSRIgwkqo.svg)](https://asciinema.org/a/QOhPOyerSRIgwkqo)

## Development

Prerequisites: [uv](https://docs.astral.sh/uv/) and [Task](https://taskfile.dev/).

Run `task --list` to see available commands. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full development guide.
