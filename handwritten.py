import tensorflow as tf
import numpy as np
import cv2 as opencv
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split

def test_model(model):
    image_number = 1
    correct = 0
    classification=[6,4,1,5,3,7,9,2,1,9,5,3,1,8,3,1,8,9,3,4,0,9,1,2,1,0,4,7,8,9,2,3]
    while os.path.isfile(f'Digits/digit{image_number}.png'):
        try:
            img = opencv.imread(f'Digits/digit{image_number}.png')[:,:,0]
            img = np.invert(np.array([img]))
            prediction = model.predict(img, verbose = 0)
            if np.argmax(prediction) != classification[image_number-1]:
                print(f'Model incorrectly classified {classification[image_number-1]} as {np.argmax(prediction)}')
                plt.imshow(img[0],cmap=plt.cm.binary)
                plt.show()
            else:
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

train_digits, val_digits, train_classification, val_classification = train_test_split(
    train_digits, train_classification, test_size=0.1, random_state=42)

try:
    model = tf.keras.models.load_model('Keras Models\handwritten-Dropout_0.1_Increasing_16_64_256.keras')
    #model = tf.keras.models.load_model('Keras Models\handwritten.keras')
    print('Model Loaded Successfully!')
    
    loss, accuracy = model.evaluate(test_digits, test_classification)
    
except:
    
    model = tf.keras.models.Sequential()
    
    model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
    
    model.add(tf.keras.layers.Dense(64,activation='relu', kernel_regularizer=tf.keras.regularizers.L1L2(l1=0.001, l2=0.001)))
    model.add(tf.keras.layers.Dropout(0.15))
    
    model.add(tf.keras.layers.Dense(10,activation='softmax'))
    model.summary()
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=5, restore_best_weights=True)

    # Train the model with validation data, early stopping, and print callback
    model.fit(train_digits, train_classification, epochs=100, batch_size=32, validation_data=(val_digits, val_classification), callbacks=[early_stopping])
    
    model.save('Keras Models\handwritten.keras')

finally:
    print(f"Accuracy: {test_model(model)}")
