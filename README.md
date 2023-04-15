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
