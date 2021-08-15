"""Find duplicates

The script will find images with the same phash and write their
filenames to a csv file.
"""

from PIL import Image, ImageChops
import imagehash
import os
from tqdm import tqdm
import csv
import sys
import getopt


def get_phash(img_name, img_folder):
    """
    Get hash of the image with filename img_name located in the
    img_folder.

            Parameters:
                    img_name (str): filename of the image, e.g.
                    '0001.jpg'

                    img_folder (str): folder with the image, e.g.
                    'image_folder/'

            Returns:
                    phash of the image
    """
    return imagehash.phash(Image.open(img_folder+img_name))


def hash_dups_dict(img_folder):
    """
    Classify images by their hashes.

            Parameters:
                    img_folder (str): the folder with the images, e.g.
                    'image_folder/'

            Returns:
                    A dictionary hash_dict.
                    hash_dict[hash_0] = ['img_1.jpg', 'img_2.jpg', ...]
                    where all the images [img_1.jpg, img_2.jpg, ...]
                    have the same hash hash_0.
    """
    images = os.listdir(img_folder)

    hash_dict = dict()
    for img_name in tqdm(images):
        if not img_name[0].isnumeric() or\
           img_name[-4:] != '.jpg':
            continue

        h = get_phash(img_name, img_folder)
        if h not in hash_dict:
            hash_dict[h] = []

        hash_dict[h].append(img_name)

    return hash_dict


def delete_duplicates(img_folder, hash_dict):
    """Deletes all the hash duplicates from the folder. After running
       this function there will be only one representative of each
       hash left.

            Parameters:
                    img_folder (str): the name of the folder with the
                    images

                    hash_dict (dict): the result of the hash_dups_dict
    """
    for img_list in tqdm(hash_dict.values()):
        for img in img_list[1:]:
            os.remove(img_folder + img)


def write_down(output_csv, hash_dict):
    """Writes down the result of the hash_dups_dict to a csv.

            Parameters:
                    output_csv (str): the filename of the output CSV,
                    e.g. 'output.csv'

                    hash_dict (dict): the result of the hash_dups_dict
    """
    with open(output_csv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for img_list in hash_dict.values():
            writer.writerow(img_list)


def main(argv):

    img_folder = ''
    output_csv = ''

    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["img_folder=",
                                                "output_csv="])
    except getopt.GetoptError:
        print ('delete_duplicates.py -h for help')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('delete_duplicates.py -i <img_folder> ' +
                   '-o [output_csv]')
            print('<img_folder> is the name of the folder with the ' +
                  'images, e.g. images/')
            print('[output_csv] is a name of a CSV file in case you ' +
                  'need to keep track of the deleted images, e.g. ' +
                  'hash_dups.csv')
            sys.exit()
        if opt in ["-i", "--img_folder"]:
            img_folder = arg
        elif opt in ["-o", "--output_csv"]:
            output_csv = arg

    print('img_folder:', img_folder)

    if not img_folder:
        print ('delete_duplicates.py -h for help')
        sys.exit(2)

    if img_folder[-1] != '/':
        img_folder.append('/')

    # generate dictionary of hash duplicates
    print("Searching for duplicates...")
    hash_dict = hash_dups_dict(img_folder)

    # delete extra images
    print("Deleting extra duplicates...")
    delete_duplicates(img_folder, hash_dict)

if __name__ == '__main__':
    main(sys.argv[1:])
