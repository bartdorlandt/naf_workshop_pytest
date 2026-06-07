# LAB: CI/CD Integration

## Objective

Build a GitHub Actions workflow from scratch that runs your tests automatically on every push and pull request, using `uv` for dependency management.

## Setup

You will need a GitHub repository with your automation code pushed to it. The workflow files you create in `.github/workflows/` will be picked up automatically by GitHub Actions.

```bash
mkdir -p .github/workflows
```

## Exercise 1: Minimal Workflow with uv

Create a workflow that checks out your code, installs dependencies with `uv`, and runs your test suite.

- Use `astral-sh/setup-uv@v6` to install uv (no need for `actions/setup-python`)
- Use `uv sync --locked` to install dependencies exactly as pinned in `uv.lock`
- Run tests with `uv run pytest`

Save it as `.github/workflows/test.yml` and push it. Verify it appears in the **Actions** tab of your repository.

## Exercise 2: Add JUnit Test Results

Extend the workflow to produce a JUnit XML report and upload it as a build artifact.

- Pass `--junitxml=test-results.xml` to pytest
- Use `actions/upload-artifact@v4` to store the file
- Use `if: always()` on the upload step so results are saved even when tests fail

Push the change, let it run, then download the artifact from the Actions UI to inspect the XML.

## Exercise 3: Split Lint and Test into Separate Jobs

Restructure the workflow into two jobs: `lint` and `test`.

- The `lint` job runs `uv run ruff check .` and `uv run ruff format --check .`
- The `test` job runs only after `lint` passes (use `needs: lint`)
- Both jobs should install the project with `uv sync --locked`

Introduce a deliberate formatting error locally (e.g. add extra blank lines), push, and observe that the `test` job is skipped when `lint` fails.

## Exercise 4: Matrix Testing Across Python Versions

Extend the `test` job to run against Python 3.12, 3.13, and 3.14 in parallel.

- Add a `strategy.matrix` with the three versions
- Pass the matrix version to `setup-uv` via `python-version: ${{ matrix.python-version }}` — this takes precedence over any `.python-version` file in the repo

Check the Actions UI — you should see three parallel `test` runs, one per version.

## Checkpoint

!!! success "Solution"

    Incremental solution workflows are provided in `solutions/lab_cicd/`:

    - `ex1_minimal.yml` — Exercise 1
    - `ex2_junit.yml` — Exercise 2
    - `ex3_lint_and_test.yml` — Exercise 3
    - `ex4_matrix.yml` — Exercise 4 (final)
