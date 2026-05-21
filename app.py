import streamlit as st
from streamlit_option_menu import option_menu

# Import fungsi dari file yang ada di dalam folder 'pages'
from pages.dashboard import tampilkan_dashboard, load_data_klasifikasi
from pages.regresi import tampilan_regresi,load_data_regresi

st.set_page_config(layout="wide")
df_klasifikasi = load_data_klasifikasi()
min_date_klasifikasi = df_klasifikasi['tanggal'].min().date()
max_date_klasifikasi = df_klasifikasi['tanggal'].max().date()

df_regresi = load_data_regresi()
min_date_regresi = df_regresi['tanggal_nabung'].min().date()
max_date_regresi = df_regresi['tanggal_nabung'].max().date()

    
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
        options=["Dashboard Klasifikasi", "Dashboard Regresi"], 
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
    # st.text("Rentang Data Klasifikasi")
    # start_date_klasfikasi = st.sidebar.date_input("Start" , min_date_klasifikasi, min_value=min_date_klasifikasi, max_value=max_date_klasifikasi)
    # end_date_klasfikasi = st.sidebar.date_input("End" , max_date_klasifikasi, min_value=min_date_klasifikasi, max_value=max_date_klasifikasi)

# Logika untuk menampilkan konten
if pilihan == "Dashboard Klasifikasi":
    tampilkan_dashboard()
elif pilihan == "Dashboard Regresi":
    tampilan_regresi()