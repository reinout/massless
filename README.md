# massless

Introduction

Usage, etc.

## Installation

As it is a personal project with loads of assumptions, I'm going to assume
what's going on in my personal situation. I'm installing this project with the
belowmentioned dev install. And I've got a makefile for custom
copy/pasting/preparing the source data.

- I'm assuming a download of `hackdiet_db.csv` in the "hacker's diet online
  csv" format in `~/Downloads/`.

- And an export of the iphone's health data. In apple health, click on your
  user icon at the top right. There'll be an export option. Takes a lot of
  time (5-10 minutes). Airdrop it to your mac and extract it in the downloads
  folder, there'll be a `apple_health_export/export.xml`.

The `Makefile` copies all that to `var/` and does some grepping to convert the
huge `xml` file to xml-like text files that we can process more easily. Yes,
this is a dirty hack.


## Development installation of this project itself

We use python's build-in "virtualenv" to get a nice isolated
directory, all handily managed in a `Makefile`. To install:

    $ make

If you do it manuallY:

    $ python3 -m venv venv
    $ venv/bin/pip install -e .[test]

There will be a script you can run like this:

    $ venv/bin/run-massless

It runs the `main()` function in `[massless/scripts.py`,
adjust that if necessary. The script is configured in
`TODO, MISSING NOW` (see `entry_points`).

In order to get nicely formatted python files without having to spend
manual work on it, get [pre-commit](https://pre-commit.com/) and install
it on this project:

    $ pre-commit install

Run the tests regularly with coverage:

    $ make test

The tests are also run automatically [on "github
actions"](https://github.com/nens/massless/actions) for
"main" and for pull requests. So don't just make a branch, but turn it into a
pull request right away. On your pull request page, you also automatically get
the feedback from the automated tests.

If you need a new dependency (like `requests`), add it in
`pyproject.toml` in `dependencies`. And update your local install with:

    $ make install
