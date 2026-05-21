import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data_regresi():
    url = "https://raw.githubusercontent.com/Capstone-Catatanku/Data-Science-Tabungan/refs/heads/main/Clean-data/Data_Clean.csv" 
    df = pd.read_csv(url)
    kolom_log = [
        'target_nominal',
        'nominal_nabung',
        'total_terkumpul',
        'sisa_target',
    ]
    for kolom in kolom_log:
        df[kolom] = np.expm1(df[kolom])
    df['tanggal_nabung'] =  pd.to_datetime(df['tanggal_nabung'])   
    df['tahun'] = df['tanggal_nabung'].dt.year
    df['bulan'] = df['tanggal_nabung'].dt.month
    df['nama_bulan'] = df['tanggal_nabung'].dt.strftime('%b')
    df['hari_minggu'] = df['tanggal_nabung'].dt.dayofweek
    df['tipe_hari'] = df['hari_minggu'].apply(lambda x: 'Akhir Pekan' if x >= 5 else 'Hari Kerja')
    return df

# df menjadi variabel global
df = load_data_regresi()

# Hapus (df) dari sini, cukup kurung kosong ()
def tampilan_regresi():

    # Title
    st.title("Dashboard Analytics Regresi Tabungan")

    # --- 1. RINGKASAN KEUANGAN (KPI) ---
    st.subheader("Ringkasan Keuangan")
    col1, col2 = st.columns(2)

    with col1:
        total_tabungan = df['target_nominal'].sum()
        st.metric("Total Target Tabungan",f"Rp {total_tabungan:,.0f}")

    with col2:
        jumlah_transaksi = len(df)
        st.metric("Jumlah Transaksi",f"{jumlah_transaksi:,} Transaksi")
        

    st.markdown("---")
    
    # --- 4. VISUALISASI FREKUENSI ---
    st.subheader("Analisis Frekuensi Menabung")
    
    col_freq1, col_freq2 = st.columns(2)
    
    with col_freq1:
        st.write("**Frekuensi Transaksi per Bulan**")
        

        freq_bulan = df.groupby(['bulan', 'nama_bulan']).size().reset_index(name='jumlah_transaksi')
        freq_bulan = freq_bulan.sort_values('bulan')
        
        transaksi_terbanyak = freq_bulan['jumlah_transaksi'].max()
        
        warna_bulan = ['#f59e0b' if val == transaksi_terbanyak else '#8b5cf6' for val in freq_bulan['jumlah_transaksi']]
        
        fig_bar = px.bar(
            freq_bulan, 
            x='nama_bulan', 
            y='jumlah_transaksi',
            text_auto=True, 
            title="Jumlah Transaksi Berdasarkan Bulan",
            labels={'nama_bulan': 'Bulan', 'jumlah_transaksi': 'Jumlah Transaksi'},)
        
        fig_bar.update_traces(marker_color=warna_bulan, textposition='outside')
        fig_bar.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_freq2:
        st.write("**Total Nominal Nabung per Bulan**")
        
        nominal_bulan = df.groupby(['bulan', 'nama_bulan'])['nominal_nabung'].sum().reset_index(name='total_nominal')
        nominal_bulan = nominal_bulan.sort_values(by='bulan')
        nominal_bulan['teks_display'] = nominal_bulan['total_nominal'].apply(lambda x: f"Rp {x:,.0f}")
        nilai_tertinggi = nominal_bulan['total_nominal'].max()
        
        warna_bar = ['#f59e0b' if val == nilai_tertinggi else '#10b981' for val in nominal_bulan['total_nominal']]
        fig_bar_bulan = px.bar(
            nominal_bulan, 
            x='nama_bulan', 
            y='total_nominal',
            text='teks_display', 
            title="Total Nominal Tabungan Setiap Bulan",
            labels={'nama_bulan': 'Bulan', 'total_nominal': 'Total Uang (Rp)'})

        fig_bar_bulan.update_traces(marker_color=warna_bar, textposition='outside')
        
        fig_bar_bulan.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        
        st.plotly_chart(fig_bar_bulan, use_container_width=True)
        
    st.markdown("---")    
    
    tab1,tab2,tab4 = st.tabs(['EDA' , 'Visualisasi Pertanyaan Bisnis' , 'Data'])

    # ==========================================
    # TAB 1: EDA 
    # ==========================================
    with tab1:
        # Membuat Sub-Tabs di dalam Tab EDA
        sub_tab1, sub_tab2, sub_tab3 = st.tabs([
            "Overview ", 
            "Segmentasi Pengguna", 
            "Distribusi & Outlier"
        ])
        
        # --- SUB-TAB 1: OVERVIEW  ---
        with sub_tab1:
            st.subheader("🎯 Ketercapaian Target Tabungan")
            total_target_keseluruhan = df['target_nominal'].sum()
            total_sisa_keseluruhan = df['sisa_target'].sum()
            persentase_sisa = (total_sisa_keseluruhan / total_target_keseluruhan) * 100 if total_target_keseluruhan > 0 else 0
            persentase_sisa = max(0, min(100, persentase_sisa))
            
            col_prog, _ = st.columns([1, 1])
            with col_prog:
                st.metric("Sisa Target Dari Total Tabungan", f"{persentase_sisa:.2f}%")
                st.progress(int(persentase_sisa))
                st.caption("Menunjukkan total kekurangan dana dibandingkan dengan Total Target keseluruhan.")
                
            st.subheader("Insight Exploratory Data Analysis")
            col_eda1, col_eda2 = st.columns(2)
        
            with col_eda1:
                st.markdown("""
                **1. Distribusi Skewed & Outlier Besar**
                - Distribusi data sangat *skewed* ke kanan. Mayoritas user menabung dengan nominal kecil, namun terdapat outlier ekstrem dengan setoran hingga miliaran rupiah.
                - Contoh: Median nominal setoran hanya **Rp 88.321**, namun rata-ratanya tertarik ke angka **Rp 4.545.024** (akibat outlier ekstrem hingga Rp 8,4 Miliar).
                
                **2. Kesenjangan Progress (Gap)**
                - Terdapat gap besar antar pengguna. Sebagian besar masih memiliki sisa target yang relatif kecil (< Rp 500 ribu), namun ada segelintir user yang masih harus mengejar target miliaran.
                """)
            
            with col_eda2:
                st.markdown("""
                **3. Analisis Frekuensi Menabung**
                - Mayoritas user (berdasarkan median) hanya tercatat menabung **1 kali**.
                - Rata-rata frekuensi menabung mencapai **33 kali** per tujuan, menandakan adanya kelompok kecil user yang sangat konsisten, sementara mayoritas pasif.
                
                **4. Distribusi Waktu (Tahun)**
                - Rentang data dimulai dari 4 Agustus 2019 hingga 31 Desember 2024.
                - Puncak frekuensi jumlah transaksi tabungan terbanyak terjadi pada tahun **2023**.
                """)

        # --- SUB-TAB 2: SEGMENTASI PENGGUNA ---
        with sub_tab2:
            st.subheader("Kategori User Berdasarkan Kasta Keuangan")
            
            def get_segment(target):
                if target <= 1000000:
                    return 'Micro (<=1Jt)'
                elif target <= 10000000:
                    return 'Small (1-10Jt)'
                elif target <= 100000000:
                    return 'Medium (10-100Jt)'
                else:
                    return 'Sultan (>100Jt)'
                    
            df_segment = df.copy()
            df_segment['user_segment'] = df_segment['target_nominal'].apply(get_segment)
            segment_counts = df_segment['user_segment'].value_counts().reset_index()
            segment_counts.columns = ['Segmen', 'Jumlah']
            
            col_segmen_grafik, col_segmen_text = st.columns([1.2, 1])
            
            with col_segmen_grafik:
                fig_pie_segmen = px.pie(
                    segment_counts, names='Segmen', values='Jumlah', 
                    hole=0.4, 
                    color_discrete_sequence=['#4e79a7', '#f28e2b', '#e15759', '#76b7b2']
                )
                fig_pie_segmen.update_layout(margin=dict(t=10, b=0, l=0, r=0))
                st.plotly_chart(fig_pie_segmen, use_container_width=True)
                
            with col_segmen_text:
                st.markdown("""
                **Insight Kategori User:**
                - **Dominasi Kelas Finansial:** Pembagian kelompok ini membantu model memahami profil risiko dan kebiasaan menabung berdasarkan target nominalnya.
                - **Aktivitas Transaksi:** Mayoritas catatan data bertumpu pada segmen tertentu, yang memperlihatkan adanya variasi motivasi menabung yang kontras di dalam aplikasi.
                - **Intensitas Tabungan:** Berdasarkan data frekuensi, sebagian besar user memiliki median transaksi sebanyak **1 kali**, mengindikasikan banyak akun yang belum konsisten memanfaatkan fitur goals jangka panjang.
                """)

        # --- SUB-TAB 3: DISTRIBUSI & OUTLIER ---
        with sub_tab3:
            st.subheader("Analisis Sebaran Variabel Finansial")
            
            col_box_grafik, col_box_text = st.columns([1.2, 1])
            
            with col_box_grafik:
                df_box = df.copy()
                df_box['Log Target Nominal'] = np.log1p(df_box['target_nominal'])
                
                fig_box = px.box(
                    df_box, y='Log Target Nominal', 
                    color_discrete_sequence=['#8b5cf6'],
                    points="all"
                )
                fig_box.update_layout(margin=dict(t=10, b=0, l=0, r=0))
                st.plotly_chart(fig_box, use_container_width=True)
                
            with col_box_text:
                st.markdown("""
                **Insight Distribusi & Outlier:**
                - **Right-Skewed Data:** Data nominal transaksi dan target tabungan riil memiliki sebaran awal yang sangat miring (*right-skewed*) dengan rentang ekstrem dari Rp 5.000 hingga Rp 9 Miliar.
                - **Distorsi Nilai Tengah:** Kondisi pencilan (*outlier*) atas ini terlihat dari nilai rata-rata (*mean*) setoran sebesar **Rp 4.545.024**, padahal nilai tengah (*median*) riil mayoritas pengguna berada jauh di bawahnya, yaitu **Rp 88.321**.
                - **Urgensi Skala Log:** Grafik *boxplot* di samping membuktikan perlunya penerapan transformasi logaritma (`log1p`) untuk menstabilkan varians variabel keuangan sebelum diproses oleh algoritma regresi.
                """)
    # ==========================================
    # TAB 2: VISUALISASI PERTANYAAN BISNIS
    # ==========================================
    with tab2:
        st.subheader("Menjawab Pertanyaan Bisnis")
        col_pertanyaan1, col_pertanyaan2 = st.columns(2)
        
        # Pertanyaan 1 
        with col_pertanyaan1:
            st.write("**1. Bagaimana perbandingan rata-rata nominal yang ditabung saat Hari Kerja vs Akhir Pekan?**")
            
            # Hitung log1p ulang untuk memastikan data yang digunakan sudah dalam bentuk logaritma (meskipun sudah dilakukan di fungsi load_data, ini untuk memastikan jika ada perubahan)
            df_temp_log = df.copy()
            df_temp_log['log_nominal'] = np.log1p(df_temp_log['nominal_nabung'])
            rata_hari_log = df_temp_log.groupby('tipe_hari')['log_nominal'].mean().reset_index()
            
            fig_hari = px.bar(
                rata_hari_log, x='tipe_hari', y='log_nominal', text_auto='.5f', color='tipe_hari',
                color_discrete_sequence=['#3b82f6', '#10b981'],
                labels={'tipe_hari': 'Tipe Hari', 'log_nominal': 'Rata-rata Nominal (Log)'}
            )
            fig_hari.update_layout(margin=dict(t=30, b=0, l=0, r=0), showlegend=False)
            st.plotly_chart(fig_hari, use_container_width=True)
            
            val_hk = rata_hari_log[rata_hari_log['tipe_hari'] == 'Hari Kerja']['log_nominal'].values[0]
            val_hl = rata_hari_log[rata_hari_log['tipe_hari'] == 'Akhir Pekan']['log_nominal'].values[0]
            
            # Kotak Insight persis gambar
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                <h4 style="margin-top: 0; color: #31333F;">Insight & Kesimpulan :</h4>
                <ul style="color: #31333F; margin-bottom: 0;">
                    <li>Hari Kerja memiliki rata-rata nominal tabungan sebesar {val_hk:.5f}</li>
                    <li>Akhir Pekan memiliki rata-rata nominal tabungan sebesar {val_hl:.5f}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Pertanyaan 2 
        with col_pertanyaan2:
            st.write("**2. Apakah User Segment (Kasta Keuangan) mempengaruhi konsistensi mencapai target?**")
            
            # Melakukan segmentasi (Micro/Small/Medium diringkas ke Low/Medium vs Sultan ke High) berdasarkan notebook
            df_wealth = df.copy()
            df_wealth['is_success'] = (df_wealth['sisa_target'] <= 0).astype(int)
            df_wealth['wealth_segment'] = pd.cut(
                df_wealth['target_nominal'], 
                bins=[-1, 10000000, float('inf')], 
                labels=['Low & Medium Wealth', 'High Wealth']
            )
            
            success_rate = df_wealth.groupby('wealth_segment')['is_success'].mean() * 100
            success_rate = success_rate.reset_index()
            
            fig_wealth = px.bar(
                success_rate, x='wealth_segment', y='is_success', text_auto='.1f', color='wealth_segment',
                color_discrete_sequence=['#f59e0b', '#8b5cf6'],
                labels={'wealth_segment': 'Segmen Pengguna', 'is_success': 'Success Rate (%)'}
            )
            fig_wealth.update_layout(margin=dict(t=30, b=0, l=0, r=0), showlegend=False)
            st.plotly_chart(fig_wealth, use_container_width=True)
            
            st.markdown("""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                <h4 style="margin-top: 0; color: #31333F;">Insight & Kesimpulan :</h4>
                <ul style="color: #31333F; margin-bottom: 0;">
                    <li><b>Low & Medium Wealth:</b> Tidak ada data keberhasilan di bulan terakhir (indikasi aktivitas sangat pasif).</li>
                    <li><b>High Wealth:</b> Meski kecil, kelompok ini mencatatkan tingkat keberhasilan target (Success Rate sekitar 2%).</li>
                    <li><b>Ya</b>, User Segment mempengaruhi konsistensi mencapai Target Tabungan.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # TAB 4: DATA
    # ==========================================
    with tab4:
        st.subheader("Tinjauan Dataset (Cleaned)")
        st.write("Tabel di bawah menampilkan data tabungan bersih yang nilai logaritma-nya telah dikembalikan (*inverse*) menjadi Rupiah.")
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    tampilan_regresi() 