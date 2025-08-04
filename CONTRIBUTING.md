# Contributing to dstamp

Thank you for taking interest in dstamp!

## Feedback

If you have a bug to report or a feature request, please raise an [Issue].

I'm also happy to accept [PR]s but I would prefer you to first raise an Issue and
indicate your willingness to submit a PR.

This is my first CLI app, so there are probably many things I could do or do differently
to improve it. If you have suggestions please let me know in an Issue :)

[PR]: https://github.com/mariusz-tang/dstamp/pulls
[Issue]: https://github.com/mariusz-tang/dstamp/issues

## Project setup

### Installing

After cloning the project set up [Poetry] and run the tests:

```bash
poetry sync

# See the Poetry docs for how to activate the virtual environment in your shell.
eval $(poetry env activate)
coverage run
```

Optionally install and run the [pre-commit] hooks.
This will handle the code style requirements for this project, among other things.

```bash
pre-commit install
pre-commit run --all-files
```

[poetry]: https://python-poetry.org/
[pre-commit]: https://pre-commit.com/

### Code style

This project uses various programs to keep code in check:

- [Black], [isort], and [Flake8] for Python.
- [Markdownlint] for Markdown.
- [yamlfix] for YAML.

If you install the pre-commit hooks as above, this will be handled for you.

[isort]: https://pycqa.github.io/isort/
[Black]: https://black.readthedocs.io/en/stable/
[Flake8]: https://flake8.pycqa.org/en/latest/
[Markdownlint]: https://github.com/markdownlint/markdownlint
[yamlfix]: https://github.com/lyz-code/yamlfix

### Testing

Please test your code :)

This project uses [pytest] and [coverage.py] for testing and coverage.

#### Coverage

As this is a small project, requiring 100% coverage is feasible and realistic.
In rare cases, there will be code that need not be covered. [Exclude] such code
from coverage.py.

[pytest]: https://docs.pytest.org/en/stable/
[coverage.py]: https://coverage.readthedocs.io/en/7.10.1/
[exclude]: https://coverage.readthedocs.io/en/7.10.1/excluding.html

### A note on perfectionism

Don't worry if you are unable to follow everything in this file! I appreciate any
effort to stick to the guidelines, but you don't need to do everything perfectly
in order to contribute code. In particular, I will run all the pre-commit hooks
before accepting any PR anyway, so anything which can be fixed with automatic
formatting is not very important.

If you are finding something challenging or are unsure about something, feel free
to get in touch, for example by raising an Issue or submitting a draft PR!
