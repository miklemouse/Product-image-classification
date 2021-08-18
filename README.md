# Product image classification

## Datasets

777x20_main:
https://drive.google.com/file/d/1JvA-I5GAhO-LnU9Uc_scg7HlVzFCogls/view?usp=sharing

Or download using scripts:

./download_and_preprocess.zsh dump_with_category.csv 777x20 cat 1000 100 777 20

100x50_main:
https://drive.google.com/file/d/1vWcaJOQ8trVMiwuyIVMAE_QsKAUhYRBY/view?usp=sharing

Or download using scripts:
./download_and_preprocess.zsh dump_with_category.csv 100x50 cat 110 70 100 50

Note: in order to download with the scripts you need to have dump_with_category.csv. It can be downloaded here:

https://drive.google.com/file/d/1rV1eqUl0vqC6Y6JYrNR1Lvh_5zzGybpq/view?usp=sharing

## Checkpoints

https://drive.google.com/drive/folders/1hWWqevcekudrhg8Fbzo4QlZITSct9U_f?usp=sharing

## Models

To test a model:

Copy the checkpoint folder in Google Drive

Download the corresponding dataset (either 777x20_main or 100x50_main)

Open colab/classification_by_category.ipynb in Google Colab

Change the variable in the second cell of the classification_by_category.ipynb script:

chkpt_path = 'drive/MyDrive/' +\
             'Checkpoints_sorted/65_perc_dm_100x50_main/epoch=2-step=164.ckpt'

And the name of the zip-folder in the second cell of the script:

!cp -u /content/drive/MyDrive/100x50_main.zip ./
!unzip -q -n 100x50_main.zip -d temp_unzip_dir/

Run all the cells

## download_and_preprocess.zsh usage:

./download_and_preprocess.zsh small_dataset.csv small_ds cat 6 6 5 5

Arguments: original dataset with the links, prefix for all the files created, parameter to sort by: either "cat" or "type", amount of categories to download initially, amount of images in each category to download initially, amount of categories to sort out, amount of images in each category to sort out

To clean it up: rm -R small_dataset_*

