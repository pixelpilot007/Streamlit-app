import streamlit as st
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

def capture_image():
    """Captures an image from the webcam."""
    cap = cv2.VideoCapture(0)
    st.write("Look at the camera and wait for capture...")
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def save_image(image, filename):
    """Saves an image to the dataset."""
    cv2.imwrite(filename, image)

def load_encoded_faces(path="faces"):
    """Loads and encodes faces from the dataset."""
    encodings = {}
    for file in os.listdir(path):
        image = face_recognition.load_image_file(os.path.join(path, file))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            encodings[file.split('.')[0]] = encoding[0]
    return encodings

def verify_face(image, known_encodings):
    """Verifies a captured face against stored encodings."""
    unknown_encoding = face_recognition.face_encodings(image)
    if unknown_encoding:
        matches = face_recognition.compare_faces(list(known_encodings.values()), unknown_encoding[0])
        if True in matches:
            matched_name = list(known_encodings.keys())[matches.index(True)]
            return matched_name
    return None

# Streamlit App
st.title("DigiYatra Interactive Passenger System")

# Flight Booking
st.header("Step 1: Search for Flight")
source = st.selectbox("From:", ["Bangalore", "Delhi", "Pune", "Mumbai"])
destination = st.selectbox("To:", ["Pune", "Delhi", "Mumbai", "Bangalore"])
date = st.date_input("Select Date", datetime.today())

if st.button("Search Flights"):
    st.success(f"Flights found from {source} to {destination} on {date}")
    st.session_state["booking_done"] = True

# Passenger Registration
if "booking_done" in st.session_state:
    st.header("Step 2: Passenger Registration")
    name = st.text_input("Passenger Name")
    email = st.text_input("Passenger Email")
    if st.button("Capture Face"):
        image = capture_image()
        if image is not None:
            filename = f"faces/{name}.jpg"
            save_image(image, filename)
            st.image(image, caption="Captured Image", use_column_width=True)
            st.success("Face Captured Successfully!")
            st.session_state["registered"] = True

# Boarding Pass Generation
if "registered" in st.session_state:
    st.header("Step 3: Boarding Pass")
    st.write(f"Passenger: {name}")
    st.write(f"Flight: {source} to {destination} on {date}")
    if st.button("Generate Boarding Pass"):
        st.success("Boarding Pass Generated! Proceed to verification.")
        st.session_state["boarding_pass"] = True

# Face Verification
if "boarding_pass" in st.session_state:
    st.header("Step 4: Face Verification")
    known_faces = load_encoded_faces()
    if st.button("Verify Identity"):
        image = capture_image()
        if image is not None:
            verified_name = verify_face(image, known_faces)
            if verified_name:
                st.success(f"Verification Successful! Approved for {verified_name}.")
            else:
                st.error("Verification Failed! Passenger not recognized.")
import face_recognition

image = face_recognition.load_image_file("/Users/madhutomar/Desktop/faces")  # Replace with an actual file in faces/
encoding = face_recognition.face_encodings(image)

if encoding:
    print("Encoding successful!")
else:
    print("Encoding failed!")

results = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=0.6)  # Increase to 0.7 if needed

