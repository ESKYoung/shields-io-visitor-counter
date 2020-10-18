# Contributing

We love contributions! This document will help you to understand the contribution guidelines. If you have any
questions, please [contact us][support].

- [Code of Conduct](#code-of-conduct)
- [Getting started](#getting-started)
  - [Installing Python packages](#installing-python-packages)
    - [Pre-commit hooks](#pre-commit-hooks)
- [Development](#deployment)
  - [Environment variables](#environment-variables)
- [Deployment](#deployment)

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

## Development

The entire application can be found in [`main.py`](./main.py), with its associated tests in the [`tests`](./tests)
folder; tests are executed using [pytest][pytest]

Travis CI deployment is managed by the [`.travis.yml`](./.travis.yml) file - see the [Deployment](#deployment)
section for further details.

The application uses environment variables extensively - see the [Environment variables](#environment-variables)
section for further details.

### Environment variables

Here are the definitions for the environment variables found in [`.envrc`](./.envrc):

| Name                       | Description                                                                                                                                                                |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT_SHIELDS_IO_LABEL` | Default label text to use if the `label` parameter isn't supplied by the user.                                                                                             |
| `DEFAULT_SHIELDS_IO_COLOR` | Default message background colour if the `color` parameter isn't supplied by the user.                                                                                     |
| `GITHUB_REPOSITORY`        | Default URL to redirect if a user goes to the application [home page][application].                                                                                        |
| `FLASK_APP`                | Used by Flask to identify the application script - [`main.py`](./main.py) in this case.                                                                                    |
| `HASH_KEY`                 | Combined with `page` to use as the CountAPI key - defined in Heroku under config vars, but should be uncommented and added in when deploying the application locally.      |
| `HTML_CRON`                | HTML file name in the [`templates`](./templates) folder that cron jobs should point to. This allows cron jobs to keep the application awake without affecting the counter. |
| `URL_COUNTAPI`             | URL for CountAPI including only the namespace.                                                                                                                             |
| `URL_SHIELDS_IO`           | URL for creating static Shields.IO badges.                                                                                                                                 |

Note, when you run `direnv allow` this should export all the uncommented environment variables in a `.env` file, as
this may be useful, e.g. for use with PyCharm's [EnvFile][envfile] plugin to use environment variables with PyCharm run
configurations.

## Deployment

This application is deployed on Heroku at [https://shields-io-visitor-counter.herokuapp.com][application]
automatically by Travis CI.

By default, Travis CI will only deploy commits with Git tags. We work on the assumption that tags are also releases, so
Git tags are only applied for releases, and vice versa. Tags/releases are named according to [semantic
versioning][semver].

[application]: https://shields-io-visitor-counter.herokuapp.com
[envfile]: https://plugins.jetbrains.com/plugin/7861-envfile
[pytest]: https://docs.pytest.org/
[semver]: https://semver.org/
