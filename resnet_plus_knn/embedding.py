from PIL import Image
import torchvision
from torchvision import transforms
import torch
import csv

from math import sqrt

model = torchvision.models.resnet34(pretrained=True)
modules = list(model.children())[:-1]
model = torch.nn.Sequential(*modules)

for p in model.parameters():
    p.requires_grad = False

model.eval()

# cosmetics
filename_one = "/Users/michaelrus/Documents/Internship/images/10000-M.jpg" 

# shoe
#filename_one = "/Users/michaelrus/Documents/Internship/images/5555-M.jpg"


# shoe
filename_two = "/Users/michaelrus/Documents/Internship/images/5557-M.jpg"


# cosmetics
#filename_two = "/Users/michaelrus/Documents/Internship/images/22504-M.jpg"

#filename_two = "/Users/michaelrus/Documents/Internship/images/5758-M.jpg"
#filename_two = "/Users/michaelrus/Documents/Internship/images/14407-M.jpg"
#filename_two = "/Users/michaelrus/Documents/Internship/images/5557-2.jpg"


def str_to_list(csv_string):

    if len(csv_string) < 2:
        return []
    elif csv_string[0] == '[' and csv_string[-1] == ']':
        split = csv_string[1:-1].split(', ')
        return [word[1:-1] for word in split]
    else:
        return ['']


def feature_embedding(filename):
    input_image = Image.open(filename)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(input_batch)

    embedding = [x[0][0] for x in output[0].unsqueeze(0).tolist()[0]]

    return embedding


IMG_FILENAMES_COL = 6
MAIN_IMG_FILENAME_COL = 5

def get_filenames():
    # key -- object number,
    # value -- list of filenames containing object's images
    filenames = {}
    with open('labels.csv', 'r') as labels:
        reader = csv.reader(labels, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)

        first_line = True
        for row in reader:
            if first_line:
                first_line = False
                continue
            main_img_filename = csv_str_to_list(row[MAIN_IMG_FILENAME_COL])[0]
            img_filenames = csv_str_to_list(row[IMG_FILENAMES_COL])

            obj_number = main_img_filename[:-6]
            filenames[obj_number] = [main_img_filename] + img_filenames
    return filenames


def get_embeddings(filenames):
    embeddings_file = open('embeddings/embeddings0.csv', 'w')
    writer = csv.writer(embeddings_file, delimiter=',', quotechar='"')

    count = 0
    for num, names in filenames.items():
        if count > 1000:
            break
        if count % 100 == 0 and count > 0:
            embeddings_file.close()
            csv_name = 'embeddings/embeddings' + str(count) + '.csv'
            embeddings_file = open(csv_name, 'w')
            writer = csv.writer(embeddings_file, delimiter=',', quotechar='"')

        count += 1
        row = [num]
        embeddings = []
        for filename in names:
            try:
                embeddings.append(feature_embedding('images/'+filename))
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except RuntimeError:
                print("error:", filename)
                embeddings.append('')
            except OSError:
                print("error:", filename)
                embeddings.append('')

        row += embeddings
        writer.writerow(row)

#filenames = get_filenames()
#print('done with reading:', len(filenames), 'filenames in total')

#get_embeddings(filenames)

emb_one = feature_embedding(filename_one)
emb_two = feature_embedding(filename_two)

print("len", len(emb_one))

cos_sim = 0
l_1, l_2 = 0, 0
for i in range(len(emb_one)):
    cos_sim += emb_one[i]*emb_two[i]
    l_1 += emb_one[i]*emb_one[i]
    l_2 += emb_two[i]*emb_two[i]

l_1 = sqrt(l_1)
l_2 = sqrt(l_2)

cosine = cos_sim / l_1 / l_2
print('cos_sim', cos_sim, 'l_1', l_1, 'l_2', l_2)
print('cos', cosine)
print()
print('dist', sqrt(2 * (1 - cosine)))