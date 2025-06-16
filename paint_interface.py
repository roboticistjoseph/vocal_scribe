#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Air Drawing Paint Interface - Real-time Gesture-Based Drawing Application

This module implements a computer vision-based paint interface that allows users to draw
in the air using hand gestures. The application uses MediaPipe for hand tracking and
provides multiple modes including drawing, erasing, text recognition, and translation.

Features:
    - Real-time hand tracking with 21 landmark detection
    - State-based mode switching (Drawing, Eraser, Save, Translation, Finger Counter)
    - Air drawing with customizable brush settings
    - OCR for text recognition from drawings
    - Multi-language text-to-speech conversion
    - Finger counting demonstration mode

Requirements:
    - Python 3.7+
    - OpenCV (cv2) >= 4.5.0
    - NumPy >= 1.19.0
    - MediaPipe >= 0.8.0
    - Custom modules: mediapipe_hand_module, ocr_module, tts_module

Usage:
    python paint_interface.py

Deployment Notes:
    - Requires webcam access (index 0 by default)
    - Interface images must be in ./interface/ directory
    - Optimal performance with 1280x720 resolution
    - Best results with good lighting and plain background

Author: Joseph Katakam
Email: jkatak73@terpmail.umd.edu
License: MIT
Version: 1.0.0
Copyright: 2020, JK
"""

# Standard library imports
import os
import threading
from enum import Enum

# Third-party imports
import cv2
import numpy as np

# Custom module imports
import mediapipe_hand_module as htm
import ocr_module
import tts_module

# *** Paint Interface ***
# brush parameters
BRUSH_THICKNESS = 25
ERASER_THICKNESS = 100
BRUSH_COLOR = (255, 0, 255)
# Buttons
folderPath = "interface"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(myList)
print(len(overlayList))
header = overlayList[0]

# *** Initialize Camera/Canvas ***
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

# *** Initialize Hand Detection Module ***
detector = htm.HandDetector(detection_con=0.65, max_hands=1)
tipIds = [4, 8, 12, 16, 20]
xp, yp = 0, 0

# *** Initialize Optical Character Recognition Module ***
ocr = ocr_module.OCR()

# *** Initialize Text-to-Speech Module ***
tts = tts_module.TTS()

# *** Other Parameters ***
language_translate = False
imgInv = cv2.cvtColor(overlayList[0], cv2.COLOR_BGR2GRAY)

# State Machine
from enum import Enum

class PaintMode(Enum):
    """
    Each mode represents a different functionality:
        IDLE: No active mode, waiting for user selection
        DRAWING: Draw on canvas with index finger
        ERASER: Erase canvas content with index finger
        SAVE_CANVAS: Save current canvas to file
        TRANSLATE_EN: Recognize text and translate to English
        TRANSLATE_FR: Recognize text and translate to French
        FINGER_COUNTER: Count and display number of raised fingers
    """
    IDLE = "idle"
    DRAWING = "drawing"
    ERASER = "eraser"
    SAVE_CANVAS = "save_canvas"
    TRANSLATE_EN = "translate_english"
    TRANSLATE_FR = "translate_french"
    FINGER_COUNTER = "finger_counter"


# initialize state variables
current_mode = PaintMode.IDLE
mode_selected = False
mode_change_cooldown = 0  # Prevent rapid mode switching

# Saving Video
fps = cap.get(cv2.CAP_PROP_FPS)
codec = cv2.VideoWriter_fourcc(*'mp4v')  # H.264 or H.265 codec for .MP4
output1 = cv2.VideoWriter("canvas.mp4", codec, fps, (1280, 720))
output2 = cv2.VideoWriter("inverse_canvas.mp4", codec, fps, (1280, 720))

while True:
    # read frames
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # find Hand Landmarks
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)

    # state based approach
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Only check for mode changes in header area
        if y1 < 137 and mode_change_cooldown == 0:
            new_mode = None

            if 5 < x1 < 190:
                new_mode = PaintMode.DRAWING
                header = overlayList[1]
            elif 200 < x1 < 390:
                new_mode = PaintMode.ERASER
                header = overlayList[2]
            elif 400 < x1 < 590:
                new_mode = PaintMode.SAVE_CANVAS
                header = overlayList[3]
            elif 600 < x1 < 790:
                new_mode = PaintMode.TRANSLATE_EN
                header = overlayList[4]
            elif 800 < x1 < 990:
                new_mode = PaintMode.TRANSLATE_FR
                header = overlayList[5]
            elif 1000 < x1 < 1270:
                new_mode = PaintMode.FINGER_COUNTER
                header = overlayList[6]

            # Only change mode if we detected a new one
            if new_mode and new_mode != current_mode:
                current_mode = new_mode
                mode_selected = True
                mode_change_cooldown = 30  # frames to wait
                print(f"[MODE CHANGE] → {current_mode.value}")

        # Cooldown countdown
        if mode_change_cooldown > 0:
            mode_change_cooldown -= 1

        # Execute current mode logic
        if mode_selected:
            # check which fingers are up
            fingers = detector.fingers_up()
            # print(fingers)
            if current_mode == PaintMode.DRAWING:
                # Setting brush color
                BRUSH_COLOR = (255, 0, 255)

                # If Drawing Mode - Index finger is up
                if fingers[1] and fingers[2] == False:
                    cv2.circle(img, (x1, y1), 15, BRUSH_COLOR, cv2.FILLED)
                    print("Drawing Mode")
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    cv2.line(img, (xp, yp), (x1, y1), BRUSH_COLOR, BRUSH_THICKNESS)

                    if BRUSH_COLOR == (0, 0, 0):
                        cv2.line(img, (xp, yp), (x1, y1), BRUSH_COLOR, ERASER_THICKNESS)
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), BRUSH_COLOR, ERASER_THICKNESS)

                    else:
                        cv2.line(img, (xp, yp), (x1, y1), BRUSH_COLOR, BRUSH_THICKNESS)
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), BRUSH_COLOR, BRUSH_THICKNESS)

                xp, yp = x1, y1

            elif current_mode == PaintMode.ERASER:
                # Setting eraser color
                BRUSH_COLOR = (0, 0, 0)
                if fingers[1] and fingers[2] == False:
                    cv2.circle(img, (x1, y1), 15, BRUSH_COLOR, cv2.FILLED)
                    cv2.line(img, (xp, yp), (x1, y1), BRUSH_COLOR, ERASER_THICKNESS)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), BRUSH_COLOR, ERASER_THICKNESS)
                xp, yp = x1, y1

                # Clear Canvas when all fingers are up
                if all(x >= 1 for x in fingers):
                    imgCanvas = np.zeros((720, 1280, 3), np.uint8)

            elif current_mode == PaintMode.SAVE_CANVAS:
                cv2.imwrite("portfolio_canvas.jpg", imgInv)
                current_mode = PaintMode.IDLE
            elif current_mode == PaintMode.TRANSLATE_EN:
                language_translate = False
                ocr_img = cv2.imread('portfolio_canvas.jpg')
                prompt = ocr.extract_text(ocr_img)
                print(prompt)
                threading.Thread(target=tts.text_to_speech, args=(prompt,), kwargs={'translate': False},
                                 daemon=True).start()
                # tts.text_to_speech(prompt=word, translate=False)
                current_mode = PaintMode.IDLE
            elif current_mode == PaintMode.TRANSLATE_FR:
                language_translate = True
                ocr_img = cv2.imread('portfolio_canvas.jpg')
                prompt = ocr.extract_text(ocr_img)
                print(prompt)
                threading.Thread(target=tts.text_to_speech, args=(prompt,), kwargs={'translate': True},
                                 daemon=True).start()
                # tts.text_to_speech(prompt=word, translate=True)
                current_mode = PaintMode.IDLE
            elif current_mode == PaintMode.FINGER_COUNTER:
                header = overlayList[6]
                finger_count = []

                # Thumb
                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                    finger_count.append(1)
                else:
                    finger_count.append(0)

                # 4 Fingers
                for id in range(1, 5):
                    # Tip ABOVE knuckle (smaller y value)
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:  # CORRECT!
                        finger_count.append(1)
                    else:
                        finger_count.append(0)

                totalFingers = finger_count.count(1)
                if totalFingers == 1:
                    header = overlayList[7]
                if totalFingers == 2:
                    header = overlayList[8]
                if totalFingers == 3:
                    header = overlayList[9]
                if totalFingers == 4:
                    header = overlayList[10]
                if totalFingers == 5:
                    header = overlayList[11]
                # Visual feedback
                # cv2.putText(img, f"Fingers: {totalFingers}", (50, 450),
                #             cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # ========== IMAGE COMPOSITION ==========
    # Create inverse mask for blending
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    # Blend camera feed with canvas
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Add/Update header overlay
    img[0:137, 0:1280] = header
    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

    # ========== DISPLAY & EXIT ==========
    cv2.imshow("Air Drawing - Paint to Talk", img)

    # cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inv", imgInv)

    # Saving: Write the frame to the output video
    # output1.write(imgCanvas)
    # output1.write(imgInv)

    # Check for exit key
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # 'q' or ESC
        print("\nExiting application...")
        break
    # Additional hotkeys
    elif key == ord('c'):  # Clear canvas
        imgCanvas = np.zeros((720, 1280, 3), np.uint8)
        print("Canvas cleared")
    elif key == ord('s'):  # Quick save
        filename = f"quicksave_{cv2.getTickCount()}.png"
        cv2.imwrite(filename, imgCanvas)
        print(f"Quick save: {filename}")

# Clean up
cap.release()
# output1.release()
# output2.release()
cv2.destroyAllWindows()
