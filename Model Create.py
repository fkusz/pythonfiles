import tensorflow as tf
import numpy as np
import cv2 as opencv
import matplotlib.pyplot as plt
import os
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

def test_model(model):
    image_number = 1
    correct = 0
    classification=[6,4,1,5,3,7,9,2,1,9,5,3,1,8,3,1,8,9,3,4,0,9,1,2,1,0,4,7,8,9,2,3]
    while os.path.isfile(f'Digits/digit{image_number}.png'):
        try:
            img = opencv.imread(f'Digits/digit{image_number}.png')[:,:,0]
            img = np.invert(np.array([img]))
            prediction = model.predict(img, verbose=0)
            if np.argmax(prediction) == classification[image_number-1]:
                correct +=1
        except:
            print("Error!")
        finally:
            image_number += 1
    return correct/len(classification)

mnist = tf.keras.datasets.mnist
(train_digits, train_classification), (test_digits, test_classification) = mnist.load_data()

train_digits = tf.keras.utils.normalize(train_digits , axis=1)
test_digits = tf.keras.utils.normalize(test_digits , axis=1)


# results = []
# for i in range(4):
#     for j in range(4):
#         for k in range(6):
#             try:
#                 model = tf.keras.models.load_model(f"Keras Models\Layers-{i+1}_Width-{2**(4+j)}_Epochs-{k+1}.keras")
#                 print('Model Loaded Successfully!')
#             except:
#                 model = tf.keras.models.Sequential()
#                 model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
#                 for _ in range(i+1):
#                     model.add(tf.keras.layers.Dense(2**(4+j),activation='relu'))       
#                 model.add(tf.keras.layers.Dense(10,activation='softmax'))
#                 model.summary()
#                 model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#                 model.fit(train_digits, train_classification, epochs=k+1)
#                 model_name = f"Keras Models\Layers-{i+1}_Width-{2**(4+j)}_Epochs-{k+1}.keras" 
#                 print(model_name)
#                 model.save(model_name)
#             finally:
#                 loss, accuracy = model.evaluate(test_digits, test_classification)
#                 results.append([accuracy,loss])

# print(results)

layers_range = range(1, 5)
width_range = range(4, 8)
epochs_range = range(1, 7)

results = np.zeros((len(layers_range), len(width_range), len(epochs_range)))

for i, layers in enumerate(layers_range):
    for j, width_power in enumerate(width_range):
        for k, epochs in enumerate(epochs_range):
            width = 2 ** width_power
            model_name = f"Keras Models\Layers-{layers}_Width-{width}_Epochs-{epochs}.keras"
            try:
                model = tf.keras.models.load_model(model_name)
                print(f'Model Loaded Successfully: {model_name}')
                #loss, accuracy = model.evaluate(test_digits, test_classification)
                accuracy = test_model(model)
                results[i, j, k] = accuracy
            except:
                print(f'Model not found: {model_name}')
                results[i, j, k] = np.nan

# Create a heatmap for each number of layers
for i, layers in enumerate(layers_range):
    plt.figure(figsize=(8, 6))
    sns.heatmap(results[i], annot=True, cmap='viridis', xticklabels=epochs_range, yticklabels=[2**w for w in width_range], mask=np.isnan(results[i]))
    plt.xlabel('Epochs')
    plt.ylabel('Width')
    plt.title(f'Accuracy Heatmap (Layers={layers})')
    plt.show()
    