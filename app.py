import streamlit as st
from streamlit_option_menu import option_menu

# Import fungsi dari file yang ada di dalam folder 'pages'
from pages.dashboard import tampilkan_dashboard
from pages.profil import tampilkan_profil

st.set_page_config(layout="wide")

# Menyembunyikan menu bawaan folder 'pages'
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Taruh option_menu di dalam sidebar
with st.sidebar:
    pilihan = option_menu(
        menu_title="Main Menu",  
        options=["Dashboard", "Profil"], 
        icons=["", ""],  
        menu_icon=" ",   
        default_index=0, 
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"display": "none"}, # 3. Tambahkan ini agar spasi/tempat icon benar-benar hilang
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#0056b3"}, # Saya ubah warnanya sedikit biar mirip gambar referensimu (biru)
        }
    )

# Logika untuk menampilkan konten
if pilihan == "Dashboard":
    tampilkan_dashboard()
elif pilihan == "Profil":
    tampilkan_profil()