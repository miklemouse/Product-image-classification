set -e

FILE="$1"
PREF="$2"
TYPE="$3"
CATS="$4"
IMGS="$5"

CATS_="$6"
IMGS_="$7"

IMG_FOLDER="${PREF}_img_folder"
FULL_INFO="${PREF}_full_info.csv"
CAT_BY_IMG="${PREF}_cat_by_img.csv"
IMG_AMOUNT="${PREF}_img_amount.csv"
SORTED="${PREF}_sorted_by_${TYPE}"
ZIP_FOLDER="${SORTED}.zip"

python3 download_images.py -i $FILE -o $IMG_FOLDER -n $IMGS -m $CATS -t $TYPE

python3 convert_to_3_channels.py -i $IMG_FOLDER

python3 delete_duplicates.py -i $IMG_FOLDER

python3 label.py -f $FILE -i $IMG_FOLDER -o $FULL_INFO -c $CAT_BY_IMG -a $IMG_AMOUNT

python3 sort_by_class.py -i $IMG_FOLDER -o $SORTED -t $TYPE -n $IMGS_ -m $CATS_ -c $CAT_BY_IMG -a $IMG_AMOUNT

zip -r $ZIP_FOLDER $SORTED 
