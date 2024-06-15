import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Lucrare practica de licenta', layout='wide', )
#link_img = " "
link_img = "https://www.lystloc.com/blog/wp-content/uploads/2023/01/6-Key-Use-Cases-Of-A-Facial-Recognition-System-In-Day-To-Day-Life.webp"


with st.sidebar:
    st.write("### Mai multe")
    select = option_menu(menu_title=None, options=["Despre", "Contact"],
                         icons=["info-square", "chat-dots"], menu_icon="cast",
                         default_index=1, orientation="vertical", styles={
            "container": {"padding-top": "0!important", "padding-bottom": "0!important",
                          "padding-right": "5px", "padding-left": "0px", "background-color": "#fafafa",
                          "float": "right"},
            "icon": {"color": "orange", "font-size": "15px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px",
                         "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green"}, })

    if select == "Despre":
        st.markdown("""
    ### Descriere
    Aceasta aplicatie web contine 2 pagini incorporate ce permit inregistrarea si detectarea trasaturilor faciale :
    - **Prezenta live**: Permite utilizatorului să vadă persoanele înregistrate în baza de date și să le identifice în timp real cu ajutorul unei camere.
    - **Formular de înregistrare**: Utilizatorii își pot introduce datele și înregistra trăsăturile faciale.

    Funcțiile profesor/student sunt strict fictive și pot fi adaptate în funcție de cerințe.
    """)
    elif select == "Contact":
        st.write("E-mail: otilia.ungur03@e-uvt.ro")
           
css_styles = """
<style>
body {
    background-color: #f0f0f0; /* Change this color to the desired background color */
}
.title {
    font-size: 50px;
    font-family: 'Stencil Std', fantasy;
    font-weight: normal;
    text-align: left;
    color: #156b2f;
    margin-bottom: 20px;
    width: 50%;
    margin-left: 7px;
    margin-right: auto;
    margin-top: None;
}

.imagine {
    max-width: 55%;
    margin-top: 0px;
    margin-left: 0 px;
    margin-right: 1px;
    text-align: right;
}

.header-container {
    margin-top:None;
    display: flex;
    align-items: center;
}

.image-source {
    text-align: right;
    color: #666;
    font-size: 8px;
    font-style: italic;
    margin-top: 1px;
}

</style>
"""
# Apply the CSS styles
st.markdown(css_styles, unsafe_allow_html=True)

# Titlu
#st.markdown('<h1 class="title">Sistem de recunoastere faciala</h1>', unsafe_allow_html=True)
#st.markdown(f'<div class="image-container"><img src="{link_img}" width="100%"></div>', unsafe_allow_html=True)

#am facut container cu titlul si poza din motive stilistice, se putea si mai simplu
st.markdown(f"""
<div class="header-container">
    <div class="title">Sistem de recunoastere faciala</div>
    <img class="imagine" src="{link_img}" alt="Facial Recognition">
</div>
<p class="image-source"><a href="{link_img}" target="_blank">{link_img}</a></p>
""", unsafe_allow_html=True) #pentru a accepta stilurile in format css si html
 

with st.spinner('Incarcare date...'):
    import recunoastere
st.success('Date incarcate cu succes')
st.success('Conectat la baza de date')