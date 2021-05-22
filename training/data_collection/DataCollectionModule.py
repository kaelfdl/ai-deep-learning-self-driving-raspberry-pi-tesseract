import os
import pandas as pd
import cv2
from datetime import datetime

global img_list, steering_list
folder_count = 0
count = 0
img_list = []
steering_list = []
make_folder = False

# Get Current Directory Path
current_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'collected_data')
print(current_dir)

# Create a new folder based on the previous folder count
while os.path.exists(os.path.join(current_dir, f'img{str(folder_count)}')):

    # If there is an no unused folder, make a new folder 
    if len(os.listdir(os.path.join(current_dir, f'img{str(folder_count)}'))) != 0:
        make_folder = True
        folder_count += 1
    else:
        make_folder = False
        break

new_path = current_dir + '/img' + str(folder_count)

if not make_folder:
    os.makedirs(new_path)

# Save images to a folder
def save_data(img, steering):
    global img_list, steering_list
    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).replace('.', '')
    filename = os.path.join(new_path, f'Image_{timestamp}.jpg')
    cv2.imwrite(filename, img)
    img_list.append(filename)
    steering_list.append(steering)

# Save the log file when the session ends
def save_log():
    global img_list, steering_list
    raw_data = {'Image': img_list, 'Steering': steering_list}
    df = pd.DataFrame(raw_data)
    new_path = os.path.join(current_dir, f'log_{str(folder_count)}.csv')
    df.to_csv(new_path, index=False, header=False)
    print('Log saved')
    print('Total Images: ', len(img_list))

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    for x in range(10):
        _, img = cv2.read()
        save_data(img, 0.2)
        cv2.waitKey(1)
        cv2.imshow('Img', img)
    save_log()
