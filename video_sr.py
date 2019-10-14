#!/usr/bin/env python3

import os
import skimage
import tensorflow as tf
import tensorlayer as tl
from video_sr_model import *
from video_sr_utils import *
from video_sr_config import config
import skvideo.io
import argparse
from keras import backend as K 

class Video_SR:

	def evaluate(self, video_path):
		## create folders to save result images

		tl.global_flag['mode'] = 'srgan'

		#save_dir = os.path.join("images", "srgan_frames")
		# tl.files.exists_or_mkdir(save_dir)
		checkpoint_dir = "checkpoint"
		
		read_video_filepath=os.path.join(os.getcwd(), video_path)
		
		videogen = skvideo.io.vreader(read_video_filepath)
		metadata = skvideo.io.ffprobe(read_video_filepath)
		metadata=metadata['video']
		H=int(metadata['@height'])
		W=int(metadata['@width'])
		fps=metadata['@r_frame_rate']
		
		C=3
		t_image = tf.placeholder('float32', [None, H, W, C], name='input_image')
		
		net_g = SRGAN_g(t_image, is_train=False, reuse=False)

		# # ###=============RESTORE G======================================================
		sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=False))
		tl.layers.initialize_global_variables(sess)
		tl.files.load_and_assign_npz(sess=sess, name=os.path.join(checkpoint_dir, 'g_srgan.npz'), network=net_g)
		write_video_filepath=os.path.join(os.getcwd(), 'videos', 'download', 'video.mp4')
		writer = skvideo.io.FFmpegWriter(write_video_filepath,inputdict={'-r': fps},outputdict={'-r': fps,'-vcodec': 'libx264','-pix_fmt': 'yuv420p'})    
		for i, frame in enumerate(videogen):        
			avg=frame.max()-frame.min()
			frame = (frame / avg) - 1  
			out = sess.run(net_g.outputs, {t_image: [frame]})
			#tl.vis.save_image(out[0], save_dir+'/'+str(i)+'.png')
			out=out[0]
			out=(255*(out-np.min(out))/(np.max(out)-np.min(out))).astype(np.uint8)
			writer.writeFrame(out)
			print (i)
			
		sess.close()
		K.clear_session()
		writer.close()

		# Optional open two vlcs to start at the same time in half windows to show the video. One low res and one hight res.
