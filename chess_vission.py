import glob
import os
import numpy as np
from PIL import Image
import chess
from tensorflow.keras.models import load_model
from matplotlib import pyplot as plt
import cv2

def detect_fen(images):
    label_list = ['E', 'N', 'p', 'B', 'b', 'Q', 'R', 'P', 'q', 'n', 'k', 'K', 'r']
    model = load_model('model.h5')

    # preprocess image
    np_images = np.array(images)

    # resize image
    np_images = np_images.reshape(-1, 50, 50, 3)

    # normalize image
    np_images = np_images / 255.0

    # predict
    pred = model.predict(np_images, verbose=None)
    pred = np.argmax(pred, axis=1)

    # show image 8 x 8
    fig = plt.figure(figsize=(8, 8))

    FEN = ""

    for i in range(8):
        E_count = 0
        for j in range(8):
            ax = fig.add_subplot(8, 8, 8*i+j+1)
            ax.imshow(images[8*i+j])
            ax.axis('off')
            ax.set_title(label_list[pred[8*i+j]])

            if label_list[pred[8*i+j]] == 'E':
                E_count += 1
            else:
                if E_count != 0:
                    FEN += str(E_count)
                    E_count = 0
                FEN += label_list[pred[8*i+j]]

        if E_count != 0:
            FEN += str(E_count)
            E_count = 0

        FEN += '/' if i != 7 else ''

    return FEN


if __name__ == "__main__":
    for file in glob.glob('boards/board_*.png'):
        # read image
        image_list = []
        img = cv2.imread(file)

        # split image to 8x8
        for i in range(8):
            for j in range(8):
                x = 50 * j
                y = 50 * i
                image_list.append(img[y:y+50, x:x+50])

        # detect piece
        detected_FEN = detect_fen(image_list)

        # compare
        print("Detected FEN: ", detected_FEN)
