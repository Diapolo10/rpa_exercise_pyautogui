# Installation

Here's a short tutorial for installing the project locally.

## Installing requirements

You'll need:

- Python 3.8 or newer
- Poetry, for development (once Python is installed, install Poetry via `pip install poetry`)

## Installing the project for development

Installing should be as simple as running `poetry install`; depending on your
system you may need to specify `python3 -m poetry install` or
`py -m poetry install`, but the end result is the same. Poetry should create
a new virtual environment, install all the dependencies it reads from
[`poetry.lock`](../poetry.lock) (if it exists) or [`pyproject.toml`](../pyproject.toml),
and once it's done everything should be good to go.

If you run into issues during installation, try running `poetry update` to
update `poetry.lock` with newer dependencies and try installing again.

The virtual environment can be activated as simply as running `poetry shell`.

## Installing for use

The only requirement should be to run `pip install .` in the project root
directory. `pip` should read the `pyproject.toml` file, and fetch the required
dependencies listed in the lock file. If problems arise, remove the lock file
and try again to regenerate it.

To run the program, navigate to the project files and launch `main.py`. You can
change the cnfiguration settings in `config.py`, should that be necessary.
