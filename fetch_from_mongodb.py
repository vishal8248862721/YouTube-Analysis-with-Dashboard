from pymongo import MongoClient
import pandas as pd
import re
import streamlit as st
from datetime import datetime

def convert_duration(duration):
    regex = r'PT(\d+H)?(\d+M)?(\d+S)?' 
    match = re.match(regex, duration)
    if not match:
        return '00:00:00'

    hours, minutes, seconds = match.groups()
    hours = int(hours[:-1]) if hours else 0
    minutes = int(minutes[:-1]) if minutes else 0
    seconds = int(seconds[:-1]) if seconds else 0
    total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds

def connect_MongoDB():
    client = MongoClient(f"mongodb+srv://vishal:vishal123@cluster0.ol1geun.mongodb.net/?retryWrites=true&w=majority")
        
    database = client['project_testing']
    collection = database['channel_data']

    result=collection.find({})
    
    return result

def channel_from_MongoDB():
    
    channel= connect_MongoDB()
    data_list = {}
    
    if channel:
        for document in channel:
            channel=document.get("Channel_Name")
            Channel_name = channel.get('channel_name')
            Channel_Views = channel.get('views_count')
            Channel_Description = channel.get('channel_Description') or None
            
            data = {
                    "channel_name": Channel_name,
                    "channel_views": Channel_Views,
                    "channel_description": Channel_Description
                    }
            
            data_list.update(data)

            
        return pd.DataFrame(data_list,index=[0])
    
channel_from_MongoDB()       

def playlist_from_MongoDB():
    
    playlist = connect_MongoDB()
    
    data_list = []
    
    if playlist:
        for document in playlist:
            playlist=document.get("Channel_Name")
            Channel_name = playlist.get('channel_name')
            Playlist_Id = playlist.get('playlist_id')
           
            
            data = {
                    "channel_name": Channel_name,
                    "playlist_id": Playlist_Id,
                    
                    }
            
            data_list.append(data)
            
        return pd.DataFrame(data_list,index=[0])
    

def comments_from_MongoDB():
    comments = connect_MongoDB()
    data_list = []

    for document in comments:
        video_ids = [key for key in document.keys() if key.startswith('video_ids_')]
        
        for video_id_key in video_ids:
            video = document.get(video_id_key)
            comment_data = video.get('comments')
            
            comment_ids = [key for key in comment_data.keys() if key.startswith('comment_id_')]
            
            for comment_id_key in comment_ids:
                comment = comment_data.get(comment_id_key)
                
                data = {
                    'comment_id': comment.get('comment_Id'),
                    'video_id': comment.get('Video_id'),
                    'comment_text': comment.get('comment'),
                    'comment_author': comment.get('comment_author'),
                    'commentPublishedAt': pd.to_datetime(comment.get('Comment_publishedAt'))
                }
                
                data_list.append(data)
                

    return pd.DataFrame(data_list)
 
   




def videos_from_MongoDB():
    
    videos = connect_MongoDB()
    
    data_list = []
    for document in videos:
        #st.write(document)
        #video_id = [key for key in document.keys() if key.startswith('video_ids_')]
        #st.write(video_id)
        channel_name = document.get('Channel_Name',{}).get('channel_name')
        #st.write(channel_name)
        playlist_id = document.get('Channel_Name',{}).get('playlist_id')
        #duration = video_id.get('Duration')

        
        for key, value in document.items():
            #st.write(key,value)
            if key.startswith('video_ids_'):
        
                video_id = value
                duration = video_id.get('Time')
                published_str= pd.to_datetime(video_id.get('PublishedAt'))
                #published_date=datetime.fromisoformat(published_str)
                #st.write(published_date)
                data = {
                        'channel_name': channel_name,
                        #'video_id': document.get('Video_id'),
                        'playlist_id':playlist_id,
                        'video_description': video_id.get('Desc'),
                        'published_date':published_str, 
                        'view_count': video_id.get('Views'),
                        'like_count': video_id.get('Likes'),
                        'title': video_id.get('Title'),
                        'caption': video_id.get('Caption'),
                        'duration': convert_duration(duration)
                    
                        }
                        
                data_list.append(data)
                
                
    return pd.DataFrame(data_list)
                