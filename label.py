"""Label

This script analyzes images downloaded with download_images.py and
generates a full list with filenames, URLs and categories.

Initial CSV file used by download_images.py            input_filename

CSV file to write the list to                         output_filename

The folder containing images                        image_folder_path
"""

from os import path
import csv
import copy
import getopt
import sys


def csv_str_to_list(csv_string):
    """
    Convert a string from csv file to list.

            Parameters:
                    csv_string (str): A string of form
                            "['text', '42', ..., 'text']"

            Returns:
                    List of string, e.g.
                            ['text', '42', ..., 'text']
    """
    if len(csv_string) < 2:
        return []
    elif csv_string[0] == '[' and csv_string[-1] == ']':
        split = csv_string[1:-1].split(', ')
        return [word[1:-1] for word in split]
    else:
        return ['']


def list_to_csv_str(arr):
    """
    Convert a list to a string of a specific format.

            Parameters:
                    List of string, e.g.
                            ['text', '42', ..., 'text']

            Returns:
                    csv_string (str): A string of form
                            "['text', '42', ..., 'text']"
    """
    if len(arr) == 0:
        return ''
    else:
        csv_string = '['
        for i in range(len(arr)):
            csv_string += "'" + arr[i] + "'"
            if i < len(arr) - 1:
                csv_string += ', '
        csv_string += ']'
        return csv_string


def check_main_image(item_number, image_folder_path):
    """
    Checks whether the item main image exists.

            Parameters:
                    item_number (int): The number of the item in the
                    list.

            Returns:
                    Tuple (bool, str): bool shows whether the image
                    exists, str containes the image filename if it
                    does; empty if it does not.
    """
    main_img_name = str(item_number) + '-M.jpg'
    if path.exists(image_folder_path + main_img_name):
        return (True, list_to_csv_str([main_img_name]), main_img_name)
    return (False, '', '')


def check_images(csv_urls, item_number, image_folder_path):
    """
    Checks whether the item images exist.

            Parameters:
                    csv_urls (str): A string of form
                    "['url_1', 'url_2', ..., 'url_42']"

                    item_number (int): The number of the item in the
                    list.

            Returns:
                    Tuple (bool, list): bool shows whether all the
                    images exist, list containes the image filenames
                    if they do; empty if they do not.
    """
    img_names = []
    img_urls = csv_str_to_list(csv_urls)
    for img_number in range(len(img_urls)):
        img_name = str(item_number) + '-' + str(img_number + 1) \
                   + '.jpg'
        if not path.exists(image_folder_path + img_name):
            return (False, '', [])
        img_names.append(img_name)

    return (True, list_to_csv_str(img_names), img_names)


def label(input_filename, output_filename, image_folder_path,
          cat_by_img_csv, img_amount_by_cat_csv,
          CAT_COL, CAT_NAME_COL, IMG_URLS_COL, MAIN_IMAGE_URL_COL,
          progress_check):
    """Write information about images to a CSV file.

            Parameters:
                    input_filename (str): Name of the original file
                    with URLS and other information about the images

                    output_filename (str): Name of the CSV file to
                    write the information to

                    image_folder_path (str): Name of the folder
                    containing the images
    """
    cat_by_img = dict()
    img_amount_by_cat = dict()

    with open(input_filename, 'r') as input_file,\
         open(output_filename, 'w') as output_file:
        reader = csv.reader(input_file, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL,
                            skipinitialspace=True)
        writer = csv.writer(output_file, delimiter=',', quotechar='"')

        line_number = -1
        for row in reader:
            line_number += 1

            if progress_check and line_number % progress_check == 0:
                print("Line:", line_number)

            newline_row = copy.deepcopy(row)
            if line_number == 0:
                newline_row += ['main_image_filename',
                                'image_filenames']
                writer.writerow(newline_row)

            else:
                cat = int(row[CAT_COL])

                if len(row) < 4 or row[MAIN_IMAGE_URL_COL] == '':
                    continue

                m_img_exists, m_img_name, m_img_real_name = check_main_image(
                                                                line_number,
                                                                image_folder_path
                                                            )
                if m_img_exists:
                    newline_row.append(m_img_name)
                    csv_urls = row[IMG_URLS_COL]
                    imgs_exist, img_names, real_img_names = check_images(
                                                             csv_urls,
                                                             line_number,
                                                             image_folder_path
                                                            )
                    cat_by_img[m_img_real_name] = cat
                    if not cat in img_amount_by_cat:
                        img_amount_by_cat[cat] = [0, 0, row[CAT_NAME_COL]]
                    img_amount_by_cat[cat][0] += 1
                    if imgs_exist:
                        newline_row.append(img_names)
                        writer.writerow(newline_row)
                        for img_name in real_img_names:
                            cat_by_img[img_name] = cat
                            img_amount_by_cat[cat][1] += 1

    with open(cat_by_img_csv, 'w') as cat_by_img_file:
        writer = csv.writer(cat_by_img_file)
        for img, cat in cat_by_img.items():
            writer.writerow([img, cat])

    with open(img_amount_by_cat_csv, 'w') as img_amount_by_cat_file:
        writer = csv.writer(img_amount_by_cat_file)
        for cat, amount in img_amount_by_cat.items():
            writer.writerow([cat] + amount)

def main(argv):

    CAT_COL = 1
    CAT_NAME_COL = 4
    IMG_URLS_COL = 2
    MAIN_IMAGE_URL_COL = 3

    input_filename = ""
    image_folder_path = ""
    output_filename = ""
    img_amount_by_cat_csv = ""
    cat_by_img_csv = ""
    progress_check = 0

    try:
        opts, _ = getopt.getopt(argv, "hf:i:o:c:a:p:",
                                ["input_file=",
                                 "img_folder=",
                                 "output_file=",
                                 "cat_by_img_csv=",
                                 "img_amount_by_cat_csv=",
                                 "progress_check="])

    except getopt.GetoptError:
        print ('label.py -h for help')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('label.py -f <input_file> -i <img_folder> ' +
                   '-o <output_file> -c <cat_by_img_csv> ' +
                   '-a <img_amount_by_cat_csv> -p [progress_check]')
            print('The CSV file with object info <input_file>')
            print('The folder with the downloaded images <img_folder>')
            print('The file to write the general info <output_file>')
            print('The file to write category of each image ' +
                  '<cat_by_img_csv>')
            print('The file to write image amount in each category ' +
                  '<img_amount_by_cat_csv>')
            print('Print progress every [progress_check] lines')
            sys.exit()
        if opt in ["-f", "--input_file"]:
            input_filename = arg
        elif opt in ["-i", "--img_folder"]:
            image_folder_path = arg
        elif opt in ["-o", "--output_file"]:
            output_filename = arg
        elif opt in ["-c", "--cat_by_img_csv"]:
            cat_by_img_csv = arg
        elif opt in ["-a", "--img_amount_by_cat_csv"]:
            img_amount_by_cat_csv = arg
        elif opt in ["-p", "--progress_check"]:
            progress_check = int(arg)

    if not input_filename or not image_folder_path or\
       not output_filename or not img_amount_by_cat_csv or\
       not cat_by_img_csv:
        print ('label.py -h for help')
        sys.exit(2)

    if image_folder_path[-1] != '/':
        image_folder_path += '/'

    # Write information about images in the CSV file
    print("Labeling images...")
    label(input_filename, output_filename, image_folder_path,
          cat_by_img_csv, img_amount_by_cat_csv,
          CAT_COL, CAT_NAME_COL, IMG_URLS_COL, MAIN_IMAGE_URL_COL,
          progress_check)


if __name__ == '__main__':
    main(sys.argv[1:])
