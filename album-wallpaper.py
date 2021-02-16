import argparse
from PIL import Image, ImageDraw, UnidentifiedImageError

# Take an image and return the most common perimeter color
def bg_color(im):
	colors = []
	for y in range(0, im.height - 1):
		if y == 0 or y == im.height - 1:
			for x in range(0, im.width - 1):
				colors.append(im.getpixel((x, y)))
		for i in (0, im.height - 1):
			colors.append(im.getpixel((i, y)))
	return max(colors, key = colors.count)

# Take an album cover and return it overlaid on a desktop sized background
def make_wallpaper(im):
	art_size = args.height - 100
	im = im.resize((art_size, art_size))
	output_im = Image.new("RGB", (args.width, args.height), bg_color(im))
	output_im.paste(im, ((args.width // 2) - (art_size // 2), 50))
	return output_im

parser = argparse.ArgumentParser(description="A Python cli application used to generate desktop wallpapers from album artwork.")
parser.add_argument("image", nargs="+", help="specify an album art image file to use")
parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1")
parser.add_argument("-x", "--width", type=int, help="specify the output width in pixels (default: %(default)s)", default=1920)
parser.add_argument("-y", "--height", type=int, help="specify the output height in pixels (default: %(default)s)", default=1080)
parser.add_argument("-d", "--output-directory", help="specify the output directory")
args = parser.parse_args()

for image in args.image:
	try:
		im = Image.open(image)
	except UnidentifiedImageError:
		sys.exit(f"Could not identify image: {args.image}")
	except FileNotFoundError:
		sys.exit(f"Could not find image: {args.image}")

	output_im = make_wallpaper(im)
	output_file = image.rsplit(".", 1)[0] + " - wallpaper.png"
	output_im.save(output_file)

