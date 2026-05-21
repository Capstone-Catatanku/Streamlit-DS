import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from scipy import stats
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# load data
@st.cache_data
def load_data_klasifikasi() :
    url = "https://raw.githubusercontent.com/Capstone-Catatanku/Data-Science/refs/heads/main/Data-clean/Data-clean.csv"
    df = pd.read_csv(url)
    df['tanggal'] =  pd.to_datetime(df['tanggal'])   
    df['tahun'] = df['tanggal'].dt.year
    df['bulan'] = df['tanggal'].dt.month
    df['nama_bulan'] = df['tanggal'].dt.strftime('%b')
    df['hari_minggu'] = df['tanggal'].dt.dayofweek
    df['tipe_hari'] = df['hari_minggu'].apply(lambda x: 'Akhir Pekan' if x >= 5 else 'Hari Kerja')
    return df

df = load_data_klasifikasi()


def tampilkan_dashboard():
    # Ini widget bawaan Streamlit
    st.title("Dashboard Analytics Klasifkasi Pengeluaran")

    # Metric Pengeluaran
    st.subheader("Ringkasan Keuangan")
    col1,col2 = st.columns(2)
    
    with col1:
        total_pengeluaran = df['nominal'].sum()
        st.metric("Total Pengeluaran" , f'Rp {total_pengeluaran:,.0f}')
    with col2:
        jumlah_transaksi = len(df)
        st.metric("Jumlah Transaksi" , f'{jumlah_transaksi:,} Transaksi')

    # Top Singko Kategori Pengeluaran
    col1 , col2 = st.columns(2)

    with col1 :
        st.subheader("Top 5 Kategori Pengeluaran")
        top_kategori = df.groupby('kategori')['nominal'].sum().sort_values(ascending=False).head(5)

        fig, ax = plt.subplots(figsize=(10,5))
        top_kategori.plot(kind='barh' , color='#ff6b6b' , ax=ax)
        ax.set_xlabel("Total Pengeluaran (Scaled)")
        ax.set_title('Top 5 Kategori Pengeluaran')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Pengeluaran Per Tahun")
        bulanan = df.groupby(df['tanggal'].dt.to_period('Y'))['nominal'].sum()
        bulanan.index = bulanan.index.astype(str)

        fig, ax = plt.subplots(figsize=(10, 5))
        bulanan.plot(kind='line', marker='o', color='#3498db', ax=ax)
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Total Pengeluaran (Scaled)')
        ax.set_title('Tren Pengeluaran per Tahun')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    
    st.markdown('---')

    tab1,tab2,tab3,tab5 = st.tabs(['EDA' , 'Visualisasi Pertanyaan Bisnis','A/B Testing' , 'Data'])

    # Tab 1 - EDA
    with tab1:
        st.header("Exploratory Data Analysis")

        subtab1,subtab2,subtab3,subtab4= st.tabs(['Nominal' , 'Kategori' , 'Waktu' , 'Outlier'])

        with subtab1:
            st.subheader("Distribusi Nominal Transaksi")
            fig,ax = plt.subplots(figsize=(12,5))
            df['nominal'].hist(bins=50 ,  color='#3498db', edgecolor='black', ax=ax)
            ax.axvline(df['nominal'].mean(), color='red', linestyle='--', label=f'Mean: Rp {df["nominal"].mean():,.0f}')
            ax.axvline(df['nominal'].median(), color='green', linestyle='--', label=f'Median: Rp {df["nominal"].median():,.0f}')
            ax.set_xlabel('Nominal (Scaled)')
            ax.set_ylabel('Frekuensi')
            ax.set_title('Histogram Distribusi Nominal')
            ax.legend()
            st.pyplot(fig)
        
            st.write("**Interpretasi:**")
            if df['nominal'].mean() > df['nominal'].median():
                st.write("Distribusi skew ke kanan, Ada outlier besar yang menarik rata-rata ke atas")
            else:
                st.write(" Distribusi relatif simetris")

        with subtab2 :
            st.subheader("Perbandingan per Kategori")
        
            # Statistik per kategori
            st.write("**Statistik per Kategori:**")
            stat_kategori = df.groupby('kategori')['nominal'].agg(['count', 'mean', 'median', 'sum']).round(0)
            stat_kategori.columns = ['Jumlah', 'Rata-rata', 'Median', 'Total']
            stat_kategori['Rata-rata'] = stat_kategori['Rata-rata'].apply(lambda x: f"Rp {x:,.0f}")
            stat_kategori['Median'] = stat_kategori['Median'].apply(lambda x: f"Rp {x:,.0f}")
            stat_kategori['Total'] = stat_kategori['Total'].apply(lambda x: f"Rp {x:,.0f}")
            st.dataframe(stat_kategori, use_container_width=True)

            #plot 2 distribusi
            kategori_total = df.groupby('kategori')['nominal'].sum().sort_values(ascending=False)
            total_semua = kategori_total.sum()

            kategori_persen = (kategori_total / total_semua * 100).round(1)

            kategori_persen_clean = kategori_persen.copy()
            kategori_persen_clean['Lain-lain'] = kategori_persen_clean[kategori_persen_clean < 1].sum()
            kategori_persen_clean = kategori_persen_clean[kategori_persen_clean >= 1]
            kategori_persen_clean = kategori_persen_clean.sort_values(ascending=False)

            kategori_pie_counts = kategori_persen_clean

            explode = [0.1 if i < 3 else 0 for i in range(len(kategori_pie_counts))]
            colors = sns.color_palette('pastel')[0:len(kategori_pie_counts)]

            fig,ax = plt.subplots(figsize=(6,6))

            def autopct_format(pct):
                return ('%1.1f%%' % pct) if pct >= 1 else ''

            wedges, texts, autotexts = ax.pie(
                kategori_pie_counts,
                labels=None,  
                autopct=autopct_format,
                startangle=140,
                colors=colors,
                explode=explode,
                shadow=False,
                textprops={'fontsize': 12},
                pctdistance=0.7,   
            )

            ax.legend(
                wedges,
                kategori_pie_counts.index,
                title="Kategori",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1),
                fontsize=12
            )

            ax.text(
                x=1, y=1, 
                s="<1% tidak di tampilkan", 
                fontsize=12, color="red", 
                ha="center", va="center", 
                bbox=dict(facecolor="yellow", alpha=0.3, edgecolor="black")
                )

            ax.set_title('Proporsi Penyebaran Kategori (Pie Chart)', fontsize=16, fontweight='bold')
            st.pyplot(fig)

            with st.expander("Lihat Detail Persentase per Kategori", expanded=False):
                st.markdown("### Persentase Eksak per Kategori")
                st.markdown("<1% tidak ditampilkan di pie chart, tapi berikut adalah data lengkapnya:", unsafe_allow_html=True)
                st.write("")
    
                detail_df = pd.DataFrame({
                'Kategori': kategori_persen.index,
                'Total (Rp)': [f"Rp {val:,.0f}" for val in kategori_total.values],
                'Persentase': [f"{val:.2f}%" for val in kategori_persen.values]
                })

                st.dataframe(detail_df, use_container_width=True, hide_index=True)
        with subtab3:
            st.subheader("Tren Waktu")
        
            # Pilih agregasi: bulanan atau tahunan
            agg_level = st.selectbox("Pilih Level Agregasi", ["Bulanan", "Tahunan"])
        
            if agg_level == "Bulanan":
                trend_data = df.groupby(df['tanggal'].dt.to_period('M'))['nominal'].sum()
                trend_data.index = trend_data.index.astype(str)
                xlabel = "Bulan"
            else:
                trend_data = df.groupby(df['tanggal'].dt.year)['nominal'].sum()
                xlabel = "Tahun"
        
            fig, ax = plt.subplots(figsize=(12, 5))
            trend_data.plot(kind='bar', color='#3498db', edgecolor='black', ax=ax)
            ax.set_xlabel(xlabel)
            ax.set_ylabel('Total Pengeluaran (Rp)')
            ax.set_title(f'Tren Pengeluaran {agg_level}')
            st.pyplot(fig)
        
            # Weekday vs Weekend
            st.subheader("Hari Kerja vs Akhir Pekan")
        
            weekday_weekend = df.groupby('tipe_hari')['nominal'].mean()
        
            fig, ax = plt.subplots(figsize=(8, 5))
            weekday_weekend.plot(kind='bar', color=['#3498db', '#e74c3c'], edgecolor='black', ax=ax)
            ax.set_ylabel('Rata-rata Nominal (Rp)')
            ax.set_title('Perbandingan Rata-rata: Hari Kerja vs Akhir Pekan')
            for i, val in enumerate(weekday_weekend.values):
                ax.text(i, val + 1000, f'Rp {val:,.0f}', ha='center')
            st.pyplot(fig)

        with subtab4 :
            st.subheader("Deteksi Outlier")
        
            if len(df) > 0:
            # Metode outlier
                metode = st.selectbox("Metode Deteksi Outlier", ["IQR (1.5x)", "2 Standar Deviasi"])
            
                if metode == "IQR (1.5x)":
                    Q1 = df['nominal'].quantile(0.25)
                    Q3 = df['nominal'].quantile(0.75)
                    IQR = Q3 - Q1
                    batas_atas = Q3 + 1.5 * IQR
                    outliers = df[df['nominal'] > batas_atas]
                else:
                    mean = df['nominal'].mean()
                    std = df['nominal'].std()
                    batas_atas = mean + 2 * std
                    outliers = df[df['nominal'] > batas_atas]
            
                st.write(f"**Jumlah Outlier:** {len(outliers)} transaksi ({len(outliers)/len(df)*100:.1f}%)")
                st.write(f"**Total Nilai Outlier:** Rp {outliers['nominal'].sum():,.0f}")
            
                if len(outliers) > 0:
                    st.write("**Daftar Outlier (Top 10):**")
                    st.dataframe(outliers[['tanggal', 'deskripsi_transaksi', 'kategori', 'nominal']].head(10),use_container_width=True)
            else:
                st.warning("Tidak ada data untuk rentang yang dipilih")
    
    # tab 2 - A/B Testing
    with tab3 :
        st.header("A/B Testing")
        # st.info(f"📊 Data A/B Testing: **{ab_start if use_custom_range else start_date}** s/d **{ab_end if use_custom_range else end_date}**")
        skenario = st.selectbox(
        "Pilih Skenario A/B Test",
            [
                "Berbelanja di weekdays lebih hemat daripada weekend",
                "Rata-rata transaksi Belanja lebih besar dari Makanan"
            ]
        )

        if skenario == "Berbelanja di weekdays lebih hemat daripada weekend":
            st.subheader("Hipotesis: Berbelanja di weekdays lebih hemat daripada weekend")
            
            if len(df) > 0:
                group_a = df[df['tipe_hari'] == 'Hari Kerja']['nominal']
                group_b = df[df['tipe_hari'] == 'Akhir Pekan']['nominal']

                st.write(f"**Kelompok A (Hari Kerja):** n = {len(group_a)}, mean = Rp {group_a.mean():,.0f}")
                st.write(f"**Kelompok B (Akhir Pekan):** n = {len(group_b)}, mean = Rp {group_b.mean():,.0f}")
                
                if len(group_a) > 0 and len(group_b) > 0:
                    t_stat, p_value = stats.ttest_ind(group_a, group_b)
                    st.write("---")
                    st.subheader("Hasil Uji Statistik")

                    col1,col2,col3 = st.columns(3)

                    with col1:
                        st.metric("T-Statistic" , f'{t_stat:.4f}')
                    with col2:
                        st.metric("P-Value" , f'{p_value:.4f}')
                    with col3:
                        from numpy import std,mean, sqrt
                        n1,n2 = len(group_a), len(group_b)
                        s1, s2 = group_a.std() , group_b.std()
                        s_pooled = sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
                        cohens_d = (group_b.mean() - group_a.mean()) / s_pooled if s_pooled > 0 else 0
                        st.metric("Cohen's d" , f'{abs(cohens_d):.4f}')

                    st.subheader("Interpretasi")
                    if p_value < 0.05:
                        st.success(f'Signifikan (p = {p_value:.4f} < 0.05)')

                        if group_b.mean() > group_a.mean():
                            selisih = (group_b.mean() - group_a.mean()) / group_a.mean() * 100
                            st.write(f"→ Akhir pekan Lebih Besar {selisih:.1f}% dari hari kerja")
                            st.write("→ **Rekomendasi:** Batasi aktivitas berbayar di akhir pekan")
                        else :
                            st.write("Hari kerja lebih besar dari akhir pekan")
                    else:
                        st.warning(f" Tidak signifikan (p = {p_value:.4f} >= 0.05)")
                        st.write("Belum ada bukti cukup bahwa ada perbedaan")

        elif skenario == "Rata-rata transaksi Belanja lebih besar dari Makanan" :
            st.subheader("Hipotesis : Rata-rata transaksi Belanja lebih besar dari Makanan")

            if len(df) > 0:
                group_a = df[df['kategori'] == 'Konsumsi']['nominal']
                group_b = df[df['kategori'] == 'Belanja']['nominal']

                st.write(f"**Kelompok A (Makanan):** n = {len(group_a)}, mean = Rp {group_a.mean():,.0f}")
                st.write(f"**Kelompok B (Belanja):** n = {len(group_b)}, mean = Rp {group_b.mean():,.0f}")

                if len(group_a) > 0 and len(group_b) > 0:
                    t_stat, p_value = stats.ttest_ind(group_a, group_b)
                    st.write("---")
                    st.subheader("Hasil Uji Statistik")

                    col1,col2,col3 = st.columns(3)

                    with col1:
                        st.metric("T-Statistic" , f'{t_stat:.4f}')
                    with col2:
                        st.metric("P-Value" , f'{p_value:.4f}')
                    with col3:
                        from numpy import std,mean, sqrt
                        n1,n2 = len(group_a), len(group_b)
                        s1, s2 = group_a.std() , group_b.std()
                        s_pooled = sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
                        cohens_d = (group_b.mean() - group_a.mean()) / s_pooled if s_pooled > 0 else 0
                        st.metric("Cohen's d" , f'{abs(cohens_d):.4f}')
                    
                    st.subheader("Interpretasi")
                    if p_value < 0.05:
                        st.success(f'Signifikan (p = {p_value:.4f} < 0.05)')

                        if group_b.mean() > group_a.mean():
                            selisih = (group_b.mean() - group_a.mean()) / group_a.mean() * 100
                            st.write(f"Belanja Lebih Besar {selisih:.1f}% dari Makanan")
                            st.write("**Rekomendasi:** Evaluasi Setiap Pembelian Di Kategori Belanja")
                        else :
                            st.write("Makanan lebih besar dari belanja")
                    else:
                        st.warning(f" Tidak signifikan (p = {p_value:.4f} >= 0.05)")
                        st.write("Belum ada bukti cukup bahwa Belanja dan Makanan berbeda")

    with tab5:
        st.header("Data Transaksi")

        csv = df.to_csv(index=False)
        st.download_button('Download Dataset (CSV)' , csv , 'data_keuangan.csv' , 'text/csv')
        st.dataframe(df , use_container_width=True)


    with tab2:
        st.header("Visualisasi Pertanyaan Bisnis")
    
        st.markdown("""
            Berikut adalah visualisasi yang menjawab **3 pertanyaan bisnis** utama:
            1. Di bulan apa total pengeluaran tertinggi?
            2. Apakah akhir pekan lebih boros dari hari kerja?
            3. Berapa total kerugian dari transaksi outlier?
            """)
    
        st.markdown("---")
    
        st.subheader("Pertanyaan #1: Bulan dengan Total Pengeluaran Tertinggi")
        st.markdown("*Di bulan apa total pengeluaran tertinggi terjadi dalam dua tahun terakhir?*")
    
        # Filter 2 tahun terakhir
        df_2tahun = df[df['tahun'].isin([2023, 2024])].copy()
    
        if len(df_2tahun) > 0:
            # Agregasi per bulan
            monthly = df_2tahun.groupby(df_2tahun['tanggal'].dt.to_period('M'))['nominal'].sum()
            monthly.index = monthly.index.astype(str)
        
            # Cari bulan tertinggi
            max_month = monthly.idxmax()
            max_value = monthly.max()
        
            # Visualisasi
            fig, ax = plt.subplots(figsize=(14, 6))
        
            # Bar chart dengan warna berbeda untuk bulan tertinggi
            colors_bar = ['#e74c3c' if idx == max_month else '#3498db' for idx in monthly.index]
            bars = ax.bar(monthly.index, monthly.values, color=colors_bar, edgecolor='black')
        
            # Tambahkan label nilai di atas bar
            for bar, val in zip(bars, monthly.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000, f'Rp {val/1_000_000:.1f}jt', ha='center', fontsize=8, rotation=45)
        
        # Sorot bulan tertinggi
            ax.scatter(monthly.index.get_loc(max_month), max_value, color='darkred', s=200, zorder=5,marker='*', edgecolor='black', linewidth=1)
        
            ax.axhline(y=monthly.median(), color='orange', linestyle='--', label=f'Median: Rp {monthly.median()/1_000_000:.1f}jt')
        
            ax.set_title(f'Total Pengeluaran per Bulan (2023-2024)\n📍 Tertinggi: {max_month} (Rp {max_value/1_000_000:.1f} juta)', fontsize=14, fontweight='bold')
            ax.set_xlabel('Periode (Tahun-Bulan)', fontsize=12)
            ax.set_ylabel('Total Pengeluaran (Rp)', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
            plt.tight_layout()
            st.pyplot(fig)
        
        # Insight
            with st.expander("Insight Pertanyaan #1", expanded=False):
                st.write(f"**Bulan dengan pengeluaran tertinggi:** {max_month}")
                st.write(f"**Total pengeluaran:** Rp {max_value:,.0f}")
                st.write(f"**Selisih dengan bulan kedua tertinggi:** Rp {(max_value - monthly.nlargest(2).iloc[1]):,.0f}")
            
                if max_month.endswith('12'):
                    st.info("**Rekomendasi:** Puncak pengeluaran terjadi di AKHIR TAHUN. Sisihkan uang lebih banyak mulai November.")
                elif max_month.endswith('06'):
                    st.info("**Rekomendasi:** Puncak pengeluaran terjadi di PERTENGAHAN TAHUN. Antisipasi dengan anggaran khusus.")
                else:
                    st.info("**Rekomendasi:** Evaluasi apa yang menyebabkan lonjakan di bulan tersebut.")
    
        st.markdown("---")

        # Pertanyaan 2
    
        st.subheader("Pertanyaan #2: Hari Kerja vs Akhir Pekan")
        st.markdown("*Apakah rata-rata pengeluaran di akhir pekan lebih besar dari hari kerja?*")
    
        enam_bulan_lalu = df['tanggal'].max() - timedelta(days=180)
        df_6bln = df[df['tanggal'] >= enam_bulan_lalu].copy()
    
        if len(df_6bln) > 0:
            # Hitung rata-rata per tipe hari
            weekday_weekend = df_6bln.groupby('tipe_hari')['nominal'].mean()
        
            # Hitung kategori penyebab
            kategori_hari = df_6bln.groupby(['kategori', 'tipe_hari'])['nominal'].sum().unstack(fill_value=0)
            kategori_hari['selisih'] = kategori_hari['Akhir Pekan'] - kategori_hari['Hari Kerja']
            top_penyebab = kategori_hari.sort_values('selisih', ascending=False).head(5)
        
            # Visualisasi 1: Bar chart perbandingan
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
            # Plot A: Bar chart rata-rata
            colors_bar = ['#3498db', '#e74c3c']
            bars = axes[0].bar(weekday_weekend.index, weekday_weekend.values, color=colors_bar, edgecolor='black')
            axes[0].set_title('Rata-rata Pengeluaran per Transaksi', fontsize=12, fontweight='bold')
            axes[0].set_ylabel('Rata-rata Nominal (Rp)', fontsize=11)
        
            for bar, val in zip(bars, weekday_weekend.values):
                axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000, f'Rp {val:,.0f}', ha='center', fontsize=10, fontweight='bold')
        
            # Plot B: Top kategori penyebab
            if len(top_penyebab) > 0:
                x = range(len(top_penyebab))
                width = 0.35
            
                axes[1].bar([i - width/2 for i in x], top_penyebab['Hari Kerja'], width, label='Hari Kerja', color='#3498db', edgecolor='black')
                axes[1].bar([i + width/2 for i in x], top_penyebab['Akhir Pekan'], width, label='Akhir Pekan', color='#e74c3c', edgecolor='black')
                axes[1].set_xticks(x)
                axes[1].set_xticklabels(top_penyebab.index, rotation=45, ha='right')
                axes[1].set_title('Top 5 Kategori Penyebab Perbedaan', fontsize=12, fontweight='bold')
                axes[1].set_ylabel('Total Pengeluaran (Rp)', fontsize=11)
                axes[1].legend()
        
            plt.tight_layout()
            st.pyplot(fig)
        
        # Insight
            with st.expander("Insight Pertanyaan #2", expanded=False):
                selisih = weekday_weekend.get('Akhir Pekan', 0) - weekday_weekend.get('Hari Kerja', 0)
                persen_selisih = abs(selisih / weekday_weekend.get('Hari Kerja', 1) * 100)
            
                st.write(f"**Hari Kerja:** Rp {weekday_weekend.get('Hari Kerja', 0):,.0f}")
                st.write(f"**Akhir Pekan:** Rp {weekday_weekend.get('Akhir Pekan', 0):,.0f}")
                st.write(f"**Selisih:** {persen_selisih:.1f}% {'Lebih Besar' if selisih > 0 else 'Lebih Kecil'} di akhir pekan")
            
                if len(top_penyebab) > 0:
                    st.write(f"\n**Kategori penyebab terbesar:** {top_penyebab.index[0]}")
                    st.write(f"Selisih: Rp {top_penyebab.iloc[0]['selisih']:,.0f}")
            
                if selisih > 0:
                    st.info("**Rekomendasi:** Batasi aktivitas berbayar di akhir pekan. Cari alternatif hiburan gratis.")
                else:
                    st.info("**Rekomendasi:** Pola pengeluaran Anda sudah baik, pertahankan!")
    
        st.markdown("---")
    
        st.subheader("Pertanyaan #3: Analisis Outlier")
        st.markdown("*Berapa total kerugian dari transaksi outlier dan berapa yang bisa dicegah?*")
    
        # Filter 1 tahun terakhir
        satu_tahun_lalu = df['tanggal'].max() - timedelta(days=365)
        df_1thn = df[df['tanggal'] >= satu_tahun_lalu].copy()
    
        if len(df_1thn) > 0:
            # Deteksi outlier (IQR method)
            Q1 = df_1thn['nominal'].quantile(0.25)
            Q3 = df_1thn['nominal'].quantile(0.75)
            IQR = Q3 - Q1
            batas_atas = Q3 + 1.5 * IQR
        
            outliers = df_1thn[df_1thn['nominal'] > batas_atas]
        
            # Outlier yang bisa dicegah (Belanja > 500rb)
            bisa_dicegah = outliers[(outliers['kategori'] == 'Belanja') & (outliers['nominal'] > 500000)]
            total_bisa_dicegah = bisa_dicegah['nominal'].sum()
            total_outlier = outliers['nominal'].sum()
            persen_bisa_dicegah = (total_bisa_dicegah / total_outlier * 100) if total_outlier > 0 else 0
        
            # Visualisasi
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
            # Plot A: Outlier per bulan
            outlier_bulanan = outliers.groupby(outliers['tanggal'].dt.to_period('M'))['nominal'].sum()
            outlier_bulanan.index = outlier_bulanan.index.astype(str)
        
            axes[0].bar(outlier_bulanan.index, outlier_bulanan.values, color='#e74c3c', edgecolor='black')
            axes[0].set_title('Total Nilai Outlier per Bulan', fontsize=12, fontweight='bold')
            axes[0].set_xlabel('Bulan', fontsize=11)
            axes[0].set_ylabel('Total Outlier (Rp)', fontsize=11)
            axes[0].tick_params(axis='x', rotation=45)
        
            # Plot B: Pie chart potensi penghematan
            sizes = [total_bisa_dicegah, total_outlier - total_bisa_dicegah]
            labels = [f'Bisa Dicegah\nRp {total_bisa_dicegah/1_000_000:.1f}jt', f'Sulit Dicegah\nRp {(total_outlier - total_bisa_dicegah)/1_000_000:.1f}jt']
            colors_pie = ['#2ecc71', '#e74c3c']
            explode = (0.05, 0)
        
            axes[1].pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90, explode=explode)
            axes[1].set_title(f'Potensi Penghematan (Kebijakan Tunggu 3 Hari)', fontsize=12, fontweight='bold')
        
            plt.tight_layout()
            st.pyplot(fig)
        
            # Insight
            with st.expander("Insight Pertanyaan #3", expanded=False):
                st.write(f"**Total outlier (1 tahun):** Rp {total_outlier:,.0f}")
                st.write(f"**Jumlah transaksi outlier:** {len(outliers)} transaksi")
                st.write(f"**Total yang BISA dicegah:** Rp {total_bisa_dicegah:,.0f} ({persen_bisa_dicegah:.1f}%)")
            
                if len(bisa_dicegah) > 0:
                    st.write("\n**Daftar transaksi prioritas yang bisa dicegah:**")
                    st.dataframe(bisa_dicegah[['tanggal', 'deskripsi_transaksi', 'nominal']].head(5), use_container_width=True, hide_index=True)
            
                if persen_bisa_dicegah > 30:
                    st.success(f"**Rekomendasi:** Terapkan aturan 'tunggu 3 hari' untuk pembelian >Rp500rb di kategori Belanja. Potensi hemat Rp {total_bisa_dicegah:,.0f}/tahun.")
                else:
                    st.info("**Rekomendasi:** Outlier dominan dari kategori selain Belanja. Perlu investigasi lebih lanjut.")
    

if __name__ == "__main__":
    tampilkan_dashboard()