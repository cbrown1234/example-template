# example-template-copier-template

A [Copier](https://copier.readthedocs.io/) template.

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
copier update --trust
```
