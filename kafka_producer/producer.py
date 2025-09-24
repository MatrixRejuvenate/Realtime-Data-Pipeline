import praw
import json
from kafka import KafkaProducer
import time

# Reddit API credentials (replace with yours)
reddit = praw.Reddit(
    client_id="#",
    client_secret="#",
    user_agent="#"
)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = "reddit_posts"
SUBREDDITS = ["technology", "worldnews"]

print("🚀 Starting Reddit Producer...")

while True:
    for subreddit in SUBREDDITS:
        for submission in reddit.subreddit(subreddit).new(limit=5):
            post = {
                "id": submission.id,
                "title": submission.title,
                "subreddit": subreddit,
                "created_utc": submission.created_utc,
                "url": submission.url
            }
            producer.send(TOPIC, post)
            print(f"Sent: {post['title']}")
    time.sleep(5)
