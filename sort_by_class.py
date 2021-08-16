import csv
import os
from shutil import copyfile
from tqdm import tqdm
import getopt
import sys


def read_cat_by_img(cat_by_img_csv):
    cat_by_img = dict()
    with open(cat_by_img_csv, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            cat_by_img[row[0]] = row[1]
    return cat_by_img


def read_img_amount_csv(img_amount_csv):
    img_amount = dict()
    with open(img_amount_csv, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            img_amount[row[0]] = [int(row[1]), int(row[2])]
    return img_amount


def is_main_by_filename(filename):
    return filename[-5] == 'M'


def sort_by_type(img_folder, output_folder, cat_by_img,
                 img_amount, imgs_in_each, cats_in_total):
    """Sort by type (main/other) with equal amount of images in each
    category."""
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for subdir in ['M/', 'O/']:
        if os.path.exists(output_folder + subdir):
            files = os.listdir(output_folder + subdir)
            for file in files:
                os.remove(output_folder + subdir + file)
        else:
            os.mkdir(output_folder + subdir)

    cats_copied = dict()
    for cat, amount in img_amount.items():
        if amount[0] >= imgs_in_each and\
           amount[1] >= imgs_in_each:
           cats_copied[cat] = [0, 0]
        if len(cats_copied) >= cats_in_total:
            break
    if len(cats_copied) < cats_in_total:
        raise RuntimeError("Not sufficient amount of images for " +
                           "the parameters you've chosen.")

    for img, cat in tqdm(cat_by_img.items()):
        if len(cats_copied) == 0:
            break
        if cat not in cats_copied:
            continue
        if is_main_by_filename(img):
            if cats_copied[cat][0] < imgs_in_each:
                copyfile(img_folder + img,
                         output_folder + 'M/' + img)
                cats_copied[cat][0] += 1
        else:
            if cats_copied[cat][1] < imgs_in_each:
                copyfile(img_folder + img,
                         output_folder + 'O/' + img)
                cats_copied[cat][1] += 1
        if cats_copied[cat][0] >= imgs_in_each and\
           cats_copied[cat][1] >= imgs_in_each:
           del(cats_copied[cat])


def sort_by_cat(img_folder, output_folder, cat_by_img,
                 img_amount, imgs_in_each, cats_in_total):
    """Sort by type (main/other) with equal amount of images in each
    category."""
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    cats_copied = dict()
    for cat, amount in img_amount.items():
        if amount[0] + amount[1] >= imgs_in_each:
           cats_copied[cat] = 0
        if len(cats_copied) >= cats_in_total:
            break
    if len(cats_copied) < cats_in_total:
        raise RuntimeError("Not sufficient amount of images for " +
                           "the parameters you've chosen.")

    for subdir in cats_copied.keys():
        if os.path.exists(output_folder + subdir):
            files = os.listdir(output_folder + subdir)
            for file in files:
                os.remove(output_folder + subdir + '/' + file)
        else:
            os.mkdir(output_folder + subdir)

    for img, cat in tqdm(cat_by_img.items()):
        if len(cats_copied) == 0:
            break
        if cat not in cats_copied:
            continue
        if cats_copied[cat] < imgs_in_each:
            copyfile(img_folder + img,
                     output_folder + cat + '/' + img)
            cats_copied[cat] += 1

        if cats_copied[cat] >= imgs_in_each:
           del(cats_copied[cat])


def main(argv):

    img_folder = ''
    output_folder = ''

    sort_type = ''

    cat_by_img_csv = ''
    img_amount_csv = ''

    imgs_in_each = 0
    cats_in_total = 0

    try:
        opts, _ = getopt.getopt(argv, "hi:o:t:n:m:c:a:",
                                ["img_folder=",
                                 "output_folder=",
                                 "sort_type=",
                                 "imgs_in_cat=",
                                 "cat_amount=",
                                 "cat_by_img_csv=",
                                 "img_amount_csv="])

    except getopt.GetoptError:
        print ('sort_by_class.py -h for help')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('sort_by_class.py -i <img_folder> ' +
                   '-o <output_folder> -t <sort_type> ' +
                   '-n <imgs_in_cat> -m <cat_amount>' +
                   ' -c <cat_by_img_csv> -a <img_amount_csv>')
            print('Folder with the downloaded images <inp_file>')
            print('Folder to copy images to <output_folder>')
            print('<sort_type> is either "cat" or "type"')
            print('The amount of images and categories you need ' +
                  '<imgs_in_cat>, <cat_amount>')
            print('CSV file telling which category each image has ' +
                  '<cat_by_img_csv>')
            print('CSV file telling amount of images in each ' +
                  'category <img_amount_csv>')

            sys.exit()
        if opt in ["-i", "--img_folder"]:
            img_folder = arg
        elif opt in ["-o", "--output_folder"]:
            output_folder = arg
        elif opt in ["-t", "--sort_type"]:
            sort_type = arg
        elif opt in ["-n", "--imgs_in_cat"]:
            imgs_in_each = int(arg)
        elif opt in ["-m", "--cat_amount"]:
            cats_in_total = int(arg)
        elif opt in ["-c", "--cat_by_img_csv"]:
            cat_by_img_csv = arg
        elif opt in ["-a", "--img_amount_csv"]:
            img_amount_csv = arg

    if not img_folder or not output_folder or not sort_type or\
       not cat_by_img_csv or not img_amount_csv or not imgs_in_each or\
       not cats_in_total:
        print ('sort_by_class.py -h for help')
        sys.exit(2)

    if img_folder[-1] != '/':
        img_folder += '/'

    if output_folder[-1] != '/':
        output_folder += '/'


    cat_by_img = read_cat_by_img(cat_by_img_csv)
    img_amount = read_img_amount_csv(img_amount_csv)

    if sort_type == 'type':
        sort_by_type(img_folder, output_folder, cat_by_img,
                     img_amount, m_img_in_each, other_img_in_each,
                     cats_in_total)
    elif sort_type == 'cat':
        sort_by_cat(img_folder, output_folder, cat_by_img,
                    img_amount, imgs_in_each, cats_in_total)


if __name__ == '__main__':
    main(sys.argv[1:])
