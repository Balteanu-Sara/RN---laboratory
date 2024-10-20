import numpy as np
from torchvision.datasets import MNIST

def download_mnist(is_train: bool):
    dataset = MNIST(root='./data', transform=lambda x: np.array(x).flatten(),
                download=True,
                train=is_train)

    mnist_data = []
    mnist_labels = []
    for image, label in dataset:
        mnist_data.append(image)
        mnist_labels.append(label)

    return mnist_data, mnist_labels

train_X, train_Y = download_mnist(True)
test_X, test_Y = download_mnist(False)


def normalize(data):
    data = np.array(data)
    return data / 255.0

def encode(labels, num_classes=10):
    one_hot_labels = np.zeros((len(labels), num_classes))
    for i, label in enumerate(labels):
        one_hot_labels[i][label] = 1
    return one_hot_labels

train_X=normalize(train_X)
test_X=normalize(test_X)

train_Y_encoded = encode(train_Y)
test_Y_encoded = encode(test_Y)


def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

def cross_entropy(preds, labels):
    return -np.mean(np.sum(labels * np.log(preds + 1e-8), axis=1))

def backpropagation(X,Y, preds):
    dim=X.shape[0]
    error = Y - preds
    dW = np.dot(X.T, error) / dim
    db = np.sum(error, axis=0) / dim

    return dW,db

def train(epochs, weights, bias, learning_rate, batch_size):

    for epoch in range(epochs):
        print(f"Epoch {epoch+1}/{epochs}")

        for i in range(0, train_X.shape[0],batch_size):
            batch_X=train_X[i: i+batch_size]
            batch_Y=train_Y_encoded[i: i+batch_size]

            z=np.dot(batch_X, weights) + bias
            predictions=softmax(z)
            loss=cross_entropy(predictions,batch_Y)

            dw,db=backpropagation(batch_X, batch_Y, predictions)

            weights=weights+ learning_rate* dw
            bias=bias+learning_rate*db

        print(f"Loss at epoch {epoch+1}: {loss}")

    test(weights, bias)

def test(weights, bias) :
    z=np.dot(test_X, weights)+bias
    preds=softmax(z)
    test_preds=np.argmax(preds, axis=1)
    accuracy=np.mean(test_preds == test_Y)
    print(f"Accuracy: {accuracy * 100:.2f}%")


weights=np.random.randn(784, 10) * 0.01
bias=np.zeros((10,))
epochs= 50
learning_rate=0.01

train(500, weights, bias, learning_rate, 100)