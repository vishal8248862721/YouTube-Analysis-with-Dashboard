import streamlit as st
from main_file import *
from transfer_to_mongodb import *
from fetch_from_mongodb import *
from test import *
import time
import pandas as pd
from channel_analysis import *

st.set_page_config(
    page_title="YouTube Scrapping",
    layout='wide'
    )

st.title(":red[YouTube Data Scrapping]")


channel_id = st.text_input("Enter Channel Id:", key="channel_id")

api_key = st.text_input("Enter API Key:", type="password", key="api_key")
  

if st.button("Get Channel Info"):
    channel_info=main_data(channel_id)
    st.write(channel_info)



    # Button to fetch JSON data
if st.button("Fetch JSON Data"):
    try:
        # Call the get_channel_stats function and display the results as JSON
        data = main_data(channel_id)
        st.json(data)
        st.success("Successfully fetched Json")
    except:
                st.error("An error occurred. Please check your API Key or Channel ID.")


# Button to fetch data and display as text

if st.button("Upload To MongoDB"):
    with st.spinner("Uploading data to MongoDB..."):
        try:
            data_to_MongoDB(channel_id)
            time.sleep(3)
            st.success("Data uploaded successufully")
        except:
            st.error("An error occurred while uploading data to MongoDB")

      
                
if st.button("view_table"):
    with st.spinner("Fetching data from MongoDB..."):
        try:
            channel_stats = channel_from_MongoDB()  
            playlist_stats = playlist_from_MongoDB()
            comment_stats = comments_from_MongoDB()
            video_stat = videos_from_MongoDB()
            

            st.write(channel_stats)
            st.write(playlist_stats)
            st.write(comment_stats)
            st.write(video_stat)

            st.success("Fetched successfully")

                                        
        except Exception as e:
            st.error(f"An error occurred while fetching data to MongoDB: {str(e)}")


              
if st.button('Migrate'):
    st.spinner("Uploading data to PostgreSQL...")
    try:
        create_channel_table()
    except Exception as e:
        st.error(f"An error occurred while uploading data to PostgreSQL: {str(e)}")
    
    try:
        create_playlist_table()
    except Exception as e:
        st.error(f"An error occurred while uploading data to PostgreSQL: {str(e)}")
        
    try:
        create_video_table()
    except Exception as e:
        st.error(f"An error occurred while uploading data to PostgreSQL: {str(e)}")
        
    try:
        create_comment_table()
        st.success("Data uploaded successfully to PostgreSQL!") 
    except Exception as e:
        st.error(f"An error occurred while uploading data to PostgreSQL: {str(e)}")


question = ["Select", "What are the names of all the videos and their corresponding channels?",
                     "Which channels have the most number of videos, and how many videos do they have?",
                     "What are the top 10 most viewed videos and their respective channels?",
                     "How many comments were made on each video, and what are their corresponding video names?",
                     "Which videos have the highest number of likes, and what are their corresponding channel names?",
                     "What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                     "What is the total number of views for each channel, and what are their corresponding channel names?",
                     "What are the names of all the channels that have published videos in the year 2022?",
                     "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                     "Which videos have the highest number of comments, and what are their corresponding channel names?"
                     ]
question_selected = st.selectbox("Select the question to get answers", options=question)

if question_selected == "What are the names of all the videos and their corresponding channels?":
    st.dataframe(question1())
elif question_selected == 'What are the top 10 most viewed videos and their respective channels?':
    st.dataframe(question3())
elif question_selected == 'What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
    st.dataframe(question6())   
elif question_selected == 'What is the total number of views for each channel, and what are their corresponding channel names?':
    st.dataframe(question7())
elif question_selected == "What are the names of all the channels that have published videos in the year 2022?":
    st.dataframe(question8())
elif question_selected == "What is the average duration of all videos in each channel, and what are their corresponding channel names?":
    st.dataframe(question9())
