import praw

import settings

reddit = praw.Reddit(
    client_id=settings.REDDIT_CLIENT_ID,
    client_secret=settings.REDDIT_CLIENT_SECRET,
    password=settings.REDDIT_PASSWORD,
    user_agent=f'script by u/{settings.REDDIT_USERNAME}',
    username=settings.REDDIT_USERNAME,
)
