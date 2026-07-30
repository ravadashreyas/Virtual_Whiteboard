# VisionSlate

VisionSlate is a webcam-based authentication system that uses hand gestures as a password. Instead of typing a passphrase, a user enrolls a secret sequence of hand gestures (for example: thumbs up, open palm, victory sign) and later logs in by repeating that sequence in front of the camera. A blink-based liveness check runs first, so the system cannot be fooled by holding up a photo of the user.

Everything runs locally in real time using MediaPipe and OpenCV. No cloud services or API keys are required.

## How it works

1. **Liveness check.** MediaPipe Face Mesh tracks the user's face, and the eye aspect ratio (EAR) of both eyes is computed every frame. The user must blink twice within a time limit to be confirmed as a live person. A depth check on the face landmarks' z-coordinates rejects flat images such as printed photos or phone screens.
2. **Gesture recognition.** Once liveness is confirmed, MediaPipe's pre-trained Gesture Recognizer model (`gesture_recognizer.task`) classifies the hand gesture in each frame. Recognized gestures include Closed Fist, Open Palm, Pointing Up, Thumb Up, Thumb Down, Victory, and I Love You.
3. **Sequence capture with debouncing.** A gesture must be held steadily for half a second before it is registered, which prevents accidental or transitional gestures from being added to the sequence. Lowering the hand between gestures allows the same gesture to be entered twice in a row.
4. **Enrollment and verification.** During enrollment the user records a sequence of at least three gestures and then repeats it once to confirm before it is saved. During verification the entered sequence is compared against the stored profile, and the screen shows ACCESS GRANTED or ACCESS DENIED.

User profiles are stored as JSON files in a local `profiles/` directory, one file per username.

## Requirements

- Python 3.9+
- A webcam
- Dependencies:

```
pip install -r requirements.txt
```

## Usage

Run the app from the repository root (the `gesture_recognizer.task` model file must be in the working directory):

```
python auth_app.py
```

A window opens showing the webcam feed with hand landmarks, face mesh contours, the currently detected gesture, and status messages.

### Controls

| Key   | Action                                                 |
| ----- | ------------------------------------------------------ |
| E     | Enroll a new user (enter a username in the terminal)   |
| V     | Verify an existing user (enter a username)             |
| SPACE | Finish entering the current gesture sequence           |
| ESC   | Cancel the current enrollment or verification          |
| Q     | Quit                                                   |

### Typical flow

1. Start the app and press `E`, then type a username in the terminal.
2. Blink twice at the camera to pass the liveness check.
3. Hold each gesture of your secret sequence for about half a second until it registers (minimum three gestures), then press SPACE.
4. Repeat the same sequence to confirm, then press SPACE again. Enrollment is saved.
5. To log in later, press `V`, enter the username, pass the liveness check, repeat your sequence, and press SPACE.

## Project structure

| File                      | Purpose                                                                 |
| ------------------------- | ----------------------------------------------------------------------- |
| `auth_app.py`             | Main application: camera loop, gesture recognition, UI overlay, input   |
| `gesture_auth.py`         | Enrollment/verification state machine, debouncing, profile storage      |
| `liveness.py`             | Blink-based liveness detection using eye aspect ratio and a depth check |
| `distance.py`             | Small geometry helpers for landmark distances                           |
| `gesture_recognizer.task` | MediaPipe pre-trained gesture recognition model                         |
| `old_files/`              | Earlier prototype of the project (air-drawing math solver)              |

## Project history

VisionSlate began as an air-writing whiteboard: the user drew math expressions in the air with a fingertip, and the app solved them (first with the Gemini API, later with local image processing). That prototype lives in `old_files/`. The project then pivoted to its current form, a gesture-sequence password system with liveness detection.

## Limitations

- Gesture sequences are stored in plain-text JSON, so this is a demonstration of the concept rather than production-grade security.
- The gesture vocabulary is limited to the classes supported by MediaPipe's pre-trained recognizer.
- Liveness detection is blink-based and defeats static photos, but it is not designed to resist sophisticated attacks such as replayed video.
