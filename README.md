# Realtime-Data-Pipeline
Make a pipeline which fetches posts from subreddit and  does sentiment analysis on subreddits' post

This shows the structure of project.
realtime-data-pipeline/
├── docker-compose.yml        # Kafka + Zookeeper
├── requirements.txt          # Dependencies
├── kafka_producer/
│   ├── producer.py           # Reddit producer
│   ├── config.env            # Reddit + Kafka config
├── spark_processor/
│   ├── processor.py    # Processes Reddit data
├── dashboard/
│   ├── dashboard.py                # Live dashboard and main file to run
├── data/                     # Processed output
└── README.md



This justifies the flow of data through the Architecture.
Reddit API (PRAW)
    ↓
Kafka Producer
    ↓
Kafka Broker (reddit_posts topic)
    ↓
Spark Structured Streaming (sentiment + keywords)
    ↓
PostgreSQL
    ↓
Streamlit Dashboard (live queries + charts + wordcloud)

