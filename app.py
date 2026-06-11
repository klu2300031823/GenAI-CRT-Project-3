import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image

st.set_page_config(page_title="Maintenance Copilot")

st.title("🔧 Maintenance Copilot")

manual = st.file_uploader(
    "Upload Maintenance Manual (PDF)",
    type="pdf"
)

sensor_event = st.text_area(
    "Enter Sensor Event",
    placeholder="Temperature = 95°C"
)

image = st.file_uploader(
    "Upload Equipment Image",
    type=["jpg", "jpeg", "png"]
)

if st.button("Analyze"):

    if not manual:
        st.error("Upload manual PDF")
        st.stop()

    text = ""

    reader = PdfReader(manual)

    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"

    issue = "Unknown"

    if "temperature" in sensor_event.lower():
        issue = "Possible Overheating"

    elif "vibration" in sensor_event.lower():
        issue = "Possible Bearing Problem"

    elif "pressure" in sensor_event.lower():
        issue = "Possible Leakage"

    st.subheader("📋 Maintenance Report")

    st.write("**Detected Issue:**", issue)

    st.write("**Sensor Event:**", sensor_event)

    st.write("**Relevant Manual Content:**")
    st.write(text[:1000])

    if image:
        img = Image.open(image)

        st.write("**Image Evidence:**")
        st.image(img, width=300)

    st.success("Analysis Complete")
