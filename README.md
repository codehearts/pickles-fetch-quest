# Pickle's Fetch Quest

[![Build Status][build-badge]][build-link] [![Coverage][coverage-badge]][coverage-link] [![Maintainability][health-badge]][health-link]

A throwback to the Game Boy era of gaming, inspired by Kirby's Great Cave Offensive and started for GitHub's 2017 Game Off. Help Pickle brave the Wolf Queen's Palace and collect as many of her treasures as you can!

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

Tests can also be run with coverage reporting.

```bash
coverage run -m unittest                        # Run tests with coverage
coverage report -m --skip-covered --include=./* # Report files without 100% coverage
```

## Dev Log

<img align="right" alt="Pickle hops around an early rendition of the game's castle" src="https://user-images.githubusercontent.com/2885412/91630544-090e2480-e987-11ea-9b2a-a36d9f2b32a7.gif" width="30%">
<p align="right" width="60%"><strong>Aug 2020</strong><br>The camera was implemented, allowing Pickle to explore maps created with the Tiled editor.</p>
<p> </p>
<img align="left" alt="Pickle stands in a castle entry hall" src="https://user-images.githubusercontent.com/2885412/48993397-45498c80-f0f2-11e8-929c-47a70d75289b.gif" width="30%">
<p align="left" width="60%"><strong>Nov 2018</strong><br>Support for the Tiled editor was added, and the demo now showcased a simple castle interior.</p>
<p> </p>
<img align="right" alt="A dog jumps and faces the direction she moves in" src="https://user-images.githubusercontent.com/2885412/48958746-0f4fb100-ef16-11e8-9b6c-a8971ecec046.gif" width="30%">
<p align="right" width="60%"><strong>Nov 2018</strong><br>Tiles could now be animated, and Pickle's original artwork was drawn.</p>
<p> </p>
<img align="left" alt="A green tile moves and jumps against other tiles" src="https://user-images.githubusercontent.com/2885412/48684936-deaff600-eb68-11e8-9ef8-733bdb9f52fc.gif" width="30%">
<p align="left" width="60%"><strong>Nov 2018</strong><br>Player input was now supported, and the demo updated to allow horizontal movement and jumping.</p>
<p> </p>
<img align="right" alt="Green tiles of varying gravity colliding" src="https://user-images.githubusercontent.com/2885412/38073387-9ed01476-32df-11e8-8f27-04f75f8de919.gif" width="30%">
<p align="right" width="60%"><strong>Mar 2018</strong><br>Collision resolution was implemented, allowing physical objects to rest against one another.</p>
<p> </p>
<img align="left" alt="A green tile falling against a black background" src="https://user-images.githubusercontent.com/2885412/33042770-e1e62a9a-cdf7-11e7-9cdf-7e236ba7aa53.gif" width="30%">
<p align="left" width="60%"><strong>Nov 2017</strong><br>The initial physics engine was added, setting up for collision detection.</p>

[coverage-badge]: https://codecov.io/gh/codehearts/pickles-fetch-quest/branch/master/graph/badge.svg
[coverage-link]:  https://codecov.io/gh/codehearts/pickles-fetch-quest
[health-badge]:   https://api.codeclimate.com/v1/badges/d43c91516157f1c02dd0/maintainability
[health-link]:    https://codeclimate.com/github/codehearts/pickles-fetch-quest/maintainability
[build-badge]:    https://travis-ci.org/codehearts/pickles-fetch-quest.svg?branch=master
[build-link]:     https://travis-ci.org/codehearts/pickles-fetch-quest
