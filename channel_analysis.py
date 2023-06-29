import psycopg2 as pg2
import pandas as pd

conn = pg2.connect(
            host= 'localhost',
            database= 'project_data',
            user= 'postgres',
            password= 'vishal',
            port= 5432)


database = conn.cursor()
print("successful")

def question1():
    database.execute("SELECT channel.channel_name, video.title FROM channel JOIN video ON channel.channel_name = video.channel_name;")
    result = database.fetchall()
    df = pd.DataFrame(result, columns=['channel_name', 'video_title']).reset_index(drop=True)
    df.index += 1
    return df

result_df =question1()
print(result_df) 

def question3():
    database.execute("SELECT video.title, channel.channel_name, video.view_count FROM video JOIN channel ON video.channel_name = channel.channel_name ORDER BY video.view_count DESC LIMIT 10;")
    result = database.fetchall()
    df = pd.DataFrame(result, columns=['channel_name', 'title', 'View count']).reset_index(drop=True)
    df.index += 1
    return df
result_df =question3()
print(result_df) 

def question6():
    database.execute("SELECT title, like_count FROM video ORDER BY like_count DESC;")
    result = database.fetchall()
    df = pd.DataFrame(result, columns=['title', 'like_count']).reset_index(drop=True)
    df.index += 1
    return df
result_df =question6()
print(result_df) 

def question7():
    database.execute("SELECT channel_name, channel_views FROM channel ORDER BY channel_views DESC;")
    result = database.fetchall()
    df = pd.DataFrame(result, columns=['channel_name', 'total_number_of_views']).reset_index(drop=True)
    df.index += 1
    return df
result_df =question7()
print(result_df) 

def question8():
    database.execute("SELECT channel.channel_name, video.title, video.published_date FROM channel JOIN video ON channel.channel_name = video.channel_name WHERE EXTRACT(YEAR FROM video.published_date) = 2022;")
    result = database.fetchall()
    df = pd.DataFrame(result, columns=['channel_name', 'video_name', 'Year_2022']).reset_index(drop=True)
    df.index += 1
    return df

result_df =question8()
print(result_df)

def question9():
    database.execute("SELECT channel.channel_name, AVG(video.duration) AS average_duration FROM channel JOIN video ON channel.channel_name = video.channel_name GROUP BY channel.channel_name;")
    result = database.fetchall()
    df = pd.DataFrame(result, columns=['channel_name', 'average_duration_of_videos']).reset_index(drop=True)
    df['average_duration_of_videos'] = df['average_duration_of_videos'].astype(float)
    df['average_duration_of_videos'] = df['average_duration_of_videos'].round(2)
    df.index += 1
    return df

result_df =question9()
print(result_df)

