import youtube_dl

def find_video(query):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    query = 'https://www.youtube.com/results?search_query=' + query
    with ydl:
        try:
            results = ydl.extract_info(
                query,
                download=False
            )
        except:
            results = ydl.extract_info(
                f"ytsearch:{query}", 
                download=False
            )

    filter = []
    results = results['entries']
    # for video in results:
    #     cleared_data = {
    #         'channel': video['uploader'],
    #         'channel_url': video['uploader_url'],
    #         'title': video['title'],
    #         'description': video['description'],
    #         'video_url': video['webpage_url'],
    #         'duration': video['duration'], #in seconds
    #         # 'upload_date': video['upload_data'], #YYYYDDMM
    #         'thumbnail': video['thumbnail'],
    #         'audio_source': video['formats'][0]['url'],
    #         'view_count': video['view_count'],
    #         'like_count': video['like_count'],
    #         'dislike_count': video['dislike_count'],
    #     }
    #     filter.append(cleared_data)

    for video in results:
        print(video['webpage_url'])
    return str(video['webpage_url'])

# search = input()
# ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
# query = 'https://www.youtube.com/results?search_query=' + query

