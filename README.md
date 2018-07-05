# Pickle's Fetch Quest

[![Build Status][build-badge]][build-link] [![Coverage][coverage-badge]][coverage-link] ![Maintainability][health-badge]][health-link]

A throwback to the Game Boy era of gaming, inspired by Kirby's Great Cave Offensive and created for GitHub's 2017 Game Off. Help Pickle brave the Wolf Queen's Palace and collect as many of her treasures as you can!

## Installing

Install dependencies with pip and run `pickles-fetch-quest.py` to play!

```bash
pip install -r requirements.txt     # To install only packages needed to play
pip install -r requirements-dev.txt # To install development packages as well
python pickles-fetch-quest.py       # Let's play!
```

## Development

Pickle's Fetch Quest uses flake8 to maintain PEP 8 compliance. Run `flake8` on the project directory when contributing to ensure your code follows these guidelines. Tests are written using Python's `unittest` module.

```bash
flake8             # Lint codebase
python -m unittest # Run tests
```

[coverage-badge]: https://codecov.io/gh/codehearts/pickles-fetch-quest/branch/master/graph/badge.svg
[coverage-link]:  https://codecov.io/gh/codehearts/pickles-fetch-quest
[health-badge]:   https://api.codeclimate.com/v1/badges/d43c91516157f1c02dd0/maintainability
[health-link]:    https://codeclimate.com/github/codehearts/pickles-fetch-quest/maintainability
[build-badge]:    https://travis-ci.org/codehearts/pickles-fetch-quest.svg?branch=master
[build-link]:     https://travis-ci.org/codehearts/pickles-fetch-quest
