

from googleapiclient.discovery import build

api_key = 'AIzaSyCrK8SYvyZsUb_KWQhRy8PAhvcS4wRZtkw'
youtube = build("youtube", "v3", developerKey=api_key)
#channel_id=" "

def get_channel(channel_id):

    api_key = 'AIzaSyCrK8SYvyZsUb_KWQhRy8PAhvcS4wRZtkw'
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.channels().list( 
        part='snippet,contentDetails,statistics',
        id=channel_id)

    response = request.execute()

    data = {"channel_name": response['items'][0]['snippet']['title'],
            "subscribers": response['items'][0]['statistics']['subscriberCount'],
            "channel_description": response['items'][0]['snippet']['description'],
            "views_count": response['items'][0]['statistics']['viewCount'],
            "playlist_id": response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            }

    return data


def get_video_details(playlist_id):

    api_key = 'AIzaSyCrK8SYvyZsUb_KWQhRy8PAhvcS4wRZtkw'
    youtube = build("youtube", "v3", developerKey=api_key)

    video_ids = []

    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )

    response = request.execute()

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token)

            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

    return video_ids



def get_video_details_1(youtube, video_ids):
    
    youtube = build("youtube", "v3", developerKey=api_key)
    all_video_info = []

    for i in range(0, len(video_ids)):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_ids[i]
        )

        response = request.execute()

        for item in response['items']:
            video_stats = {'Title': item['snippet']['title'],
                           'Desc': item['snippet']['description'],
                           'Time': item['contentDetails']['duration'],
                           'PublishedAt': item['snippet']['publishedAt'],
                           'Views': item['statistics']['viewCount'],
                           'Caption': item['contentDetails']['caption'],
                           'Likes': item['statistics']['likeCount'],
                           'comments':video_comments(youtube, video_ids)
                    

                        }
            
           
            all_video_info.append(video_stats)

    return all_video_info



# to get video comments

def video_comments(youtube, video_ids):
    youtube = build("youtube", "v3", developerKey=api_key)
    all_comments = []


    for i in range(len(video_ids)):
        request = youtube.commentThreads().list(
            part="snippet, replies",
            videoId=video_ids[i],
            maxResults=100
        )
        try:
            response = request.execute()
            c = 0
            for comment in response['items']:
                Video_id = comment['snippet']['videoId']  # video_id
                commentss = comment['snippet']['topLevelComment']['snippet']['textOriginal']  # comment
                comment_author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']  # comment_author
                comment_like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']  # comment_like
                comment_Id = comment['snippet']['topLevelComment']['id']  # comment_Id
                Comment_publishedAt = comment['snippet']['topLevelComment']['snippet']['publishedAt']  # Comment_publishedAt

                all_comments.append({'Video_id': Video_id, 'comment': commentss, 'comment_author': comment_author,
                                     'comment_like_count': comment_like_count, 'comment_Id': comment_Id,
                                     'Comment_publishedAt': Comment_publishedAt})
        except:
            pass

        C_dict={}



        for i,comment in enumerate(all_comments,1):
            C_dict.update({f"comment_id_{i}":comment})

    return C_dict
            



def main_data(channel_id):
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    youtube = build("youtube", "v3", developerKey=api_key)
    

    channel_stats = get_channel(channel_id)
    playlist_id = channel_stats['playlist_id']
    video_ids = get_video_details(playlist_id)
    video_details = get_video_details_1(youtube, video_ids)
    
    c_video={"Channel_Name": channel_stats}

    for i,video in enumerate(video_details,1):
            c_video.update({f"video_ids_{i}":video})


    return c_video


    

    