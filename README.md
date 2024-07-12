# Remove bots from my twitter

### 🚀 How to run it?

Close all your Google Chrome windows and start it using debug mode, on MacOS is:

```sh
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

Install the project dependencies

```sh
pip install -r requirements.txt
```

Run the script
```sh
python main.py
```


### 📝 Notes

- It will remove as follower all followers with 0 posts.
- The initial version included a template to send screenshot of users to OpenAI, but it's too complex to do such approach at the moment.
- There are rate limits in X.com; specially when getting the `posts` ui/data, after using the script you will that on your main profile there will be an issue loading the `posts` because of this rate limit.
- We don't rely anymore in the `posts` ui area, as in the header there is already the total posts a user have, cool!.

### 😎 Learnings

- First time using playwright with python.
- Sending screenshot of user to OpenAI.
- Some scraping of user profile.
- The connection to a common Chrome app (in debug mode) using `connect_over_cdp`, this is useful as it allows reusing our current "active" (after restarting it with `--remote-debugging-port`) chrome session. I already did it before with Robot Framework.