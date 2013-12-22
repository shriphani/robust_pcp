'''
Animate supplied npy files
'''
import argparse
import numpy as np
import Tkinter
from PIL import Image, ImageTk

def animate(matrices, w, h):
	mats = [np.load(x) for x in matrices]

	tk_win = Tkinter.Tk()
	tk_win.title('Escalator')
	canvas = Tkinter.Canvas(tk_win, width=7*w, height=7*h)
	canvas.pack()

	for i, row in enumerate(mats[0]):
		ims = [Image.new('L', (w, h)) for _ in mats]
		for j, im in enumerate(ims):
			im.putdata(map(float, list(row)))
			tk_ims = ImageTk.PhotoImage(im)
			canvas.create_image(j * w, h, image = im)
			canvas.update()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--npy-files',
		dest = 'npy_files',
		nargs = '+',
		help = 'numpy matrices'
	)

	parsed = parser.parse_args()

	animate(parsed.npy_files, 160, 130)