import streamlit as st
from Acasa import recunoastere
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

st.set_page_config(page_title='Formular inregistrare')
st.subheader('Formular inregistrare')

registration_form = recunoastere.Inregistrare()

#Formular pentru colectarea numelui si functiei
numele_complet = st.text_input(label= 'Va rog sa va introduceti numele:', placeholder='Prenume si Nume')
functia = st.selectbox(label= 'Sunteti student sau profesor?', options=('Student', 'Profesor'))
#Se colecteaza trasaturile faciale
def video_inregistrare(frame):
    img = frame.to_ndarray(format="bgr24")
    img2, embedding = registration_form.get_embedding(img)

    #---------------------------------------------------------------
    if embedding is not None:
            with open('face_embedding.txt',mode='ab') as f:
                np.savetxt(f,embedding)

    return av.VideoFrame.from_ndarray(img2, format="bgr24")

webrtc_streamer(key='salvare', video_frame_callback = video_inregistrare)


#Se salveaza in baza de date
if st.button('Salveaza'):
   return_val = registration_form.save_data_in_redis_db(numele_complet,functia)
   if return_val == True:
        st.success(f"{numele_complet} a fost adaugat/adaugata")
   elif return_val == 'nume_fals':
        st.error('Va rog introduceti numele.')