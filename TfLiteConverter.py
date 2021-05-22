import tensorflow as tf

def convert_to_tflite(model):
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tfmodel = converter.convert()
    open ("model_v1.tflite" , "wb") .write(tfmodel)


if __name__ == '__main__':
    model = tf.keras.models.load_model('model_v1.h5')
    convert_to_tflite(model)