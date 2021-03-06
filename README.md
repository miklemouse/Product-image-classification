# Color classification sample results:

<img src="https://github.com/miklemouse/Product-image-classification/blob/main/Color-classification-results.jpg" height=600 />


## Results

0. Classification by category, accuracy 55% (1000 categories, 100 images in each, duplicates have not been removed in this experiment). Feature embedding created with pretrained resnet34 from torchvision, and then passed to K-Neighbours Classifier (from scipy).
1. Classification by category, accuracy 65% (100 categories, 50 images in each). Model -- resnet34 trained with pytorch-lightning, loss -- the negative log likelihood loss.
2. Binary classification Main image / Other image, accuracy 60% (777 categories, 40 images in each). Model -- resnet34 trained with pytorch-lightning, loss -- the negative log likelihood loss.
3. Color classification, determine all the colors. Model -- resnet34 trained with python-lightning, loss -- binary cross entropy. Two approaches: choose checkpoint with (1) the greatest recall or (2) the least loss. 1st one: recall 30%, precision 50%. 2nd one: recall 20%, precision 56%. (Only main images) 
4. Color classification, determine 10 simple colors. Model -- resnet34 trained with python-lightning, loss -- binary cross entropy. Two approaches: choose checkpoint with (1) the greatest recall or (2) the least loss. 1st one: recall 68%, precision 76%. 2nd one: recall 56%, precision 81%. (Only main images) (Colors: ['red', 'yellow', 'blue', 'orange', 'green', 'purple', 'beige', 'pink', 'white', 'black'] aka ['красный', 'желтый', 'голубой', 'оранжевый', 'зеленый', 'фиолетовый', 'бежевый', 'розовый', 'белый', 'черный'])
As I trained the model in 3. and 4., precision was decreasing whereas recall was inscreasing.
## Datasets

777x20_main:
https://drive.google.com/file/d/1JvA-I5GAhO-LnU9Uc_scg7HlVzFCogls/view?usp=sharing

Or download using scripts:

./download_and_preprocess.zsh dump_with_category.csv 777x20 cat 1000 100 777 20

100x50_main:
https://drive.google.com/file/d/1vWcaJOQ8trVMiwuyIVMAE_QsKAUhYRBY/view?usp=sharing

Or download using scripts:
./download_and_preprocess.zsh dump_with_category.csv 100x50 cat 110 70 100 50

Note: in order to download with these scripts you need to have dump_with_category.csv. It can be downloaded here:

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

## Scripts
To run all the scripts:

./download_and_preprocess.zsh small_dataset.csv small_ds cat 6 6 5 5

Arguments: original dataset with the links, prefix for all the files created, parameter to sort by: either "cat" or "type", amount of categories to download initially, amount of images in each category to download initially, amount of categories to sort out, amount of images in each category to sort out

To clean it up: rm -R small_ds_*

