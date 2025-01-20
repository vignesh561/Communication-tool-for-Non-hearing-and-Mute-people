import speech_recognition as sr
import cv2
import os

# Folders containing videos and sign language images
video_folder = "videos/"

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

# Function to capture voice input and convert it to text
def capture_voice_input():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Please speak now...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized Text: {text}")
        return text.strip().upper()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

# Function to recognize speech and play the corresponding video
def speech_to_avatar():
    text = capture_voice_input()
    if text and text in word_video_dict:
        video_path = os.path.join(video_folder, word_video_dict[text])
        print(f"Playing video for: {text}")
        play_video(video_path)
    else:
        print(f"No predefined video for '{text}' or unrecognized input.")

if __name__ == "__main__":
    speech_to_avatar()
