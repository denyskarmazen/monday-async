# Contributing to monday-async

Thank you for your interest in contributing to monday-async! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Running Tests](#running-tests)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/denyskarmazen/monday-async.git
   cd monday-async
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/denyskarmazen/monday-async.git
   ```

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

## Commit Message Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) to automatically generate our changelog. Please follow these guidelines when writing commit messages.

### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

Your commits **must** use one of the following types to be included in the changelog:

#### 💥 Breaking Changes
Use when introducing breaking changes:
```bash
feat!: redesign authentication API

BREAKING CHANGE: removed support for legacy API keys
```

#### ✨ New Features
Use `feat:` for new features:
```bash
feat: add webhook subscription support
feat(boards): add ability to duplicate boards with templates
```

#### 🐛 Bug Fixes
Use `fix:` for bug fixes:
```bash
fix: resolve token expiration issue
fix(items): correct column value serialization for status columns
```

#### ⚡ Performance
Use `perf:` for performance improvements:
```bash
perf: optimize GraphQL query batching
perf(queries): reduce API calls by implementing request caching
```

#### 📌 Other Changes
Use `other:` for other changes that need to be mentioned in the changelog

### Commits That Won't Appear in Changelog

The following commit types are important for development but won't appear in the user-facing changelog:

- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, missing semicolons, etc.)
- `refactor:` - Code refactoring without feature changes
- `test:` - Adding or updating tests
- `build:` - Changes to build system or dependencies
- `ci:` - Changes to CI configuration
- `chore` - for maintenance tasks

**Example:**
```bash
docs: update installation instructions
style: format code with ruff
refactor: reorganize project structure
test: add integration tests for board operations
```

### Commit Message Examples

**Good:**
```bash
✅ feat: add support for monday.com subitem queries
✅ fix: handle null values in column data correctly
✅ perf: cache frequently accessed board metadata
✅ feat!: rename AsyncClient to AsyncMondayClient
```

**Bad:**
```bash
❌ fixed bug
❌ updates
❌ WIP
❌ small changes
```

## Pull Request Process

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feat/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** following our code style guidelines

3. **Run tests** to ensure everything works:
   ```bash
   uv run pytest
   ```

4. **Run linting** to ensure code quality:
   ```bash
   uv run ruff check
   uv run ruff format --check
   ```

5. **Commit your changes** following our commit message guidelines

6. **Push to your fork**:
   ```bash
   git push origin feat/your-feature-name
   ```

7. **Open a Pull Request** on GitHub:
   - Provide a clear title and description
   - Link any related issues
   - Ensure all CI checks pass

### Pull Request Title

Your PR title should follow the same format as commit messages:
```
feat: add webhook subscription support
fix: resolve authentication token expiration
```

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

### Run Linting

```bash
# Check for linting errors
uv run ruff check

# Auto-fix linting errors
uv run ruff check --fix

# Format code
uv run ruff format
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=monday_async

# Run specific test file
uv run pytest tests/test_items.py

# Run with verbose output
uv run pytest -v
```

## Questions?

If you have any questions or need help, feel free to:
- Open an issue on GitHub
- Start a discussion in the Discussions tab
- Reach out to the maintainers

Thank you for contributing to monday-async! 🚀
