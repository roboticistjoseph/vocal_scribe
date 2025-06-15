#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: mediapipe_hand_module.py - Real-time Hand Detection and Tracking

This module provides a high-level interface for hand tracking using MediaPipe,
designed for air drawing applications.

Features:
    - Real-time hand detection and tracking (up to 2 hands)
    - 21 landmark detection per hand
    - Finger state detection (up/down)
    - Customizable detection/tracking confidence

Example:
    detector = HandDetector(max_hands=1, detection_con=0.7)
    img = detector.find_hands(frame)
    lmList = detector.find_position(img)
    fingers = detector.fingers_up()

Author: Joseph Katakam
Date: 2020-05-01
Dependencies: opencv-python>=4.5.0, mediapipe>=0.8.0
"""

# importing libraries
import cv2              # open-cv for Computer Vision
import mediapipe as mp  # mediapipe for hand tracking
import time             # time for calculating FPS

class HandDetector:
    """
    High-level wrapper for MediaPipe hand tracking with gesture recognition.

    This class simplifies hand detection and provides utility methods for
    extracting landmark positions and determining finger states, optimized
    for air drawing applications.

    Attributes:
        mode (bool): Static image mode (False for video stream)
        maxHands (int): Maximum number of hands to detect (1-2)
        detectionCon (float): Minimum detection confidence (0.0-1.0)
        trackCon (float): Minimum tracking confidence (0.0-1.0)
        tipIds (list): Landmark IDs for fingertips [thumb, index, middle, ring, pinky]

    Note:
        Best performance with hand 0.5-1.5 meters from camera
        May struggle with fast motion or unusual hand orientations
    """
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.detectionCon = detection_con
        self.trackCon = track_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=float(self.detectionCon),
            min_tracking_confidence=float(self.trackCon)
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]


    def find_hands(self, img, draw=True):
        """
        Function to find the hands.

        Args:
            img: Input frame to detect hands.
            draw: Boolean to draw connecting lines on detected landmarks.

        Returns:
            Image of detected hands.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        """
        Extract hand landmark positions in pixel coordinates.

        Args:
            img (np.ndarray): Input image (BGR format)
            hand_no (int): Hand index to track (0 or 1 for multi-hand)
            draw (bool): Whether to draw circles on landmarks

        Returns:
            list: List of [id, x, y] for each landmark, empty if no hand detected

        Raises:
            IndexError: If hand_no exceeds detected hands

        Example:
            lmList = detector.find_position(img, hand_no=0)
            if lmList:
                thumb_tip = lmList[4]  # [4, x, y]
        """
        self.lmList = []

        if not self.results or not self.results.multi_hand_landmarks:
            return self.lmList  # Return empty list if no hands

        if hand_no >= len(self.results.multi_hand_landmarks):
            print(f"Warning: Requested hand {hand_no} but only {len(self.results.multi_hand_landmarks)} detected")
            return self.lmList

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return self.lmList

    def fingers_up(self):
        """
        Function to detect fingers up

        Returns:
            A list of booleans representing whether fingers up
        """
        if not hasattr(self, 'lmList') or not self.lmList:
            return []

        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

def main():
    """
    Main Function

    Returns:
        Used to test the functionality of the module
    """
    p_time = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        if len(lm_list) != 0:
            print(lm_list[4])

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Hand Detection", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()