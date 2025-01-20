import cv2
import mediapipe as mp
import json
import os
import numpy as np
import pyttsx3  # Import text-to-speech library
import time  # Import time library for delay handling

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Folder containing gesture data and videos
gesture_data_folder = "gesture_data"
video_folder = "videos"

# Ensure the folders exist
os.makedirs(gesture_data_folder, exist_ok=True)
os.makedirs(video_folder, exist_ok=True)

# Function to normalize hand landmarks relative to wrist
def normalize_landmarks(landmarks):
    wrist = landmarks[0]  # Wrist landmark (Base reference)
    normalized_landmarks = []

    for lm in landmarks:
        normalized_landmarks.append({
            'x': lm.x - wrist.x,  # Relative X
            'y': lm.y - wrist.y,  # Relative Y
            'z': lm.z - wrist.z   # Relative Z
        })
    
    return normalized_landmarks

# Function to save gesture landmarks
def save_gesture_landmarks(gesture_name, landmarks):
    gesture_file = os.path.join(gesture_data_folder, f"{gesture_name}.json")
    normalized_data = normalize_landmarks(landmarks)

    with open(gesture_file, 'w') as f:
        json.dump(normalized_data, f)
    print(f"Gesture '{gesture_name}' saved!")

# Function to load saved gesture landmarks
def load_gesture_landmarks(gesture_name):
    gesture_file = os.path.join(gesture_data_folder, f"{gesture_name}.json")
    if os.path.exists(gesture_file):
        with open(gesture_file, 'r') as f:
            return json.load(f)
    return None

# Function to compare two gestures using Euclidean distance
def compare_gestures(saved_gesture, current_landmarks):
    normalized_current = normalize_landmarks(current_landmarks)
    threshold = 0.1  # Adjust for accuracy
    
    distances = []
    for saved, current in zip(saved_gesture, normalized_current):
        distance = np.linalg.norm([saved['x'] - current['x'], saved['y'] - current['y'], saved['z'] - current['z']])
        distances.append(distance)

    avg_distance = np.mean(distances)
    return avg_distance < threshold  # True if similar

# Function to play the avatar video
def play_avatar_video(video_path):
    if not os.path.exists(video_path):
        print(f"Video file '{video_path}' not found.")
        return

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Unable to open video file '{video_path}'.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Avatar Video", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):  # Press 'q' to quit video
            break

    cap.release()
    cv2.destroyAllWindows()

# Open the webcam
cap = cv2.VideoCapture(0)

# Timer and state to control audio playback
last_audio_time = 0  # Initialize the last audio playback time
last_recognized_gesture = None  # Store the last recognized gesture

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)  # Flip for selfie view
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    recognized_gesture = None  # Variable to store recognized gesture name

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Check for saved gestures
            for gesture_name in os.listdir(gesture_data_folder):
                if gesture_name.endswith(".json"):
                    saved_gesture = load_gesture_landmarks(gesture_name[:-5])
                    if saved_gesture and compare_gestures(saved_gesture, landmarks.landmark):
                        recognized_gesture = gesture_name[:-5]
                        break  # Stop checking if one is recognized

            # Save new gesture (Press 's' to save)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                gesture_name = input("Enter gesture name to save: ")
                save_gesture_landmarks(gesture_name, landmarks.landmark)

    # Display recognized gesture or prompt
    if recognized_gesture:
        cv2.putText(frame, f"Gesture: {recognized_gesture}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        print(f"Recognized Gesture: {recognized_gesture}")

        # Check if the recognized gesture is the same as the last one
        if recognized_gesture != last_recognized_gesture:
            # If the gesture has changed, immediately play the audio and video
            engine.say(recognized_gesture)
            engine.runAndWait()

            # Play the corresponding avatar video
            video_path = os.path.join(video_folder, f"{recognized_gesture}.mp4")
            play_avatar_video(video_path)

            last_audio_time = time.time()  # Update the last audio playback time
            last_recognized_gesture = recognized_gesture  # Update the last recognized gesture
        else:
            # If the gesture is the same, play audio only if 6 seconds have passed
            current_time = time.time()
            if current_time - last_audio_time > 6:
                engine.say(recognized_gesture)
                engine.runAndWait()
                last_audio_time = current_time

    else:
        cv2.putText(frame, "No Gesture Recognized", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        last_recognized_gesture = None  # Reset the last recognized gesture if no gesture is detected

    # Display the frame
    cv2.imshow("Gesture Detection", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
