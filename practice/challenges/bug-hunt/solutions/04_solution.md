# Solution: Key and Attribute Errors

## Bug 1 — `print_display_names` crashes on missing key

**Problem:** Bob's record has no `"display_name"` key. `user['display_name']`
raises `KeyError`. Eve's `display_name` is `None`, which prints as "None".

**Fix:**

```python
def print_display_names(users):
    for user in users:
        name = user.get("display_name") or user["username"]
        print(f"  {name}")
```

## Bug 2 — `count_by_type` crashes on missing key and wrong initialization

**Lines:** `user["type"]` and `counts[user_type] + 1`

**Problem:** Diana has no `"type"` key → `KeyError`. Even for users that have
a type, `counts[user_type] + 1` fails on the first occurrence because the key
doesn't exist in `counts` yet.

**Fix:**

```python
def count_by_type(users):
    counts = {}
    for user in users:
        user_type = user.get("type", "unknown")
        counts[user_type] = counts.get(user_type, 0) + 1
    return counts
```

## Bug 3 — `most_recent_user` crashes on None date

**Problem:** Eve's `last_login` is `None`. `datetime.strptime(None, ...)`
raises `TypeError`.

**Fix:** Skip users with no login date:

```python
if user["last_login"] is None:
    continue
```

## Bug 4 — `most_recent_user` uses attribute access on a dict

**Line:** `latest_user = user.username`

**Problem:** `user` is a dictionary, not an object. Dictionaries use bracket
access `user["username"]`, not dot access `user.username`.

**Fix:**

```python
latest_user = user["username"]
```
