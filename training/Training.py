print("Setting Up...")
import os
import sys
base_dir = os.path.dirname(os.path.realpath(__file__)).split('/')[:-1]
base_dir = '/'.join(base_dir)
print(base_dir)
sys.path.insert(0, base_dir)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from sklearn.model_selection import train_test_split

from Utils import *
from TfLiteConverter import convert_to_tflite

# 1 - INITIALIZE DATA
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_collection/collected_data')
data = import_data_info(path)
print(data.head())

# 2 - VISUALIZE AND BALANCE DATA
data = balance_data(data, samples_per_bin=800, display=True)

# 3 - PREPARE DATA FOR PROCESSING
images_path, steering_angles = load_data(path, data)


# 4 - SPLIT DATA FOR TRAINING AND VALIDATION
x_train, x_val, y_train, y_val = train_test_split(images_path, steering_angles,
                                    test_size=0.2, random_state=42)

print('Total Training Images: ', len(x_train))
print('Total Validation Images: ', len(x_val))

# 5 - AUGMENT DATA

# 6 - PREPROCESS DATA

# 7 - CREATE MODEL
model = create_model()

# 8 - TRAINING
history = model.fit(data_gen(x_train, y_train, 100, 1),
                    steps_per_epoch=100,
                    epochs=10,
                    validation_data=data_gen(x_val, y_val, 50, 0),
                    validation_steps=50)

# 9 - SAVE THE MODEL
model.save(os.path.join(base_dir, 'model_v1.h5'))
convert_to_tflite(model)
print('Model saved')

# 10 - PLOT RESULTS
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()
