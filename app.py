import streamlit as st
import smtplib
import zipfile
from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(email, file):
    msg = MIMEMultipart()
    msg['Subject'] = 'Mashup'
    msg['From'] = 'grewal.harry.music@gmail.com'
    msg['To'] = email
    
    with open(file, 'rb') as f:
        file = MIMEApplication(f.read(),_subtype = "zip")
        file.add_header('content-disposition','attachment',filename='result.zip')
        msg.attach(file)
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('grewal.harry.music@gmail.com', 'iuuu gevs atwy wncx')
    s.sendmail('grewal.harry.music@gmail.com', [email], msg.as_string())
    s.quit()

st.set_page_config(page_title="Mashup", layout="centered")

st.markdown("<h1 style='text-align: center; color: Red;'>Mashup </h1>", unsafe_allow_html=True)

singername = st.text_input("Singer name:")
sn = singername.replace(' ','') + "songs"
number_of_videos = st.number_input("Number of videos:", step=1, format='%d')
duration_of_each_video = st.number_input("Duration of videos:", step=1, format='%d')
email = st.text_input("Email: ")
resultfile = 'result.mp3'
if st.button("Generate"):
    st.write("Please wait for results to be sent on your email")
    st.write("Please refresh on error.")

    # Perform the mashup generation
    urls = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(sn))
    id_video = re.findall(r"watch\?v=(\S{11})", urls.read().decode())

    for i in range(number_of_videos):
        ytube = YouTube("https://www.youtube.com/watch?v=" + id_video[i]) 
        print("File "+str(i+1)+" Downloading!")
        mp4files = ytube.streams.filter(only_audio=True).first().download(filename='videofile-'+str(i)+'.mp3')

    print("Mashup generation in process")
    if os.path.isfile("videofile-0.mp3"):
        final_audio = AudioSegment.from_file("videofile-0.mp3")[:duration_of_each_video*1000]
    for i in range(1,number_of_videos):
        aud_file = str("videofile-"+str(i)+".mp3")
        final_audio = final_audio.append(AudioSegment.from_file(aud_file)[:duration_of_each_video*1000],crossfade=1000)
    
    try:
        final_audio.export(resultfile, format="mp3")
    except:
        sys.exit("Error")
     
    result = str("result.mp3" )
    # Create the zip file
    with zipfile.ZipFile('result.zip', mode='w') as archive:
        archive.write(result)
    # Send the email with the zip file
    send_email(email, 'result.zip')
    st.success("Result sent ")
