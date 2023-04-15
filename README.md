# Twitter_Scrapper
### A twitter scrapper is created using 'snscrape' module in python and using 'streamlit' module GUI is created.

#### The code below is a Python script that performs the following steps:

- It uses the snscrape library to scrape Twitter.
- It creates a Pandas DataFrame from the scraped data, including fields such as date, tweet ID, URL, tweet content, user, reply count, retweet count, language, source, and like count.
- It stores the scraped data in MongoDB by creating a client object and a database object, and inserting the scraped data into a collection called "twitter_data" in the database. The inserted data includes the scraped word/keyword, scraped date, and the scraped data itself. Overall, this script allows for the efficient scraping and storage of Twitter data using Python, Pandas, and MongoDB.


## Streamlit API :
API stands for Application Programming Interface. It is a set of protocols, routines, and tools for building software applications that allows different software components to interact with each other.

An API defines how two or more software components should communicate and interact with each other. It typically specifies the request and response format, the set of operations that can be performed, and the authentication and authorization mechanisms.

Streamlit is a popular Python framework for building data science applications. It provides a simple and intuitive way to create interactive web applications using Python code. Streamlit API is a set of functions and classes that allow you to create and customize Streamlit applications.

Streamlit API provides a range of functions for creating interactive widgets, visualizations, and user interfaces. These functions can be used to create custom web applications, dashboards, and data science workflows. The API also allows you to integrate your Streamlit application with other Python libraries and web services.

#### Some of the key features of Streamlit API include:

- Simple and intuitive API: The Streamlit API is designed to be easy to use and understand, even for beginners.
- Interactive widgets: Streamlit API provides a range of widgets such as sliders, checkboxes, and dropdowns that allow users to interact with your application.
- Data visualization: Streamlit API includes a range of visualization functions that allow you to create charts, graphs, and other data visualizations.
- Customization: Streamlit API allows you to customize the appearance and behavior of your application using CSS stylesheets and other advanced features.

In summary, Streamlit API is a powerful tool for building interactive web applications using Python code. It provides a simple and intuitive way to create custom applications and workflows that can help you to analyze, visualize, and communicate your data effectively


### <Code>
  
import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
# import datetime
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
