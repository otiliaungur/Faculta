import streamlit as st
from Acasa import recunoastere
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av

#st.set_page_config(page_title='Live', layout='wide')
st.subheader('Prezenta live')


#Iau date din Redis DB
db_redis = recunoastere.culegere_date(name='inregistrare')

# Recunoastere live - cod din github stteamlit
#callback function
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img_final = recunoastere.analiza_fata(img, db_redis,'Trasaturi', ['Nume', 'Functie'], punct_detectie=0.5)
    return av.VideoFrame.from_ndarray(img_final, format="bgr24")


webrtc_streamer(key="prezicerelive", video_frame_callback=video_frame_callback)

st.markdown("#### Lista tuturor persoanelor inregistrate in baza de date :")
st.dataframe(db_redis)