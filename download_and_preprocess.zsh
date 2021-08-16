set -e

FILE="$1"
TYPE="$2"
CATS="$3"
IMGS="$4"

CATS_="$5"
IMGS_="$6"

PREFIX=${FILE%.*}
IMG_FOLDER="${PREFIX}_img_folder"
FULL_INFO="${PREFIX}_full_info.csv"
CAT_BY_IMG="${PREFIX}_cat_by_img.csv"
IMG_AMOUNT="${PREFIX}_img_amount.csv"
SORTED="${PREFIX}_sorted_by_${TYPE}"

python3 download_images.py -i $FILE -o $IMG_FOLDER -n $IMGS -t $CATS

python3 convert_to_3_channels.py -i $IMG_FOLDER

python3 delete_duplicates.py -i $IMG_FOLDER

python3 label.py -f $FILE -i $IMG_FOLDER -o $FULL_INFO -c $CAT_BY_IMG -a $IMG_AMOUNT

python3 sort_by_class.py -i $IMG_FOLDER -o $SORTED -t $TYPE -n $IMGS_ -m $CATS_ -c $CAT_BY_IMG -a $IMG_AMOUNT
