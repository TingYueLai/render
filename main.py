from pytube import YouTube
import ssl
from flask import Flask, render_template, send_file, request
import os

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"已成功刪除檔案: {file_path}")
    except Exception as e:
        print(f"刪除檔案時發生錯誤: {e}")

def mp3sownload(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path='file/' , filename="download.mp3")

ssl._create_default_https_context = ssl._create_stdlib_context
def download_youtube_video(url, file_path):
    try:
        yt = YouTube(url)

        video_stream = yt.streams.get_highest_resolution()

        video_stream.download(output_path=file_path,filename='download.mp4')
        print("影片已下載到:", file_path)
        return yt.title
    except Exception as e:
        print("下載影片時發生錯誤:", e)
        return yt.title
    


video_url = 'https://www.youtube.com/watch?v=5o53fdEV7F0'  
file_path = 'file/'  
#download_youtube_video(video_url, file_path)
app = Flask(__name__)
@app.route("/")
def Main_page():
    return 'nothing'


@app.route("/mp3")
def mp3():
    return render_template("mp3.html")
@app.route('/login/mp3', methods=["GET", "POST"])
def mp3login():

    if request.method == 'GET':
      return render_template("mp3.html")
    else:
        delete_file('file/download.mp3')
        url = request.form['UU']
        mp3sownload(url)
        PATH = 'file/download.mp3'
        return send_file(PATH, as_attachment=True)
    



@app.route("/mp4")
def mp4():
    return render_template("mp4.html")
@app.route('/login/mp4', methods=["GET", "POST"])
def login():

    if request.method == 'GET':
      return render_template("mp4.html")
    else:
        delete_file('file/download.mp4')
        url = request.form['UU']
        title=download_youtube_video(url,'file/')
        PATH = 'file/download.mp4'
        return send_file(PATH, as_attachment=True)


#fff/name_env/file/123.mp4
@app.route('/download/<username>')
def Download_File(username):
    PATH = 'file/'+username+".mp4"
    return send_file(PATH, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)