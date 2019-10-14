import numpy as np
from PIL import Image
from ISR.models import RDN
from os.path import join

class Image_SR:

	def evaluate(self, img_dir, save_dir):
		rdn = RDN(arch_params={'C':6, 'D':20, 'G':64, 'G0':64, 'x':2})
		rdn.model.load_weights('img_sr_weights/rdn-C6-D20-G64-G064-x2_ArtefactCancelling_epoch219.hdf5')
		img = Image.open(img_dir)
		lr_img = np.array(img)
		sr_img = rdn.predict(lr_img)
		sr_img = Image.fromarray(sr_img)
		sr_img.save(join(save_dir, "image.jpg"))
		