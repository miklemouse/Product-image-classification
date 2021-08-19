import csv
import os
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from math import sqrt

MAIN_IMG_FILENAME_COL = 5
CATEGORY_COL = 1
MIN_OBJ_IN_CAT = 100
MAX_OBJ_IN_CAT = 100

def csv_str_to_list(csv_string):

    if len(csv_string) < 2:
        return []
    elif csv_string[0] == '[' and csv_string[-1] == ']':
        split = csv_string[1:-1].split(', ')
        return [word[1:-1] for word in split]
    else:
        return ['']


def str_to_float_list(csv_string):

    if len(csv_string) < 2:
        return []
    elif csv_string[0] == '[' and csv_string[-1] == ']':
        split = csv_string[1:-1].split(', ')
        return [float(word) for word in split]


def get_categories():
    # key -- object number,
    # value -- object category number aka label
    categories = {}
    with open('labels.csv', 'r') as labels:
        reader = csv.reader(labels, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)

        first_line = True
        for row in reader:
            if first_line:
                first_line = False
                continue
            main_img_filename = csv_str_to_list(row[MAIN_IMG_FILENAME_COL])[0]
            category = int(row[CATEGORY_COL])

            obj_number = main_img_filename[:-6]
            categories[obj_number] = category
    return categories



def load_embeddings(categories):
    embeddings = []

    for i in range(551):
        if i % 50 == 0:
            print(i, 'out of', 551)
        filename = 'embeddings/embeddings' + str(i * 100) + '.csv'
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter = ',', quotechar = '"',
                                quoting = csv.QUOTE_ALL, skipinitialspace=True)
            for row in reader:
                category = categories[row[0]]
                csv_embeddings = row[1:]
                for csv_emb in csv_embeddings:
                    emb = str_to_float_list(csv_emb)
                    if emb != []:
                        embeddings.append((emb, category))
    print('loaded')

    return embeddings


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


categories = get_categories()
all_embeddings = load_embeddings(categories)

count_all_dict = {}
for emb in all_embeddings:
    category = emb[1]
    if not category in count_all_dict:
        count_all_dict[category] = 0
    count_all_dict[category] += 1

# embeddings = [emb for emb in all_embeddings if count_all_dict[emb[1]] >= MIN_OBJ_IN_CAT]

embeddings = []
count_current_dict = {}
for emb in all_embeddings:
    category = emb[1]
    if count_all_dict[category] >= MIN_OBJ_IN_CAT:
        if not category in count_current_dict:
            count_current_dict[category] = 0
        if count_current_dict[category] < MAX_OBJ_IN_CAT:
            embeddings.append(emb)
            count_current_dict[category] += 1


X = [emb[0] for emb in embeddings]
y = [emb[1] for emb in embeddings]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state = 2, stratify = y, shuffle = True)

neigh = KNeighborsClassifier(n_neighbors = 10, metric='euclidean')
neigh.fit(X_train, y_train)


def predict(X, y):
    correct = 0
    print('correct', 'in_total', '%')
    for i in range(len(X)):
        try:
            predict = neigh.predict([X[i]])[0]
            reality = y[i]
            if reality == predict:
                correct += 1
            if i%100 == 0 and i > 0:
                print(correct, i, str((correct / i) * 100) + '%')
        except KeyboardInterrupt:
            if i > 0:
                print(correct, i, str((correct / i) * 100) + '%')
            return
    return correct / len(X)
