# AI-Based Virtual Gesture Controller
# Author: Sujitha Mary
# Description: Control mouse, keyboard, and volume using hand gestures.

import cv2
import mediapipe as mp
import pyautogui
import time
import math
import subprocess
import tkinter as tk
from tkinter import ttk


# ---------------- Volume Control ----------------
def volume_controller():
    webcam = cv2.VideoCapture(0)
    hands = mp.solutions.hands.Hands()
    draw = mp.solutions.drawing_utils

    while True:
        ret, img = webcam.read()
        if not ret:
            break

        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                draw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)
                lm = hand.landmark

                x1 = int(lm[8].x * w)
                y1 = int(lm[8].y * h)
                x2 = int(lm[4].x * w)
                y2 = int(lm[4].y * h)

                distance = math.hypot(x2 - x1, y2 - y1)

                if distance > 80:
                    pyautogui.press("volumeup")
                else:
                    pyautogui.press("volumedown")

        cv2.imshow("Volume Control", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()


# ---------------- Virtual Mouse ----------------
def virtual_mouse():

    webcam = cv2.VideoCapture(0)
    hands = mp.solutions.hands.Hands(max_num_hands=1)
    draw = mp.solutions.drawing_utils

    screen_w, screen_h = pyautogui.size()

    while True:
        ret, img = webcam.read()
        if not ret:
            break

        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:

                draw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)

                lm = hand.landmark
                index = lm[8]

                x = int(index.x * w)
                y = int(index.y * h)

                screen_x = int((x / w) * screen_w)
                screen_y = int((y / h) * screen_h)

                pyautogui.moveTo(screen_x, screen_y)

        cv2.imshow("Virtual Mouse", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()


# ---------------- Virtual Keyboard ----------------
def virtual_keyboard():

    cap = cv2.VideoCapture(0)
    hands = mp.solutions.hands.Hands()
    draw = mp.solutions.drawing_utils

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:

            for hand in result.multi_hand_landmarks:

                draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

                lm = hand.landmark
                index = lm[8]

                if index.y < lm[6].y:
                    pyautogui.press("a")

        cv2.imshow("Virtual Keyboard", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------------- GUI ----------------
def main_gui():

    root = tk.Tk()
    root.title("Gesture Control Interface")
    root.geometry("400x300")

    ttk.Button(root, text="Volume Control", command=volume_controller).pack(pady=20)
    ttk.Button(root, text="Virtual Mouse", command=virtual_mouse).pack(pady=20)
    ttk.Button(root, text="Virtual Keyboard", command=virtual_keyboard).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main_gui()
