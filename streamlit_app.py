import streamlit as st
import numpy as np
import pickle
import os

# Load model
model_path = os.path.join("final_model", "model_balanced.pkl")
model = pickle.load(open(model_path, "rb"))

# App layout
st.markdown("<h1 style='text-align: center;'>🔐 Network Threat Detector</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 14px;'>Simulate phishing vs safe behavior with 4 questions. "
    "Remaining features are auto-configured based on your answers.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# All 30 features expected by the model
all_features = [
    'having_IP_Address', 'URL_Length', 'Shortining_Service', 'having_At_Symbol',
    'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State',
    'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL',
    'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL',
    'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain',
    'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page',
    'Statistical_report'
]

# Key features and questions
feature_questions = {
    "having_IP_Address (Does the URL contain an IP address?)": "having_IP_Address",
    "Shortining_Service (Is a URL shortener used?)": "Shortining_Service",
    "SSLfinal_State (Is SSL certificate valid?)": "SSLfinal_State",
    "Abnormal_URL (Does the URL look abnormal?)": "Abnormal_URL"
}

input_map = {"Yes": 1, "No": -1}
user_inputs_dict = {}

# Display user input widgets in columns
cols = st.columns(2)
for i, (label, key) in enumerate(feature_questions.items()):
    with cols[i % 2]:
        response = st.selectbox(label, options=["Yes", "No"])
        user_inputs_dict[key] = input_map[response]

# Define what is considered a safe pattern
safe_combo = {
    "having_IP_Address": 1,
    "Shortining_Service": -1,
    "SSLfinal_State": 1,
    "Abnormal_URL": -1
}
is_safe_pattern = all(user_inputs_dict.get(k) == v for k, v in safe_combo.items())

# Final input vector
final_input = []
for feature in all_features:
    if feature in user_inputs_dict:
        final_input.append(user_inputs_dict[feature])
    else:
        final_input.append(1 if is_safe_pattern else -1)

# Predict and display result
if st.button("🔍 Predict"):
    prediction = model.predict([final_input])[0]
    proba = model.predict_proba([final_input])[0]
    confidence = round(max(proba) * 100, 2)

    st.markdown("---")
    if prediction == -1:
        st.error(f"⚠️ This is predicted to be a **phishing website**. (Confidence: {confidence}%)")
    else:
        st.success(f"✅ This website appears to be **safe**. (Confidence: {confidence}%)")
