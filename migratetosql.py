import psycopg2 as pg2
from fetch_from_mongodb import *

conn = pg2.connect(
            host= 'localhost',
            database= 'project_data',
            user= 'postgres',
            password= 'vishal',
            port= 5432)


database = conn.cursor()
print("successful")


def create_channel_table():

    database.execute('DROP TABLE IF EXISTS channel')
    database.execute('''
                    CREATE TABLE IF NOT EXISTS channel(
                                channel_name VARCHAR(255),
                                channel_views INT,
                                channel_Description TEXT
                    )
                ''')
    
    print("Table created")

    query = '''
            INSERT INTO channel (channel_name,channel_views, channel_description)
            VALUES (%s, %s, %s)
    '''
    channel_df = channel_from_MongoDB()
    


    for _, row in channel_df.iterrows():
            try:
                values = tuple(row)
                database.execute(query, values)
            except:
                pass

    print("Data inserted into 'channel' table.")
    


def create_playlist_table():
    database.execute('DROP TABLE IF EXISTS playlist')
    database.execute('''
        CREATE TABLE IF NOT EXISTS playlist(
            Channel_name VARCHAR(255),
            Playlist_Id VARCHAR(255) PRIMARY KEY
        )
    ''')
    print("Table 'playlist' created.")

    query = '''
        INSERT INTO playlist (Channel_name, Playlist_Id)
        VALUES (%s, %s)
    '''
    playlist_df = playlist_from_MongoDB()

    for _, row in playlist_df.iterrows():
        try:
            values = tuple(row)
            database.execute(query, values)
        except:
            pass

    print("Data inserted into 'playlist' table.")


def create_video_table():
    database.execute('DROP TABLE IF EXISTS video')
    database.execute('''CREATE TABLE IF NOT EXISTS video(
                                    channel_name       VARCHAR(255),
                                    playlist_id        VARCHAR(255),
                                    video_description   TEXT,
                                    published_date      TIMESTAMP,
                                    view_count          INT,
                                    like_count          INT,
                                    title               varchar(255),
                                    caption             VARCHAR(255),
                                    duration            INT

                        )
    ''')
    
    query = '''
                INSERT INTO video (channel_name,playlist_id,video_description,published_date,view_count,like_count,title,caption,duration)          
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
            '''
            
    video_df = videos_from_MongoDB()

    for _, row in video_df.iterrows():
        values = tuple(row)
        database.execute(query, values)
    conn.commit()


def create_comment_table():

    database.execute('DROP TABLE IF EXISTS comment')

    database.execute('''CREATE TABLE IF NOT EXISTS comment(
                                comment_id              VARCHAR(255) ,
                                video_id                VARCHAR(255) ,
                                comment_text            TEXT,
                                comment_author          VARCHAR(255),
                                CommentPublishedAt      TIMESTAMP)'''
                     )

    query = '''
            INSERT INTO comment (comment_id,video_id, comment_text, comment_author, CommentPublishedAt)
            VALUES (%s,%s,%s,%s,%s)
            '''
    comment_df = comments_from_MongoDB()

    for _, row in comment_df.iterrows():
            values = tuple(row)
            database.execute(query, values)      
        
    conn.commit()




    
