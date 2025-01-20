import cv2
import os

# Folders containing videos and sign language images
video_folder = "videos/"
sign_language_folder = "sign_language_images/"

# Predefined words mapped to video filenames
word_video_dict = {
    "HELLO": "hello.mp4",
    "THANK YOU": "thankyou.mp4",
    "WELCOME": "welcome.mp4",
    "GOOD MORNING": "good morning.mp4",
    "GOOD BYE": "Good bye.mp4",
    "GOOD NIGHT": "good night.mp4",
    "HELP": "help.mp4",
    "HOWAREYOU": "howareyou.mp4",
    "PLEASE": "please.mp4",
    "STOP": "stop.mp4",
    "NO": "no.mp4",
    "YES": "yes.mp4",
    "UNDERSTAND": "understand.mp4",
    "NOT UNDERSTAND": "not understand.mp4",
    "SORRY": "sorry.mp4"
}

# Dictionary to map alphabets to image filenames
sign_language_dict = {}

# List of alphabets to save
alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Load images for each alphabet and store them in a dictionary
for alphabet in alphabets:
    image_path = os.path.join(sign_language_folder, f"{alphabet}.png")  # Assuming images are named A.png, B.png, etc.
    if os.path.exists(image_path):
        sign_language_dict[alphabet] = cv2.imread(image_path)
    else:
        print(f"Image for {alphabet} not found in folder.")

# Function to play a video
def play_video(video_path):
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

        cv2.imshow("Video Playback", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to display sign language images for a given word
def show_sign_language_slideshow(word):
    for letter in word.upper():
        if letter == " ":
            continue  # Skip spaces
        if letter.isalpha():
            if letter in sign_language_dict:
                cv2.imshow(f"Sign Language Gesture for {letter}", sign_language_dict[letter])
                cv2.waitKey(1000)  # Wait 1 second before next image
            else:
                print(f"Sign language gesture for '{letter}' not available.")
        else:
            print(f"'{letter}' is not a valid letter for sign language gestures.")

    cv2.destroyAllWindows()

# Get text input from user
word_input = input("Enter a word or phrase: ").strip().upper()

if word_input:
    # Check if the input is in the predefined dictionary
    if word_input in word_video_dict:
        video_path = os.path.join(video_folder, word_video_dict[word_input])
        print(f"Playing video for '{word_input}'...")
        play_video(video_path)
    else:
        print(f"No predefined video for '{word_input}'. Showing letter-by-letter gestures.")
        show_sign_language_slideshow(word_input)
