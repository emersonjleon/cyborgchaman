import numpy as np
from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random

number_of_epochs = int(input("How many epochs to train each model for? "))

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

def calculate_accuracy(model, X_test, y_test):
    output = model.forward(X_test)
    predicted_labels = np.argmax(output, axis=1)
    correct_predictions = np.sum(predicted_labels == y_test)
    accuracy = (correct_predictions / len(y_test))
    return accuracy

def display_random_predictions_with_images(models, X_test, y_test, sample_count=4):
    sample_indices = random.sample(range(X_test.shape[0]), sample_count)
    samples = X_test.iloc[sample_indices]
    true_labels = y_test.iloc[sample_indices]

    print("\nRandom Predictions:")
    for i, model in enumerate(models, start=1):
        predictions = model.forward(samples.values)
        predicted_labels = np.argmax(predictions, axis=1)
        print(f"\nModel {i}:")

        fig, axes = plt.subplots(1, sample_count, figsize=(10, 3))
        fig.suptitle(f"Predictions from Model {i}", fontsize=14)
        
        for idx, (sample, true_label, pred_label, ax) in enumerate(zip(samples.values, true_labels, predicted_labels, axes)):
            img = sample.reshape(28, 28)
            ax.imshow(img, cmap="gray")
            ax.axis("off")
            ax.set_title(f"True: {true_label}\nPred: {pred_label}")

        plt.tight_layout()
        plt.show()


class NN_with_one_hidden_layer:
    def __init__(self, input_size, output_size, hidden_size, lr, activation):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.learning_rate = lr
        self.activation = activation

        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2 / self.input_size)
        self.bias_hidden = np.zeros((1, self.hidden_size))
        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2 / self.hidden_size)
        self.bias_output = np.zeros((1, self.output_size))

        mnist = fetch_openml('mnist_784', version=1)
        X, y = mnist["data"], mnist["target"]

        y = y.astype(np.uint8)

        X = X[:10000] / 255
        y = y[:10000]

        indices = np.random.permutation(X.shape[0])

        test_size = int(0.2 * X.shape[0])
        X_train = X.iloc[indices[:-test_size]]
        X_test = X.iloc[indices[-test_size:]]
        y_train = y.iloc[indices[:-test_size]]
        y_test = y.iloc[indices[-test_size:]]
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
    
    def get_mode_sets(self, mode):
        if mode == 'train':
            return self.X_train, self.y_train
        elif mode == 'test':
            return self.X_test, self.y_test
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        
    def forward(self, X):
        self.linear_transformation_1 = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        if self.activation == "relu":
            self.activation_hidden_layer = relu(self.linear_transformation_1)
        elif self.activation == "sigmoid":
            self.activation_hidden_layer = sigmoid(self.linear_transformation_1)
        self.linear_transformation_2 = np.dot(self.activation_hidden_layer, self.weights_hidden_output) + self.bias_output
        return self.linear_transformation_2
    
    def backward(self, X, y, output):
        one_hot_encoded = np.zeros((len(y), 10))
        one_hot_encoded[np.arange(len(y)), y] = 1
        output_error = output - one_hot_encoded
        output_delta = output_error / len(y)
        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        if self.activation == "relu":
            hidden_delta = hidden_error * relu_derivative(self.linear_transformation_1)
        elif self.activation == "sigmoid":
            hidden_delta = hidden_error * sigmoid_derivative(self.linear_transformation_1)

        self.weights_hidden_output -= self.activation_hidden_layer.T.dot(output_delta) * self.learning_rate
        self.bias_output -= np.sum(output_delta, axis=0) * self.learning_rate
        self.weights_input_hidden -= X.T.dot(hidden_delta) * self.learning_rate
        self.bias_hidden -= np.sum(hidden_delta, axis=0) * self.learning_rate
    
    def train(self, X, y, epochs):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)

class NN_with_two_hidden_layers:
    def __init__(self, input_size, output_size, hidden_size, lr, activation):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.learning_rate = lr
        self.activation = activation

        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2 / self.input_size)
        self.bias_hidden = np.zeros((1, self.hidden_size))
        self.weights_hidden_hidden = np.random.randn(self.hidden_size, self.hidden_size) * np.sqrt(2 / self.hidden_size)
        self.bias_hidden2 = np.zeros((1, self.hidden_size))
        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2 / self.hidden_size)
        self.bias_output = np.zeros((1, self.output_size))

        mnist = fetch_openml('mnist_784', version=1)
        X, y = mnist["data"], mnist["target"]

        y = y.astype(np.uint8)

        X = X[:10000] / 255
        y = y[:10000]

        indices = np.random.permutation(X.shape[0])

        test_size = int(0.2 * X.shape[0])
        X_train = X.iloc[indices[:-test_size]]
        X_test = X.iloc[indices[-test_size:]]
        y_train = y.iloc[indices[:-test_size]]
        y_test = y.iloc[indices[-test_size:]]
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
    
    def get_mode_sets(self, mode):
        if mode == 'train':
            return self.X_train, self.y_train
        elif mode == 'test':
            return self.X_test, self.y_test
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        
    def forward(self, X):
        self.linear_transformation_1 = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        if self.activation == "relu":
            self.activation_hidden_layer = relu(self.linear_transformation_1)
        elif self.activation == "sigmoid":
            self.activation_hidden_layer = sigmoid(self.linear_transformation_1)
        self.linear_transformation_2 = np.dot(self.activation_hidden_layer, self.weights_hidden_hidden) + self.bias_hidden2
        if self.activation == "relu":
            self.activation_hidden_layer2 = relu(self.linear_transformation_2)
        elif self.activation == "sigmoid":
            self.activation_hidden_layer2 = sigmoid(self.linear_transformation_2)
        self.linear_transformation_3 = np.dot(self.activation_hidden_layer2, self.weights_hidden_output) + self.bias_output
        return self.linear_transformation_3
    
    def backward(self, X, y, output):
        one_hot_encoded = np.zeros((len(y), 10))
        one_hot_encoded[np.arange(len(y)), y] = 1
        output_error = output - one_hot_encoded
        output_delta = output_error / len(y)
        hidden_error2 = output_delta.dot(self.weights_hidden_output.T)
        if self.activation == "relu":
            hidden_delta2 = hidden_error2 * relu_derivative(self.linear_transformation_2)
        elif self.activation == "sigmoid":
            hidden_delta2 = hidden_error2 * sigmoid_derivative(self.linear_transformation_2)
        hidden_error1 = hidden_delta2.dot(self.weights_hidden_hidden.T)
        if self.activation == "relu":
            hidden_delta1 = hidden_error1 * relu_derivative(self.linear_transformation_1)
        elif self.activation == "sigmoid":
            hidden_delta1 = hidden_error1 * sigmoid_derivative(self.linear_transformation_1)

        self.weights_hidden_output -= self.activation_hidden_layer2.T.dot(output_delta) * self.learning_rate
        self.bias_output -= np.sum(output_delta, axis=0) * self.learning_rate
        self.weights_hidden_hidden -= self.activation_hidden_layer.T.dot(hidden_delta2) * self.learning_rate
        self.bias_hidden2 -= np.sum(hidden_delta2, axis=0) * self.learning_rate
        self.weights_input_hidden -= X.T.dot(hidden_delta1) * self.learning_rate
        self.bias_hidden -= np.sum(hidden_delta1, axis=0) * self.learning_rate
    
    def train(self, X, y, epochs):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)

class DrawingApp:
    def __init__(self):
        self.grid_size = 28
        self.canvas = np.zeros((self.grid_size, self.grid_size))
        self.fig, self.ax = plt.subplots()
        self.img = self.ax.imshow(self.canvas, cmap="gray", vmin=0, vmax=1)
        self.pressed = False

        self.fig.canvas.mpl_connect("button_press_event", self.on_press)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

        button_width = 0.2
        button_height = 0.075

        self.clear_button_ax = self.fig.add_axes([0.1, 0.05, button_width, button_height])
        self.clear_button = Button(self.clear_button_ax, "Clear")
        self.clear_button.on_clicked(self.clear_canvas)

        self.submit_button_ax = self.fig.add_axes([0.7, 0.05, button_width, button_height])
        self.submit_button = Button(self.submit_button_ax, "Submit")
        self.submit_button.on_clicked(self.submit_canvas)

        plt.axis("off")
        plt.show()

    def on_press(self, event):
        self.pressed = True
        self.draw(event)

    def on_release(self, event):
        self.pressed = False

    def on_motion(self, event):
        if self.pressed:
            self.draw(event)

    def draw(self, event):
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.canvas[y, x] = 1
                self.img.set_data(self.canvas)
                self.fig.canvas.draw()

    def clear_canvas(self, event):
        self.canvas = np.zeros((self.grid_size, self.grid_size))
        self.img.set_data(self.canvas)
        self.fig.canvas.draw()

    def submit_canvas(self, event):
        plt.close(self.fig)
        self.process_image(self.canvas)

    def process_image(self, image):
        flat_image = image.flatten().reshape(1, -1)
        models = [NN_one_layer_relu, NN_two_layer_relu, NN_one_layer_sigmoid, NN_two_layer_sigmoid]

        print("\nClassification Results:")
        for i, model in enumerate(models, start=1):
            prediction = model.forward(flat_image)
            predicted_label = np.argmax(prediction, axis=1)[0]
            print(f"Model {i} Prediction: {predicted_label}")



NN_one_layer_sigmoid = NN_with_one_hidden_layer(input_size = 784, output_size = 10, hidden_size = 64, lr = 0.05, activation = "sigmoid")
X_train, y_train = NN_one_layer_sigmoid.get_mode_sets('train')    
X_test, y_test = NN_one_layer_sigmoid.get_mode_sets('test')
NN_one_layer_sigmoid.train(X_train, y_train, number_of_epochs)

NN_two_layer_sigmoid = NN_with_two_hidden_layers(input_size = 784, output_size = 10, hidden_size = 16, lr = 0.1, activation = "sigmoid")
X_train, y_train = NN_two_layer_sigmoid.get_mode_sets('train')    
X_test, y_test = NN_two_layer_sigmoid.get_mode_sets('test')
NN_two_layer_sigmoid.train(X_train, y_train, number_of_epochs)

NN_one_layer_relu = NN_with_one_hidden_layer(input_size = 784, output_size = 10, hidden_size = 64, lr = 0.05, activation = "relu")
X_train, y_train = NN_one_layer_relu.get_mode_sets('train')    
X_test, y_test = NN_one_layer_relu.get_mode_sets('test')
NN_one_layer_relu.train(X_train, y_train, number_of_epochs)

NN_two_layer_relu = NN_with_two_hidden_layers(input_size = 784, output_size = 10, hidden_size = 16, lr = 0.1, activation = "relu")
X_train, y_train = NN_two_layer_relu.get_mode_sets('train')    
X_test, y_test = NN_two_layer_relu.get_mode_sets('test')
NN_two_layer_relu.train(X_train, y_train, number_of_epochs)

accuracy_one_layer_relu = calculate_accuracy(NN_one_layer_relu, X_test, y_test)
accuracy_two_layer_relu = calculate_accuracy(NN_two_layer_relu, X_test, y_test)
accuracy_one_layer_sigmoid = calculate_accuracy(NN_one_layer_sigmoid, X_test, y_test)
accuracy_two_layer_sigmoid = calculate_accuracy(NN_two_layer_sigmoid, X_test, y_test)

print(f"Accuracy of NN with one hidden layer (ReLU)(Model 1): {accuracy_one_layer_relu * 100:.2f}%")
print(f"Accuracy of NN with two hidden layers (ReLU)(Model 2): {accuracy_two_layer_relu * 100:.2f}%")
print(f"Accuracy of NN with one hidden layer (Sigmoid)(Model 3): {accuracy_one_layer_sigmoid * 100:.2f}%")
print(f"Accuracy of NN with two hidden layers (Sigmoid)(Model 4): {accuracy_two_layer_sigmoid * 100:.2f}%")

models = [NN_one_layer_relu, NN_two_layer_relu, NN_one_layer_sigmoid, NN_two_layer_sigmoid]

display_random_predictions_with_images(models, X_test, y_test)

if __name__ == "__main__":
    app = DrawingApp()
