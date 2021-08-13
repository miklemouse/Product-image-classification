"""Label

This script analyzes images downloaded with download_images.py and
generates a full list with filenames, URLs and categories.

To specify parameters, please adjust global variables in the script:

Initial CSV file used by download_images.py            input_filename

CSV file to write the list to                         output_filename

The folder containing images                        image_folder_path
"""

from os import path
import csv
import copy

input_filename = "dump_with_category.csv"
output_filename = "1000x100.csv"
image_folder_path = "1000x100/"

IMG_URLS_COL = 2
MAIN_IMAGE_URL_COL = 3


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


def check_main_image(item_number):
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
        return (True, list_to_csv_str([main_img_name]))
    return (False, '')


def check_images(csv_urls, item_number):
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
            return (False, [])
        img_names.append(img_name)

    return (True, list_to_csv_str(img_names))


with open(input_filename, 'r') as input_file,\
     open(output_filename, 'w') as output_file:
    reader = csv.reader(input_file, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL, skipinitialspace=True)
    writer = csv.writer(output_file, delimiter=',', quotechar='"')

    line_number = -1
    for row in reader:
        line_number += 1

        if line_number % 100000 == 0:
            print("Line:", line_number)

        newline_row = copy.deepcopy(row)
        if line_number == 0:
            newline_row += ['main_image_filename', 'image_filenames']
            writer.writerow(newline_row)

        else:
            if len(row) < 4 or row[MAIN_IMAGE_URL_COL] == '':
                continue
            m_img_exists, m_img_name = check_main_image(line_number)
            if m_img_exists:
                newline_row.append(m_img_name)
                csv_urls = row[IMG_URLS_COL]
                imgs_exist, img_names = check_images(csv_urls, line_number)
                if imgs_exist:
                    newline_row.append(img_names)
                    writer.writerow(newline_row)
                else:
                    print("incomplete data", line_number, img_names)
