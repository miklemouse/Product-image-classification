# Product-image-classification
Usage:

./download_and_preprocess.zsh small_dataset.csv cat 6 6 5 5

Arguments: original dataset with the links, parameter to sort by: either "cat" or "type", the amount of images in each category to download initially, the amount of categories to download initially, the amount of images in each category to sort out, the amount of categories to sort out

To clean it up:

rm -R small_dataset_*

