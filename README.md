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

We use "uv" for a local dev install:

    $ uv sync --dev

Run the scripts in massless/ like this:

    $ uv run massless/fix-csv.py

In order to get nicely formatted python files without having to spend
manual work on it, get [pre-commit](https://pre-commit.com/) and install
it on this project:

    $ pre-commit install
