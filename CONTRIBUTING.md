# Contributing

We love contributions! This document will help you to understand the contribution guidelines. If you have any
questions, please [contact us][support].

- [Code of Conduct](#code-of-conduct)
- [Getting started](#getting-started)
  - [Installing Python packages](#installing-python-packages)
  - [Pre-commit hooks](#pre-commit-hooks)

## Code of Conduct

Please read [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) before contributing to this repository.

## Getting started

To contribute to this code, please make sure your system meets the following requirements:

- Unix-like operating system (macOS, Linux, …);
- Load environment variables from [`.envrc`](/.envrc);
- Python 3.6 or above; and
- Python packages [installed](#installing-python-packages) from the [`requirements.txt`](./requirements.txt) file.

We recommend installing [`direnv`](https://direnv.net/), and its shell hooks to load environment variables from
[`.envrc`](/.envrc). You can manually do so each time by sourcing the file in your terminal:

```
. ./.envrc
```

### Installing Python packages

It is highly recommended you first create a Python virtual environment using one of the various methods, before
installing packages. To install the packages, and [set up pre-commit hooks](#pre-commit-hooks) in your terminal run the
following command:

```
make requirements
```

#### Pre-commit hooks

[`pre-commit`][pre-commit] is used to manage pre-commit hooks to:

- Ensure the Python code meets PEP8 standards;
- Check for any secrets being accidentally committed; and
- Check for any large files (over 5MB) being committed.

The hooks run on _every commit_, and allow us to maintain the repository in a healthy state.

If the pre-commit hooks incorrectly flag items as secrets, you will have to scan, audit, and update
[`.secrets.baseline`](./.secrets.baseline) — refer to the [`detect-secrets`][detect-secrets] documentation for further
information.

[support]: mailto:eskyoung.github@gmail.com?subject=Support
[pre-commit]: https://pre-commit.com
[detect-secrets]: https://github.com/Yelp/detect-secrets
