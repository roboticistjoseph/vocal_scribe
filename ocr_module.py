#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: ocr_module.py
Author: Joseph Katakam
Date: 2020-05-01
Description: A module for performing Optical Character Recognition (OCR)
             using Tesseract and OpenCV, with functions to extract text,
             detect characters, words, or digits in images.
"""

# importing libraries
import cv2
import pytesseract
import os

class OCR:
    def __init__(self):
        """
        Initialize OCR engine by pointing to Tesseract executable.
        """
        self.tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

    def extract_text(self, img):
        """
        Extract readable text from an input image using OCR.
        Applies preprocessing for better OCR accuracy.
        Args:
            img (np.ndarray): Input image in BGR format (from OpenCV)
        Returns:
            str: Recognized text from the image
        """
        # Resize image
        img = cv2.resize(img, (640, 480))

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Denoise the image using median blur
        denoised = cv2.medianBlur(thresh, 3)

        # Optional: convert to RGB if needed
        rgb = cv2.cvtColor(denoised, cv2.COLOR_GRAY2RGB)

        # Perform OCR
        text = pytesseract.image_to_string(rgb)
        # print("[OCR Output]: \n", text)
        return text

    def display_detected_characters(self, img):
        """
        Draw bounding boxes around each detected character in the image.
        Args:
            img (np.ndarray): Input image
        """
        hImg, wImg, _ = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes = pytesseract.image_to_boxes(img_rgb)

        for b in boxes.splitlines():
            b = b.split(' ')
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(img_rgb, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
            cv2.putText(img_rgb, b[0], (x, hImg - y + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)

        cv2.imshow('Detected Characters', img_rgb)
        cv2.waitKey(0)

    def detect_only_words(self, img, visualize=False):
        """
        Detects and returns full words from the image.
        Optionally displays them with bounding boxes.

        Args:
            img (np.ndarray): Input image
            visualize (bool): Whether to display image with word boxes

        Returns:
            List[str]: List of detected words
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes = pytesseract.image_to_data(img_rgb)

        detected_words = []

        for i, b in enumerate(boxes.splitlines()):
            if i == 0:
                continue  # skip header
            b = b.split()
            if len(b) == 12:
                word = b[11]
                detected_words.append(word)

                if visualize:
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (50, 50, 255), 2)
                    cv2.putText(img_rgb, word, (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)

        if visualize:
            cv2.imshow('Detected Words', img_rgb)
            cv2.waitKey(0)

        # print(detected_words)
        return detected_words

    def detect_only_digits(self, img, visualize=False):
        """
        Detects and returns only numeric digits in the image.
        Optionally displays bounding boxes around them.

        Args:
            img (np.ndarray): Input image
            visualize (bool): Whether to display detected digits with OpenCV

        Returns:
            List[str]: List of detected digits
        """
        hImg, _, _ = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        config = r'--oem 3 --psm 6 outputbase digits'
        boxes = pytesseract.image_to_boxes(img_rgb, config=config)

        detected_digits = []

        for b in boxes.splitlines():
            b = b.split(' ')
            char = b[0]
            detected_digits.append(char)

            if visualize:
                x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                cv2.rectangle(img_rgb, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
                cv2.putText(img_rgb, char, (x, hImg - y + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)

        if visualize:
            cv2.imshow('Detected Digits', img_rgb)
            cv2.waitKey(0)

        # print(detected_digits)
        return detected_digits

def main():
    """
    Example usage of the OCR module.
    Loads an image, resizes and converts it to RGB, and performs OCR.
    """
    image_path = '1.png'
    if not os.path.exists(image_path):
        print(f"[Error] Image file '{image_path}' not found.")
        return

    img = cv2.imread(image_path)
    img = cv2.resize(img, (720, 640))

    # Initialize OCR object
    ocr = OCR()

    # Extract and print text
    ocr.extract_text(img)

    # Uncomment to visualize character or word detection
    # ocr.display_detected_characters(img)

    # words = ocr.detect_only_words(img)
    # print("Words found:", words)

    # digits = ocr.detect_only_digits(img)
    # print("Digits found:", digits)

if __name__ == "__main__":
    main()