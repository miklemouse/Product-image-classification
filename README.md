# Product-image-classification

python3 download_images.py -i small_dataset.csv -o test_images -n 5 -t 5

python3 convert_to_3_channels.py -i test_images

python3 delete_duplicates.py -i test_images

python3 label.py -f small_dataset.csv -i test_images -o test_images_info.csv --progress_check=30
