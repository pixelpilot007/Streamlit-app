# 1.Load Flights & Passenger Booking
import streamlit as st
import pandas as pd
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import face_recognition
import os

st.set_page_config(page_title="DigiYatra Passenger System", layout="wide")

# Load flight data
@st.cache_data
def load_flights():
    return pd.DataFrame({
        "Flight No": ["AI101", "6E202", "SG303"],
        "Airline": ["Air India", "Indigo", "SpiceJet"],
        "From": ["Delhi", "Mumbai", "Bengaluru"],
        "To": ["Bengaluru", "Delhi", "Chennai"],
        "Time": ["10:30 AM", "2:15 PM", "6:50 PM"]
    })

flights = load_flights()

st.title("✈️ DigiYatra Passenger Classification System")

# User selects flight
st.subheader("📌 Select Your Flight")
flight_selected = st.selectbox("Choose a flight:", flights["Flight No"].tolist())

# Fetch selected flight details
flight_details = flights[flights["Flight No"] == flight_selected].iloc[0]
st.write(f"**Airline:** {flight_details['Airline']}")
st.write(f"**Source:** {flight_details['Source']} → **Destination:** {flight_details['Destination']}")
st.write(f"**Price:** ₹{flight_details['Price']}")

# Passenger Details
st.subheader("🛂 Passenger Details")
passenger_name = st.text_input("Enter Name")
email = st.text_input("Enter Email")

# Capture face using webcam
st.subheader("📷 Capture Face for Verification")
captured_image_path = f"passenger_images/{passenger_name}.jpg"

if st.button("Capture Face"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(captured_image_path, frame)
        st.image(frame, caption="Captured Face", use_column_width=True)
        st.success("Face Captured Successfully!")
    cap.release()

# 2.Check-in & Facial Verification
st.subheader("🔍 Check-in & Face Verification")

def compare_faces(image_path1, image_path2):
    image1 = face_recognition.load_image_file(image_path1)
    image2 = face_recognition.load_image_file(image_path2)

    face_encodings1 = face_recognition.face_encodings(image1)
    face_encodings2 = face_recognition.face_encodings(image2)

    if not face_encodings1 or not face_encodings2:
        return False

    return face_recognition.compare_faces([face_encodings1[0]], face_encodings2[0])[0]

live_image_path = "live_checkin.jpg"

if st.button("Verify Identity"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(live_image_path, frame)
        st.image(frame, caption="Live Check-in Image", use_column_width=True)
    cap.release()

    if compare_faces(captured_image_path, live_image_path):
        st.success("✅ Identity Verified! Boarding Pass Approved.")
        st.balloons()
    else:
        st.error("❌ Identity Mismatch! Please try again.")

