# Remove bots from my twitter

Notes:

- There are rate limits in X.com; specially when getting the `posts` ui/data, after using the script you will that on your main profile there will be an issue loading the `posts` because of this rate limit.

Learnings:

- First time using playwright with python.
- Sending screenshot of user to python.
- Some scraping of user profile.
- The connection to a common Chrome app (in debug mode) using `connect_over_cdp`, this is useful as it allows reusing our current "active" (after restarting it with `--remote-debugging-port`) chrome session.