"""Convert to 3 channels

Converts all the images in the folder to 3 channels.
"""

from PIL import Image
import os
from tqdm import tqdm
import sys
import getopt

def convert_image(filename):
    """Converts an image to RGB."""
    with open(filename, 'rb') as f:
        img = Image.open(f)
        input_image = img.convert('RGB')
    input_image.save(filename)


def convert_all_in_folder(img_folder):
    img_list = [img_folder + file for file in os.listdir(img_folder)]

    for img in tqdm(img_list):
        convert_image(img)


def main(argv):

    img_folder = ''

    try:
        opts, _ = getopt.getopt(argv, "hi:", ['img_folder='])
    except getopt.GetoptError:
        print('convert_to_3_channels.py -h for help')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('convert_to_3_channels.py -i <img_folder>')
            sys.exit()
        elif opt in ['-i', '--img_folder']:
            img_folder = arg

    if not img_folder:
        print('convert_to_3_channels.py -h for help')
        sys.exit(2)

    if img_folder[-1] != '/':
        img_folder += '/'

    # convert all images in the folder to 3 channels
    print("Converting the images to 3 channels")
    convert_all_in_folder(img_folder)

if __name__ == '__main__':
    main(sys.argv[1:])
