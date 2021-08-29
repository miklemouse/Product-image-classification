set -e

FILE="$1"
PREF="$2"
SORT_TYPE="$3"
DOWNLOAD_TYPE="$4"
DS_TYPE="$5"
CATS="$6"
IMGS="$7"

CATS_="$8"
IMGS_="$9"

IMG_FOLDER="${PREF}_img_folder"
FULL_INFO="${PREF}_full_info.csv"
CAT_BY_IMG="${PREF}_cat_by_img.csv"
COLOR_BY_IMG="${PREF}_color_by_img.csv"
IMG_AMOUNT="${PREF}_img_amount.csv"
SORTED="${PREF}_sorted_by_${SORT_TYPE}"
ZIP_FOLDER="${SORTED}.zip"

#python3 download_images.py -i $FILE -o $IMG_FOLDER -n $IMGS -m $CATS -t $DOWNLOAD_TYPE -b 777x20_im

#python3 convert_to_3_channels.py -i $IMG_FOLDER

#python3 delete_duplicates.py -i $IMG_FOLDER

#python3 label.py -f $FILE -i $IMG_FOLDER -o $FULL_INFO -c $CAT_BY_IMG -a $IMG_AMOUNT -t DS_TYPE -l $COLOR_BY_IMG

python3 sort_by_class.py -i $IMG_FOLDER -o $SORTED -t $SORT_TYPE -n $IMGS_ -m $CATS_ -c $CAT_BY_IMG -a $IMG_AMOUNT -f $COLOR_BY_IMG

zip -r $ZIP_FOLDER $SORTED 
