# Module 03 / Project 02 — Query Parameters

[README](../../../../README.md)

## Focus

- Passing query parameters with the `params` dict
- Filtering API results by field values
- Paginating results with `_limit` and `_start`
- Understanding the difference between params dict and URL string

## Why this project exists

Most APIs return too much data if you do not tell them what you want. Query parameters are how you filter, sort, and paginate results. This project teaches you two ways to attach parameters to a request and shows you how to work with lists of results instead of a single resource.

## Run

```bash
cd projects/modules/03-rest-apis/02-query-parameters
python project.py
```

## Expected output

```text
--- Method 1: params dict ---
Fetching posts by user 3 (using params dict)...
Found 10 posts by user 3.
  Post 21: ea molestias quasi exercitationem repellat qui ipsa sit aut
  Post 22: delectus ullam et corporis nulla voluptas sequi
  Post 23: nesciunt iure omnis dolorem tempora et accusantium
  (showing first 3)

--- Method 2: URL string ---
Fetching posts by user 3 (using URL string)...
Found 10 posts by user 3.

--- Pagination ---
Page 1: fetched 5 posts (IDs: 1, 2, 3, 4, 5)
Page 2: fetched 5 posts (IDs: 6, 7, 8, 9, 10)
Page 3: fetched 5 posts (IDs: 11, 12, 13, 14, 15)
```

## Alter it

1. Change the `userId` filter to a different user (1 through 10 are valid). How many posts does each user have?
2. Change the page size from 5 to 3 and fetch 5 pages instead of 3.
3. Combine filtering and pagination: fetch user 1's posts, 2 at a time.

## Break it

1. Pass `userId=999` — a user that does not exist. What does the API return? Is it an error or an empty list?
2. Set `_limit=0`. What happens?
3. Pass `params={"userId": [1, 2]}` — a list instead of a single value. Does the API handle it? What do you get back?

## Fix it

1. Add a check after each request: if the response is an empty list, print "No results found" instead of trying to iterate.
2. Add validation before the request: if `user_id` is not between 1 and 10, print a warning.
3. After fixing, test with both valid and invalid user IDs.

## Explain it

1. What is the difference between passing `params={"userId": 3}` and putting `?userId=3` directly in the URL string?
2. Why does JSONPlaceholder return an empty list instead of a 404 when you filter by a nonexistent user?
3. How does `_start` differ from `_page` in pagination schemes you might encounter in other APIs?
4. When would you choose params dict over URL string in your own code?

## Mastery check

You can move on when you can:

- pass query parameters using both methods,
- paginate through results using `_start` and `_limit`,
- handle empty results gracefully,
- explain why the params dict is usually preferred.

## Next

Continue to [POST and Auth](../03-post-and-auth/).
