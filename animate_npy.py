'''
Animate supplied npy files
'''
import argparse
import numpy as np
import time
import Tkinter
from PIL import Image, ImageTk

def animate(matrices, w, h):
	mats = [np.load(x) for x in matrices]

	tk_win = Tkinter.Toplevel()
	tk_win.title('Escalator')
	canvas = Tkinter.Canvas(tk_win, width=7*w, height=7*h)
	canvas.pack()
	tk_ims = [None for _ in mats]
	for i, row in enumerate(mats[0]):
		ims = [Image.new('L', (w, h)) for _ in mats]
		for j, im in enumerate(ims):
			im.putdata(map(float, list(mats[j][i])))
			tk_ims[j] = ImageTk.PhotoImage(im)
			canvas.create_image((j * w) + 200, h, image = tk_ims[j])
			canvas.update()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'width',
		type = int,
		help = 'frame width'
	)
	parser.add_argument(
		'height',
		type = int,
		help = 'frame width'
	)
	parser.add_argument(
		'--npy-files',
		dest = 'npy_files',
		nargs = '+',
		help = 'numpy matrices'
	)

	parsed = parser.parse_args()

	animate(parsed.npy_files, parsed.width, parsed.height)