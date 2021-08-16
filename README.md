# Product-image-classification

python3 download_images.py -i small_dataset.csv -o test_images -n 5 -t 5

python3 convert_to_3_channels.py -i test_images

python3 delete_duplicates.py -i test_images

python3 label.py -f small_dataset.csv -i test_images/ -o test.csv -c cat_by_img.csv -a img_amount.csv

python3 sort_by_class.py -i test_images -o sorted_by_class -t cat -n 5 -m 5 -c cat_by_img.csv -a img_amount.csv 
