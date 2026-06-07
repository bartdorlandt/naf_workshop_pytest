# CI/CD Integration

## Why CI/CD for Network Automation?

Continuous Integration and Continuous Deployment (CI/CD) brings software engineering best practices to network automation:

- **Automated testing** on every code change
- **Consistent environments** for running tests
- **Fast feedback** on code quality
- **Confidence** to deploy changes

## GitHub Actions Basics

GitHub Actions runs workflows defined in `.github/workflows/`:

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv and set the python version
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
          python-version: '3.12'

      - name: Install the project
        run: uv sync --locked

      - name: Run tests
        run: uv run pytest -v
```

## Test Reports

### JUnit XML Output

Generate JUnit XML for CI systems:

```yaml
- name: Run tests
  run: uv run pytest --junitxml=test-results.xml

- name: Upload test results
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: test-results.xml
```

### Coverage Reports

Add test coverage. The coverage dependencies like `pytest-cov` should already be part of your project, defined in `pyproject.toml`:

```yaml
- name: Run tests with coverage
  run: uv run pytest --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    files: coverage.xml
```

## Matrix Testing

Test across multiple Python versions:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12', '3.13', '3.14']

    steps:
      - uses: actions/checkout@v4

      - name: Install uv and set the python version
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
          python-version: ${{ matrix.python-version }}

      # Assert that the `uv.lock` will remain unchanged
      - name: Install the project
        run: uv sync --locked

      - name: Run tests
        run: uv run pytest -v
```

## Pre-commit Hooks

Run tests locally before committing:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        pass_filenames: false
```

## Best Practices

1. **Run tests on every PR** - Catch issues before merge
2. **Keep tests fast** - Slow tests discourage running them
3. **Use caching** - Cache dependencies to speed up CI
4. **Fail fast** - Stop on first failure during development
5. **Parallel execution** - Use `pytest-xdist` for parallel tests

## Example: Complete Workflow

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv and set the python version
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
          python-version: '3.12'

      - run: uv run ruff check .
      - run: uv run ruff format --check .

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Install uv and set the python version
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
          python-version: '3.12'

      - name: Install the project
        run: uv sync --locked

      - name: Run tests & coverage
        run: uv run pytest -v --cov=src --cov-report=term-missing --junitxml=test-results.xml

      - name: Upload test results
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results.xml
```
