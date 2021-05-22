import os
import cv2
import pandas as pd
import numpy as np
import imgaug.augmenters as iaa
from sklearn.utils import shuffle

from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import random

# 1 - INITIALIZE DATA
def get_name(filepath):
    '''
    Returns the path of the image and its current directory
    '''
    image_path_list = filepath.split('/')[-2:]
    image_path = os.path.join(image_path_list[0], image_path_list[1])
    return image_path

def import_data_info(path):
    '''
    Converts the contents of the log csv file
    into a pandas data frame
    '''
    columns = ['ImgPath', 'Steering']
    no_of_folders = len(os.listdir(path)) // 2
    data = pd.DataFrame()
    for x in range(no_of_folders):
        data_new = pd.read_csv(os.path.join(path, f'log_{x}.csv'), names=columns)
        print(f'{x}:{data_new.shape[0]}')
        data_new['ImgPath'] = data_new['ImgPath'].apply(get_name)
        data = data.append(data_new, True)
    print('')
    print('Total Images Imported', data.shape[0])
    return data

# 2 - VISUALIZE AND BALANCE DATA
def balance_data(data, samples_per_bin=300, display=True):
    '''
    Balances the data to prevent overfitting
    '''
    n_bin = 31
    hist, bins = np.histogram(data['Steering'], n_bin)
    if display:
        center = (bins[:-1] + bins[1:]) * 0.5
        plt.bar(center, hist, width=0.03)
        plt.plot((np.min(data['Steering']), np.max(data['Steering'])), (samples_per_bin, samples_per_bin))
        plt.title('Data Visualization')
        plt.xlabel('Steering Angle')
        plt.ylabel('No of Samples')
        plt.show()
    remove_index_list = []
    for j in range(n_bin):
        bin_data_list = []
        for i in range(len(data['Steering'])):
            if data['Steering'][i] >= bins[j] and data['Steering'][i] <= bins[j + 1]:
                bin_data_list.append(i)
        bin_data_list = shuffle(bin_data_list)
        bin_data_list = bin_data_list[samples_per_bin:]
        remove_index_list.extend(bin_data_list)
    print('Removed Images: ', len(remove_index_list))
    data.drop(data.index[remove_index_list], inplace=True)
    print('Remaining Images: ', len(data))
    if display:
        hist, _ = np.histogram(data['Steering'], (n_bin))
        plt.bar(center, hist, width=0.03)
        plt.plot((np.min(data['Steering']), np.max(data['Steering'])), (samples_per_bin, samples_per_bin))
        plt.title('Balanced Data')
        plt.xlabel('Steering Angle')
        plt.ylabel('No of Samples')
        plt.show()
    return data

# 3 - PREPARE FOR PROCESSING
def load_data(path, data):
    images_path = []
    steering = []
    for i in range(len(data)):
        indexed_data = data.iloc[i]
        images_path.append(os.path.join(path, indexed_data[0]))
        steering.append(float(indexed_data[1]))
    images_path = np.asarray(images_path)
    steering = np.asarray(steering)
    return images_path, steering

# 5 - AUGMENT IMAGES
def augment_image(img_path, steering):
    '''
    Reads an image from a given path
    and then randomly augments the image
    '''
    img = cv2.imread(img_path)
    if np.random.rand() < 0.5:
        pan = iaa.Affine(translate_percent={'x': (-0.1, 0.1), 'y': (-0.1, 0.1)})
        img = pan.augment_image(img)
    if np.random.rand() < 0.5:
        zoom = iaa.Affine(scale=(1, 1.2))
        img = zoom.augment_image(img)
    if np.random.rand() < 0.5:
        brightness = iaa.Multiply((0.5, 1.2))
        img = brightness.augment_image(img)
    if np.random.rand() < 0.5:
        img = cv2.flip(img, 1)
        steering = -steering
    return img, steering

imgRe, st = augment_image('collected_data/img0/Image_1621256928554.jpg',0)
# mpimg.imsave('Result.jpg',imgRe)
cv2.imshow('img', imgRe)


# 6 - PREPROCESS
def preprocess(img):
    img = img[174:, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img


# 7 - CREATE MODEL
def create_model():
    model = Sequential(
        [
            layers.Convolution2D(24, (5, 5), (2, 2), input_shape=(66, 200, 3), activation='elu'),
            layers.Convolution2D(36, (5, 5), (2, 2), activation='elu'),
            layers.Convolution2D(48, (5, 5), (2, 2), activation='elu'),
            layers.Convolution2D(64, (3, 3), activation='elu'),
            layers.Convolution2D(64, (3, 3), activation='elu'),
            
            layers.Flatten(),
            layers.Dense(100, activation='elu'),
            layers.Dense(50, activation='elu'),
            layers.Dense(10, activation='elu'),
            layers.Dense(1)
        ]
    ) 

    opt = Adam(learning_rate=0.0003)
    model.compile(loss='mse', optimizer=opt)
    return model

# 8 - TRAINING
def data_gen(images_path, steering_list, batch_size, train_flag):
    '''
    Generates a batch of images and its corresponding steering angle.
    
    If the train flag is set to true, this function will augment the images.
    '''
    while True:
        img_batch = []
        steering_batch = []

        for i in range(batch_size):
            index = random.randint(0, len(images_path) - 1)
            if train_flag:
                img, steering = augment_image(images_path[index], steering_list[index])
            else:
                img = cv2.imread(images_path[index])
                steering = steering_list[index]
            img = preprocess(img)
            img_batch.append(img)
            steering_batch.append(steering)
            yield (np.asarray(img_batch), np.asarray(steering_batch))