# ctfd.py

Async Python client for the [CTFd](https://ctfd.io) API (v1).

## Installation

```sh
uv add ctfd-api
# or
pip install ctfd-api
```

## Requirements

- Python **3.13+**
- [httpx](https://www.python-httpx.org/) (installed automatically)

## Quick start

```python
import asyncio
from ctfd import CTFdClient

async def main():
    async with CTFdClient('https://my-ctf.example.com', token='ctfd_...') as ctfd:
        # Get the current user
        me = await ctfd.users.me()
        print(me.name, me.score)

        # List all challenges
        challenges = await ctfd.challenges.list()
        for ch in challenges:
            print(ch.name, ch.value, ch.category)

asyncio.run(main())
```

## Authentication

Pass an API token obtained from **Profile → API Access Tokens**:

```python
ctfd = CTFdClient('https://my-ctf.example.com', token='ctfd_abc123')
```

Without a token the client still works for public endpoints (e.g. scoreboard).

## Resources

Every swagger tag maps to an attribute on `CTFdClient`:

| Attribute            | Resource                                     |
| -------------------- | -------------------------------------------- |
| `ctfd.challenges`    | Challenges, attempts, sub-resources          |
| `ctfd.users`         | Users, `/me`, solves, fails, awards          |
| `ctfd.teams`         | Teams, `/me`, members, solves, fails, awards |
| `ctfd.scoreboard`    | Full list, top-N                             |
| `ctfd.flags`         | Flags, types                                 |
| `ctfd.hints`         | Hints                                        |
| `ctfd.tags`          | Tags                                         |
| `ctfd.topics`        | Topics                                       |
| `ctfd.awards`        | Awards                                       |
| `ctfd.submissions`   | Submissions                                  |
| `ctfd.files`         | Files, upload, download                      |
| `ctfd.notifications` | Notifications                                |
| `ctfd.configs`       | Config keys, fields                          |
| `ctfd.pages`         | Pages                                        |
| `ctfd.tokens`        | API tokens                                   |
| `ctfd.unlocks`       | Unlocks                                      |
| `ctfd.comments`      | Comments                                     |
| `ctfd.shares`        | Shares                                       |
| `ctfd.brackets`      | Brackets                                     |
| `ctfd.solutions`     | Solutions                                    |
| `ctfd.statistics`    | Statistics aggregates                        |
| `ctfd.exports`       | Export archive                               |

## Pagination

List endpoints return the first page. Use `.iter()` to walk all pages automatically:

```python
async with CTFdClient('https://my-ctf.example.com', token='ctfd_...') as ctfd:
    # All users, page by page
    async for user in ctfd.users.iter():
        print(user.id, user.name)

    # Or collect everything at once
    all_submissions = await ctfd.submissions.iter().all()
```

## Common operations

### Submit a flag

```python
result = await ctfd.challenges.attempt(challenge_id=42, submission='flag{example}')
print(result['status'])   # 'correct' or 'incorrect'
```

### Create a challenge (admin)

```python
from ctfd.models import Challenge

ch = await ctfd.challenges.create({
    'name': 'My Challenge',
    'description': 'Find the flag.',
    'value': 100,
    'category': 'web',
    'type': 'standard',
    'state': 'visible',
})
print(ch.id)
```

### Manage flags (admin)

```python
flag = await ctfd.flags.create({
    'challenge_id': ch.id,
    'type': 'static',
    'content': 'flag{secret}',
})

await ctfd.flags.delete(flag.id)
```

### Upload a file (admin)

```python
with open('attachment.zip', 'rb') as f:
    files = await ctfd.files.create({
        'files': [('file', ('attachment.zip', f, 'application/zip'))],
        'type': 'challenge',
        'challenge_id': 42,
    })
```

### Export (admin)

```python
# Download entirely in memory
data = await ctfd.exports.raw()
with open('ctfd_backup.zip', 'wb') as f:
    f.write(data)

# Or stream to disk
async with CTFdClient(...) as ctfd:
    with open('ctfd_backup.zip', 'wb') as f:
        async for chunk in ctfd.exports.stream():
            f.write(chunk)
```

### Team management (admin)

```python
# Add a user to a team
await ctfd.teams.add_member(team_id=5, user_id=12)

# Remove a member
await ctfd.teams.remove_member(team_id=5, user_id=12)
```

### Config (admin)

```python
# Bulk update
await ctfd.configs.bulk_update({'ctf_name': 'My CTF', 'ctf_description': 'Have fun!'})

# Single key
cfg = await ctfd.configs.get('ctf_name')
print(cfg.value)
```

## Error handling

```python
from ctfd import (
    CTFdAuthenticationError,
    CTFdNotFoundError,
    CTFdPermissionError,
    CTFdRateLimitError,
    CTFdValidationError,
)

try:
    ch = await ctfd.challenges.get(9999)
except CTFdNotFoundError:
    print('challenge not found')
except CTFdAuthenticationError:
    print('invalid or missing token')
except CTFdPermissionError:
    print('admin rights required')
except CTFdValidationError as e:
    print('bad request:', e.errors)
except CTFdRateLimitError:
    print('rate limited, slow down')
```

## Dev setup

```sh
uv sync                     # install deps + dev tools
uv run pre-commit install   # install git hooks
uv run pytest               # run tests
uv run pytest --cov         # tests with coverage
uv run ruff check ctfd      # lint
uv run mypy                 # type-check
```

## License

[GPL-3.0-or-later](LICENSE)
