import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

st.title("📊 Real-Time Reddit Sentiment Dashboard")

conn = psycopg2.connect(
    host="...",
    database="...",
    user="...",
    password="..."
)

# Fetch latest data
df = pd.read_sql("SELECT * FROM reddit_posts ORDER BY created_utc DESC LIMIT 50;", conn)

st.subheader("Latest Reddit Posts")
st.write(df[["title", "subreddit", "sentiment"]])

st.subheader("Sentiment Distribution")
fig, ax = plt.subplots()
df["sentiment"].hist(ax=ax, bins=20)
st.pyplot(fig)

st.subheader("Average Sentiment by Subreddit")
avg_sent = df.groupby("subreddit")["sentiment"].mean()
st.bar_chart(avg_sent)
