from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=5JmaHz1xeOw&list=RD5JmaHz1xeOw&start_radio=1')
filters = yt.streams.filter(progressive=True, file_extension='mp4')
high = filters.get_highest_resolution()
low = filters.get_lowest_resolution()
audio = yt.streams.get_audio_only()
#high.download(filename = 'download_out', output_path='')
title = yt.title
print(title)