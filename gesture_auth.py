import json
import os
import time


PROFILES_DIR = "profiles"


class GestureAuth:
    def __init__(self):
        os.makedirs(PROFILES_DIR, exist_ok=True)

        # TODO: Initialize your state variables
        #   - What mode is the app in? (idle, enrolling, confirming, verifying)
        #   - What is the current username?
        #   - What is the enrolled gesture sequence?
        #   - What is the current gesture sequence being recorded?
        #   - How many times has the user confirmed during enrollment?
        #   - What gesture is currently being held? When did it start?
        #   - Has the current gesture already been registered (to prevent duplicates)?
        #   - What is the current status message to show the user?
        #   - What is the current result (GRANTED/DENIED) and when should it disappear?
        pass

    def start_enrollment(self, username):
        """Begin enrollment for a new user."""
        # TODO: Set mode to enrolling, store username, reset sequences
        pass

    def start_verification(self, username):
        """Begin verification — load the user's profile and prepare to compare."""
        # TODO: Load the profile JSON from profiles/username.json
        # TODO: If profile doesn't exist, show error
        # TODO: Set mode to verifying, store the enrolled sequence
        pass

    def process_gesture(self, gesture, score):
        """Called EVERY FRAME with the current gesture. YOU handle debouncing here."""
        # TODO: Ignore if not in an active mode (enrolling/confirming/verifying)
        # TODO: Ignore low-confidence or "none" gestures
        # TODO: DEBOUNCING LOGIC:
        #   - If this is a NEW gesture (different from what was being held), start a timer
        #   - If this is the SAME gesture held for 0.5+ seconds, REGISTER it
        #   - After registering, LOCK so it doesn't register again while still held
        #   - UNLOCK when the gesture changes
        pass

    def finish_sequence(self):
        """Called when user presses SPACE to signal their sequence is done."""
        # TODO: If enrolling → validate minimum length, switch to confirmation mode
        # TODO: If confirming → compare against enrolled sequence
        #       Match → increment counter, if 3 matches → save profile
        #       Mismatch → show error, let them retry
        # TODO: If verifying → compare against enrolled sequence
        #       Match → ACCESS GRANTED
        #       Mismatch → ACCESS DENIED
        pass

    def cancel(self):
        """Called when user presses ESC."""
        # TODO: Reset everything back to idle
        pass

    def _save_profile(self):
        """Save the enrolled sequence to profiles/username.json"""
        # TODO: Create a dict with username, gesture_sequence, created_at
        # TODO: json.dump it to profiles/username.json
        pass

    def _load_profile(self, username):
        """Load a profile from profiles/username.json, return None if not found."""
        # TODO: Check if file exists, read and return json.load, or return None
        pass
