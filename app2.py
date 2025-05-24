import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf

# Set page configuration
st.set_page_config(page_title="MediSync", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .header {
        color: #5E4B8C;  /* Lavender */
        font-size: 40px;
        background-color: #E8EAF6; /* Light Purple */
        padding: 10px;
        border-radius: 10px;
    }
    .subheader {
        color: #7A9BBA; /* Light Blue */
        font-size: 24px;
        background-color: #D1E8E2; /* Light Teal */
        padding: 8px;
        border-radius: 10px;
    }
    .text {
        color: #333333; /* Dark Grey */
    }
    .button {
        background-color: #D7B7E6; /* Light Lavender */
        color: white;
        border-radius: 5px;
    }
    .form {
        background-color: #F0F4F8; /* Light Grey */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .doctor-box {
        background-color: #FFECF0; /* Light Pink */
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        border: 1px solid #FFB3C1; /* Soft Pink Border */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Simulated hospital data based on locations in Tamil Nadu with departments and doctors
hospital_data = {
    "Chennai": {
        "Apollo Hospital": {
            "Cardiology": [
                ("Dr. A. Kumar", "9:00 AM - 12:00 PM"),
                ("Dr. B. Suresh", "1:00 PM - 4:00 PM"),
                ("Dr. C. Iyer", "5:00 PM - 7:00 PM"),
            ],
            "Neurology": [
                ("Dr. D. Nair", "10:00 AM - 1:00 PM"),
                ("Dr. E. Mehta", "2:00 PM - 5:00 PM"),
                ("Dr. F. Ravi", "5:00 PM - 8:00 PM"),
            ],
            "Orthopedics": [
                ("Dr. G. Sharma", "8:00 AM - 11:00 AM"),
                ("Dr. H. Verma", "12:00 PM - 3:00 PM"),
            ],
            "Oncology": [
                ("Dr. I. Patel", "9:30 AM - 12:30 PM"),
                ("Dr. J. Natarajan", "1:30 PM - 4:30 PM"),
            ],
        },
        "Fortis Malar Hospital": {
            "Orthopedics": [
                ("Dr. K. Singh", "8:00 AM - 11:00 AM"),
                ("Dr. L. Ramesh", "12:00 PM - 3:00 PM"),
                ("Dr. M. Rao", "4:00 PM - 7:00 PM"),
            ],
            "General Surgery": [
                ("Dr. N. Gupta", "10:00 AM - 1:00 PM"),
                ("Dr. O. Joshi", "2:00 PM - 5:00 PM"),
            ],
        },
        "MIOT International": {
            "Gastroenterology": [
                ("Dr. P. Raghavan", "9:00 AM - 12:00 PM"),
                ("Dr. Q. Chatterjee", "1:00 PM - 4:00 PM"),
            ],
            "Endocrinology": [
                ("Dr. R. Kumar", "10:30 AM - 1:30 PM"),
                ("Dr. S. Ravi", "2:30 PM - 5:30 PM"),
            ],
        },
    },
    "Coimbatore": {
        "Coimbatore Medical College Hospital": {
            "Pediatrics": [
                ("Dr. T. Ramesh", "9:30 AM - 12:30 PM"),
                ("Dr. U. Nithya", "1:30 PM - 4:30 PM"),
            ],
            "Cardiology": [
                ("Dr. V. Kumar", "8:00 AM - 11:00 AM"),
                ("Dr. W. Sharma", "12:00 PM - 3:00 PM"),
            ],
        },
        "Kovai Medical Center and Hospital": {
            "General Surgery": [
                ("Dr. X. Iyer", "10:00 AM - 1:00 PM"),
                ("Dr. Y. Verma", "2:00 PM - 5:00 PM"),
            ],
            "Dermatology": [
                ("Dr. Z. Patel", "9:00 AM - 12:00 PM"),
                ("Dr. A1. Suresh", "1:00 PM - 4:00 PM"),
            ],
            "Orthopedics": [
                ("Dr. B1. Nair", "8:00 AM - 11:00 AM"),
                ("Dr. C1. Gupta", "12:00 PM - 3:00 PM"),
            ],
        },
    },
    "Madurai": {
        "Madurai Meenakshi Mission Hospital": {
            "Internal Medicine": [
                ("Dr. D1. Kumar", "9:00 AM - 12:00 PM"),
                ("Dr. E1. Nithya", "1:00 PM - 4:00 PM"),
            ],
            "Obstetrics and Gynecology": [
                ("Dr. F1. Mehta", "10:00 AM - 1:00 PM"),
                ("Dr. G1. Rani", "2:00 PM - 5:00 PM"),
            ],
        },
        "Nirmal Hospital": {
            "Ophthalmology": [
                ("Dr. H1. Raghavan", "9:30 AM - 12:30 PM"),
                ("Dr. I1. Joshi", "1:30 PM - 4:30 PM"),
            ],
            "Nephrology": [
                ("Dr. J1. Nair", "10:00 AM - 1:00 PM"),
                ("Dr. K1. Verma", "2:00 PM - 5:00 PM"),
            ],
        },
    },
}

# Sidebar navigation menu
st.sidebar.title("Navigation")
menu = ["Home", "Book Appointment", "Upload Prescription", "Symptom Tracker", "Chatbot", "Summary"]
choice = st.sidebar.selectbox("Navigate", menu)

# Load the pre-trained model (ensure model.h5 is in the correct path)
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("my_model.h5")  # Replace with the actual path to your model
    return model

model = load_model()

# Preprocessing function to match model input requirements
def predict(image, model):
    img = image.resize((220, 220))  # Resize to 220x220 as required by your model
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = np.array(img) / 255.0  # Normalize the image
    prediction = model.predict(img)  # Predict using the loaded model
    return prediction

# Home Page
if choice == "Home":
    st.title("Welcome to MediSync", anchor='welcome')
    st.markdown('<div class="header">Your Complete Healthcare Management Hub</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="text">
        Our goal is to streamline and enhance your healthcare experience with seamless appointment scheduling, 
        prescription delivery, symptom tracking, and interactive chatbot support in English and regional languages.
        </div>
    """, unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1580281657527-47d671e7a63a", caption="Healthcare Optimization")

# Enhanced Book Appointment Page
elif choice == "Book Appointment":
    st.header("Book a Hospital Appointment")
    st.markdown('<div class="subheader">Find nearby hospitals in Tamil Nadu and book an appointment.</div>', unsafe_allow_html=True)

    # Doctor selection
    with st.form(key='doctor_selection_form'):
        city = st.selectbox("Select Your City", list(hospital_data.keys()), key='city_select')
        
        if city:
            hospital = st.selectbox("Select Your Hospital", list(hospital_data[city].keys()), key='hospital_select')
            
            if hospital:
                department = st.selectbox("Select Department", list(hospital_data[city][hospital].keys()), key='department_select')
                
                if department:
                    doctors = hospital_data[city][hospital][department]
                    st.write(f"Available Doctors in {department} at {hospital}:")

                    # Display available doctors and their timings
                    doctor_options = []
                    for doctor, timing in doctors:
                        doctor_options.append(doctor)
                        st.markdown(f'<div class="doctor-box">- <strong>{doctor}</strong> | Available: {timing}</div>', unsafe_allow_html=True)

                    # Appointment Date and Time selection
                    appointment_date = st.date_input("Select Appointment Date")
                    appointment_time = st.time_input("Select Appointment Time")
                    
                    # Choose a Doctor button
                    selected_doctor = st.selectbox("Choose a Doctor", doctor_options, key='doctor_select')
                    
                    # Book appointment button
                    submitted = st.form_submit_button("Book Appointment")
                    if submitted:
                        st.session_state.selected_doctor = selected_doctor
                        st.session_state.hospital = hospital
                        st.session_state.city = city
                        st.session_state.department = department
                        st.session_state.appointment_date = appointment_date
                        st.session_state.appointment_time = appointment_time
                        st.success(f"Appointment booked with {selected_doctor} at {hospital} on {appointment_date} at {appointment_time}.")
    
    st.markdown('<div class="form"></div>', unsafe_allow_html=True)


# Upload Prescription Page
elif choice == "Upload Prescription":
    st.header("Upload Your Prescription")

    st.markdown('<div class="subheader">Upload a photo or scan of your prescription for medicine delivery.</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a prescription file", type=["jpg", "jpeg", "png", "pdf"])

    if uploaded_file is not None:
        st.image(Image.open(uploaded_file), caption="Uploaded Prescription", use_column_width=True)
        st.write("Prescription uploaded. Your medications will be delivered soon.")

    # Option for automated refills
    if st.checkbox("Enable monthly automatic prescription refills"):
        st.success("Automated refills enabled! You will receive your medications every month.")
        
        # Terminate the subscription button
        if st.button("🛑 Terminate Auto-Renewal"):
            st.warning("Automated prescription refills have been terminated.")

# Symptom Tracker Page
elif choice == "Symptom Tracker":
    st.header("Symptom Tracker")
    st.markdown('<div class="subheader">Track your symptoms by uploading images of wounds or scans.</div>', unsafe_allow_html=True)
    
    symptom_type = st.selectbox("Choose Symptom Type", ["External Wound", "Internal Scan"])
    
    if symptom_type == "External Wound":
        uploaded_symptom = st.file_uploader("Upload Wound Image", type=["jpg", "jpeg", "png"])
        if uploaded_symptom is not None:
            image = Image.open(uploaded_symptom)
            st.image(image, caption="Uploaded Wound Image", use_column_width=True)
            st.write("Wound image uploaded successfully.")
            
            if st.button("Analyze Wound"):
                with st.spinner("Analyzing..."):
                    # Call the updated predict function and pass the loaded model
                    prediction = predict(image, model)
                    predicted_class = np.argmax(prediction, axis=1)[0]
                    
                    # Assuming your model has predefined classes (e.g., 0 = "Minor Wound", 1 = "Severe Wound", etc.)
                    wound_classes = {0: "Bruises", 1: "Burns", 2: "Cut", 3: "Laceration", 4: "Stab wound"}
                    analysis_result = wound_classes.get(predicted_class, "Unknown Wound Type")
                
                st.success(f"Wound Analysis Result: {analysis_result}")

    elif symptom_type == "Internal Scan":
        uploaded_scan = st.file_uploader("Upload Scan Image", type=["jpg", "jpeg", "png", "pdf"])
        if uploaded_scan is not None:
            st.image(Image.open(uploaded_scan), caption="Uploaded Scan", use_column_width=True)
            st.write("Scan uploaded successfully.")

# Chatbot Page
elif choice == "Chatbot":
    st.header("MediSync Chatbot")
    st.markdown('<div class="subheader">Ask your medical queries here.</div>', unsafe_allow_html=True)

    user_query = st.text_input("Type your question here:")
    if st.button("Submit"):
        # Simulated response
        st.success("Chatbot Response: Please consult with a healthcare professional for accurate information.")

# Summary Page
elif choice == "Summary":
    st.header("Appointment Summary")
    st.markdown('<div class="subheader">Here are your appointment details:</div>', unsafe_allow_html=True)

    if 'city' in st.session_state:
        st.write(f"You have chosen {st.session_state.selected_doctor} as your doctor.")
        st.write(f"You are appointed at {st.session_state.hospital} located in {st.session_state.city}.")
        st.write(f"The appointment is for the {st.session_state.department} department.")
        st.write(f"Your appointment is scheduled for {st.session_state.appointment_date} at {st.session_state.appointment_time}.")
        st.success("Thank you for using MediSync! We look forward to assisting you with your healthcare needs.")
    else:
        st.write("No appointment details available. Please book an appointment first.")

# Footer
st.markdown("""
    <style>
    footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)