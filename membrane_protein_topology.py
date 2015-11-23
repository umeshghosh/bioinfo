
import Image
import ImageDraw
import ImageFont

def draw_object(position, sequence):

	counter = 0

	for j in range(20):
		for i in range(4 - j % 2):
			if j % 2 == 1:
				translate = SIZE / 2
			else:
				translate = 0
			draw.ellipse((SIZE * i + translate + position[0],SIZE * j + position[1],SIZE * (i + 1) + translate + position[0],SIZE * (j + 1) + position[1]), None, (0,0,0))
			draw.text((SIZE * i + translate + TRANSX + position[0], SIZE * j + TRANSY + position[1]), sequence[counter], (0,0,0), sans16)
			counter = counter + 1

#-----------------------------------

fontPath = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
sans16 = ImageFont.truetype ( fontPath, 16 )


im = Image.new('RGB', (600,600), (255, 255, 255))

draw = ImageDraw.Draw(im)

SIZE = 20
TRANSX = 5
TRANSY = 1

sequence = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"

draw_object((0,0), sequence)
draw_object((120,20), sequence)
draw_object((240,10), sequence)
draw_object((360,30), sequence)
draw_object((480,0), sequence)

im.show()
im.save('test.png', 'PNG')
