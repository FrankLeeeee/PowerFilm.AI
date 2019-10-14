from flask import Flask, Response, request, jsonify, send_from_directory, send_file
from image_sr import Image_SR
from video_sr import Video_SR
from voice_st import Voice_ST
import os
from werkzeug.utils import secure_filename
import pickle

app = Flask(__name__, static_folder='', static_url_path='')

image_sr_model = Image_SR()
video_sr_model = Video_SR()
voice_st_model = Voice_ST()

@app.route('/', methods=['GET'])
def main_page():
	return send_file('templates/index.html')

@app.route('/img_sr', methods = ['POST', 'GET'])
def img_sr():
	if request.method == 'POST':
		image = request.files['image']
		image.save(os.path.join('images/upload', secure_filename("image.jpg")))
		image_sr_model.evaluate('images/upload/image.jpg', 'images/download')
		res = {'msg': 'success'}
		return jsonify(res)
	
	elif request.method == 'GET':
		return send_file('images/download/image.jpg', attachment_filename="image.jpg", as_attachment=True,)

@app.route('/video_sr', methods = ['GET', 'POST'])
def video_sr():
	if request.method == 'POST':
		video = request.files['video']
		video.save(os.path.join('videos/upload', secure_filename('video.mp4')))
		video_sr_model.evaluate('videos/upload/video.mp4')

		res = {"msg": "success"}
		return jsonify(res)

	elif request.method == 'GET':
		return send_file("videos/download/video.mp4", attachment_filename= 'video.mp4', as_attachment= True,)

@app.route('/audio_st', methods=['POST', 'GET'])
def voice_st():

    if request.method == 'POST':
        source = request.files['source_audio']
        target = request.files['target_audio']

        source_name = secure_filename("source.wav")
        target_name = secure_filename("target.wav")

        source_path = os.path.join('audio/upload', source_name)
        target_path = os.path.join('audio/upload', target_name)

        source.save(source_path)
        target.save(target_path)
        
        # do the conversion
        # the converter returns the path of the converted file
        converter = Voice_ST()
        converter.run(source_path, target_path)

        data = {"msg": 'success'}
        return jsonify(data)

    elif request.method == 'GET':
        return send_file("audio/download/audio.wav", attachment_filename='audio.wav',
                         as_attachment=True, )


if __name__ == "__main__":
	app.run(port=3000)