import tflite_runtime.interpreter as tflite

class Interpreter():

    # Load the TFLite model
    def __init__(self, model_path):
        self.interpreter = tflite.Interpreter(model_path=model_path)


    def interpret(self, img):
        # Allocate tensors.
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # Run the model with the input data.
        input_data = img 
        self.interpreter.set_tensor(input_details[0]['index'], input_data)

        self.interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        return output_data
