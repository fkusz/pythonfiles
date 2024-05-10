import tensorflow as tf
import numpy as np
import cv2 as opencv
import matplotlib.pyplot as plt
import os
from keras.utils import to_categorical
from keras import layers, models
from sklearn.model_selection import train_test_split

mnist = tf.keras.datasets.mnist
(train_digits, train_classification), (test_digits, test_classification) = mnist.load_data()

train_digits = train_digits.reshape((60000,28,28,1))
train_digits = train_digits.astype('float32')/255

test_digits = test_digits.reshape((10000,28,28,1))
test_digits = test_digits.astype('float32')/255

train_classification = to_categorical(train_classification)
test_classification = to_categorical(test_classification)

train_digits, val_digits, train_classification, val_classification = train_test_split(
    train_digits, train_classification, test_size=0.1, random_state=42)

try:
    model = tf.keras.models.load_model('Keras Models\handwrittenCNN2.keras')
    model.summary()
    print('Model Loaded Successfully!')

except:    
    model = models.Sequential()
    model.add(layers.Conv2D(32,(3,3),activation='relu', input_shape=(28,28,1)))
    model.add(layers.MaxPooling2D((2,2)))
    model.add(layers.Conv2D(64,(3,3),activation='relu'))
    model.add(layers.MaxPooling2D((2,2)))
    model.add(layers.Conv2D(64,(3,3),activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.10))
    model.add(layers.Dense(10, activation='softmax'))
    
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
    
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=5, restore_best_weights=True)
    
    model.fit(train_digits, train_classification, epochs=100, batch_size=32, validation_data=(val_digits, val_classification), callbacks=[early_stopping])
    
    model.save('Keras Models\handwrittenCNN2.keras')

finally:
    loss, accuracy = model.evaluate(test_digits, test_classification)
    image_number = 1
    correct = 0
    classification=[6,4,1,5,3,7,9,2,1,9,5,3,1,8,3,1,8,9,3,4,0,9,1,2,1,0,4,7,8,9,2,3]
    if os.path.isfile(f'Digits/digit{image_number}.png'):
        while os.path.isfile(f'Digits/digit{image_number}.png'):
            try:
                img = opencv.imread(f'Digits/digit{image_number}.png')[:,:,0]
                img = np.invert(np.array([img]))
                prediction = model.predict(img, verbose = 0)
                if np.argmax(prediction) != classification[image_number-1]:
                    print(f'Model incorrectly classified this image as a {np.argmax(prediction)}')
                    plt.imshow(img[0],cmap=plt.cm.binary)
                    plt.show()
                else:
                    correct +=1
            except:
                print("Error!")
            finally:
                image_number += 1
        print(f"Accuracy: {correct/len(classification)}")
    else:
        print("Test images not found at filepath")