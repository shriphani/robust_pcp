'''
Convert a bitmap sequence to matrix.
'''
import os
import numpy as np
import argparse
from PIL import Image

def bitmap_to_mat(bitmap_seq):
	matrix = []

	for bitmap_file in bitmap_seq:
		im = Image.open(bitmap_file).convert('L') # convert to grayscale
		pixels = list(im.getdata())
		matrix.append(pixels)

	return np.array(matrix)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('--bmp-dir', dest = 'bmp_dir')
	parser.add_argument('--bmp-out', dest = 'bmp_out')

	parsed = parser.parse_args()

	bmp_seq = map(
		lambda s: os.path.join(parsed.bmp_dir, s),
		os.listdir(parsed.bmp_dir)
	)
	res = bitmap_to_mat(bmp_seq)
	np.save(parsed.bmp_out, res)