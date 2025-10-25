import streamlit as st #frontend
import smtplib #simple mail transfer protocol - send email using SMTP
import random #For otp generation
import os #accessing enviorment variable
from email.mime.multipart import MIMEMultipart #multi media internet messsaging - to format email
from email.mime.text import MIMEText #to add plain text in email
from dotenv import load_dotenv #to load envirment variable

#accessing enviroment over here inside the code
load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
PASSWORD =  os.getenv("EMAIL_PASS")

st.title("Email OTP Verification App")

if "otp" not in st.session_state:
    st.session_state.otp = None

with st.form("otp_form"):
    user_email = st.text_input("Enter your email address:")
    send_Clicked = st.form_submit_button("send OTP")

if send_Clicked:
    if EMAIL is None or PASSWORD is None:
        st.error("Invalid Email or Password")
    elif user_email == "":
        st.warning("Please enter email ID")
    else :
        st.session_state.otp = random.randint(1000,9999)

        body = f"OTP for verification:  {st.session_state.otp}"

        msg = MIMEMultipart()
        msg["form"] = EMAIL
        msg["to"] = user_email
        msg["Subject"] = "OTP to steal all your money"
        msg.attach(MIMEText(body,"plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com" ,587)
            server.starttls()
            server.login(EMAIL,PASSWORD)
            server.send_message(msg)
            server.quit()
            st.success("OTP fired successfully")

        except:
            st.error("Authentication Fails OR Internet Issue")

#verify the otp you entered is right or wrong
if st.session_state.otp:
    entered_otp = st.text_input("Enter OTP you recieved in Email:")
    if st.button("Verify OTP"):
        if int(entered_otp) == st.session_state.otp:
            st.success("OTP match")
        else :
            st.error("Wrong OTP")