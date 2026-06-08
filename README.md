# ctfd.py

Async Python client for the [CTFd](https://ctfd.io) API (v1).

[![PyPI](https://img.shields.io/pypi/v/ctfd-api)](https://pypi.org/project/ctfd-api/)
[![Python](https://img.shields.io/pypi/pyversions/ctfd-api)](https://pypi.org/project/ctfd-api/)
[![License](https://img.shields.io/pypi/l/ctfd-api)](LICENSE)

**[Documentation](https://donasako.github.io/ctfd.py/)** · [PyPI](https://pypi.org/project/ctfd-api/) · [Changelog](CHANGELOG.md)

## Installation

```sh
uv add ctfd-api
# or
pip install ctfd-api
```

Requires Python 3.13+.

## Quick start

```python
import asyncio
from ctfd import CTFdClient

async def main():
    async with CTFdClient('https://my-ctf.example.com', token='ctfd_...') as ctfd:
        me = await ctfd.users.me()

        async for challenge in ctfd.challenges.iter():
            print(challenge.name, challenge.value)

asyncio.run(main())
```

Get a token from **Profile → API Access Tokens** on your CTFd instance.

## Dev setup

```sh
uv sync                              # install deps + dev tools
uv run pre-commit install            # install git hooks
uv run pytest                        # run tests
uv run ruff check ctfd               # lint
uv run mypy                          # type-check
uv run --group docs mkdocs serve     # live docs preview
```

## License

[GPL-3.0-or-later](LICENSE)
