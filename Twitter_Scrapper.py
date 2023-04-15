import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import base64

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]
collection = db["twitter_data"]


# Define a function to scrape Twitter data
def scrape_twitter_data(keyword, start_date, end_date, tweet_count):
    tweets_list = []
    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(f"{keyword} since:{start_date} until:{end_date}").get_items()):
        if i >= tweet_count:
            break
        tweets_list.append(
            [tweet.date, tweet.id, tweet.url, tweet.rawContent, tweet.user.username, tweet.replyCount, tweet.retweetCount,
             tweet.lang, tweet.sourceLabel, tweet.likeCount])
    df = pd.DataFrame(tweets_list,
                      columns=['date', 'id', 'url', 'tweet_content', 'user', 'reply_count', 'retweet_count', 'language',
                               'source', 'like_count'])
    return df


# Define the Streamlit app
def app():
    st.title("Twitter Data Scraper and Uploader")

    # Define the sidebar inputs
    keyword = st.sidebar.text_input("Enter the keyword or hashtag to search")
    start_date = st.sidebar.date_input("Select the start date")
    end_date = st.sidebar.date_input("Select the end date")
    tweet_count = st.sidebar.number_input("Enter the number of tweets to scrape", min_value=1, max_value=1000,
                                          value=100)

    # Define the main app inputs
    show_data = st.checkbox("Show scraped data")
    upload_data = st.button("Upload data to MongoDB")
    download_csv = st.button("Download data as CSV")
    download_json = st.button("Download data as JSON")

    # Scrape Twitter data and show it if requested
    if keyword and start_date and end_date and tweet_count:
        df = scrape_twitter_data(keyword, start_date, end_date, tweet_count)
        if show_data:
            st.write(df)

    # Upload the scraped data to MongoDB if requested
    if upload_data and 'df' in locals():
        scraped_data = {
            "Scraped Word": keyword,
            "Scraped Start Date": str(start_date),
            "Scraped End Date": str(end_date),
            "Scraped Data": df.to_dict('records')
        }
        collection.insert_one(scraped_data)
        st.write("Data uploaded to MongoDB!")

    # Download the scraped data as CSV if requested
    if download_csv and 'df' in locals():
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="twitter_data.csv">Download CSV File</a>',
                    unsafe_allow_html=True)

    # Download the scraped data as JSON if requested
    if download_json and 'df' in locals():
        json = df.to_json(orient='records')
        b64 = base64.b64encode(json.encode()).decode()
        st.markdown(f'<a href="data:file/json;base64,{b64}" download="twitter_data.json">Download JSON File</a>',
                    unsafe_allow_html=True)


def main():
    app()


if __name__ == "__main__":
    main()