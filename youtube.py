from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=5JmaHz1xeOw&list=RD5JmaHz1xeOw&start_radio=1')
print(yt.order_by('resolution'))