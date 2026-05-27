import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data_regresi():

    url = "https://raw.githubusercontent.com/Capstone-Catatanku/Data-Science-Tabungan/refs/heads/main/Clean-data/Data_Progressive_Clean.csv"

    df = pd.read_csv(url)

    df['tanggal_nabung'] = pd.to_datetime(df['tanggal_nabung'])

    df['tahun'] = df['tanggal_nabung'].dt.year
    df['bulan'] = df['tanggal_nabung'].dt.month
    df['nama_bulan'] = df['tanggal_nabung'].dt.strftime('%b')

    df['hari_minggu'] = df['tanggal_nabung'].dt.dayofweek

    df['tipe_hari'] = df['hari_minggu'].apply(
        lambda x: 'Akhir Pekan' if x >= 5 else 'Hari Kerja'
    )

    df['lama_menabung'] = (
        df.groupby('id_tabungan')['tanggal_nabung']
        .transform(lambda x: (x.max() - x.min()).days)
    )

    df['hasil_akhir'] = (
        df.groupby('id_tabungan')['status']
        .transform(lambda x: 'Selesai' if (x == 'Selesai').any() else 'Belum Selesai')
    )

    df = df.sort_values(['id_tabungan', 'tanggal_nabung'])

    df['jarak_hari_nabung'] = (
        df.groupby('id_tabungan')['tanggal_nabung']
        .diff()
        .dt.days
    )

    df['jarak_hari_nabung'] = df['jarak_hari_nabung'].fillna(0)

    return df


df = load_data_regresi()


def tampilan_regresi():

    st.title("Dashboard Analytics Regresi Tabungan")

    st.subheader("Ringkasan Keuangan")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Rencana Target",
            f"Rp {df['target_nominal'].sum():,.0f}"
        )

    with col2:
        st.metric(
            "Total Dana Terkumpul",
            f"Rp {df['total_terkumpul'].sum():,.0f}"
        )

    with col3:

        jumlah_id_unik = df['id_tabungan'].nunique()

        st.metric(
            "Jumlah Rencana Goal",
            f"{jumlah_id_unik:,} Goal"
        )

    with col4:

        st.metric(
            "Total Dataset",
            f"{len(df):,} Kali"
        )

    st.subheader("Analisis Tren Waktu Menabung")

    col_freq1, col_freq2 = st.columns(2)

    with col_freq1:

        st.write("**Frekuensi Transaksi per Bulan**")

        freq_bulan = (
            df.groupby(['bulan', 'nama_bulan'])
            .size()
            .reset_index(name='jumlah_transaksi')
        )

        freq_bulan = freq_bulan.sort_values('bulan')

        transaksi_terbanyak = freq_bulan['jumlah_transaksi'].max()

        warna_bulan = [
            '#f59e0b' if val == transaksi_terbanyak else '#8b5cf6'
            for val in freq_bulan['jumlah_transaksi']
        ]

        fig_bar = px.bar(
            freq_bulan,
            x='nama_bulan',
            y='jumlah_transaksi',
            text_auto=True,
            title="Jumlah Transaksi Berdasarkan Bulan"
        )

        fig_bar.update_traces(
            marker_color=warna_bulan,
            textposition='outside'
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with col_freq2:

        st.write("**Total Nominal Nabung per Bulan**")

        nominal_bulan = (
            df.groupby(['bulan', 'nama_bulan'])['nominal_nabung']
            .sum()
            .reset_index(name='total_nominal')
        )

        nominal_bulan = nominal_bulan.sort_values(by='bulan')

        nominal_bulan['teks_display'] = nominal_bulan[
            'total_nominal'
        ].apply(lambda x: f"Rp {x:,.0f}")

        nilai_tertinggi = nominal_bulan['total_nominal'].max()

        warna_bar = [
            '#f59e0b' if val == nilai_tertinggi else '#10b981'
            for val in nominal_bulan['total_nominal']
        ]

        fig_bar_bulan = px.bar(
            nominal_bulan,
            x='nama_bulan',
            y='total_nominal',
            text='teks_display',
            title="Total Nominal Tabungan Setiap Bulan"
        )

        fig_bar_bulan.update_traces(
            marker_color=warna_bar,
            textposition='outside'
        )

        st.plotly_chart(fig_bar_bulan, use_container_width=True)

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        'EDA',
        'Visualisasi Pertanyaan Bisnis',
        'Data'
    ])
    
    # EDA
    with tab1:

        sub_tab1, sub_tab2 = st.tabs([
            "Overview & Persentase Terkumpul",
            "Distribusi Target Nominal"
        ])

        with sub_tab1:

            st.subheader(
                "Visualisasi Distribusi persentase_terkumpul"
            )

            col_grafik1, col_text1 = st.columns([1.3, 1])

            with col_grafik1:

                fig, ax = plt.subplots(figsize=(8, 5))

                sns.histplot(
                    data=df,
                    x='persentase_terkumpul',
                    bins=30,
                    kde=True,
                    color='skyblue',
                    edgecolor='black',
                    alpha=0.7,
                    ax=ax
                )

                ax.set_title(
                    "Visualisasi Distribusi persentase_terkumpul"
                )

                ax.set_xlabel("Persentase (%)")
                ax.set_ylabel("Frekuensi")

                ax.grid(
                    True,
                    linestyle='--',
                    alpha=0.4
                )

                st.pyplot(fig)

            with col_text1:

                st.markdown("""
                **Insight Persentase Terkumpul:**
                - Rata-rata persentase tabungan yang terkumpul sekitar 50%.
                - Median 49% menunjukkan sebagian besar pengguna sudah mencapai hampir separuh target.
                - Distribusi terlihat cukup merata di rentang 0–100%.
                """)

        with sub_tab2:

            st.subheader(
                "Visualisasi Distribusi Target Nominal"
            )

            col_grafik2, col_text2 = st.columns([1.3, 1])

            with col_grafik2:

                fig, ax = plt.subplots(figsize=(8, 5))

                sns.histplot(
                    df['target_nominal'],
                    bins=30,
                    kde=True,
                    color='skyblue',
                    edgecolor='black',
                    alpha=0.7,
                    ax=ax
                )

                ax.set_title(
                    'Visualisasi Distribusi target_nominal'
                )

                ax.set_xlabel('Target Nominal (Rp)')
                ax.set_ylabel('Frekuensi')

                ax.grid(alpha=0.3)

                st.pyplot(fig)

            with col_text2:

                st.markdown("""
                **Insight Target Nominal:**
                - Distribusi target nominal cenderung right-skewed.
                - Sebagian besar target berada pada nominal rendah.
                - Terdapat beberapa outlier dengan target sangat besar.
                """)
    
    # Visualisasi Pertanyaan Bisnis
    with tab2:

        sub_Q1, sub_Q2 = st.tabs([
            "Pertanyaan 1",
            "Pertanyaan 2"
        ])
        # Pertanyaan bisnis 1
        with sub_Q1:

            st.markdown("""
            ### Q1
            "Dari 10 nama_goal dengan frekuensi tertinggi, mana yang memiliki rata-rata persentase pencapaian terendah untuk tabungan 'Belum Selesai' yang sudah berjalan lebih dari 180 hari?"
            """)

            col_chart_q1, col_text_q1 = st.columns([1.6, 1])

            with col_chart_q1:

                df_uni = (
                    df.sort_values('tanggal_nabung')
                    .groupby('id_tabungan')
                    .last()
                    .reset_index()
                )

                df_belum_selesai = df_uni[
                    (df_uni['hasil_akhir'] == 'Belum Selesai') &
                    (df_uni['lama_menabung'] > 180)
                ].copy()

                top10_goals = (
                    df_belum_selesai['nama_goal']
                    .value_counts()
                    .head(10)
                    .index
                )

                df_top10 = df_belum_selesai[
                    df_belum_selesai['nama_goal'].isin(top10_goals)
                ]

                mean_per_goal = (
                    df_top10
                    .groupby('nama_goal')['persentase_terkumpul']
                    .mean()
                    .sort_values()
                )

                fig, ax = plt.subplots(figsize=(12, 7))

                colors = plt.cm.RdYlGn_r(
                    mean_per_goal.values / 100
                )

                bars = ax.barh(
                    mean_per_goal.index,
                    mean_per_goal.values,
                    color=colors,
                    edgecolor='black'
                )

                for bar, val in zip(
                    bars,
                    mean_per_goal.values
                ):

                    ax.text(
                        val + 1,
                        bar.get_y() + bar.get_height()/2,
                        f'{val:.1f}%',
                        va='center',
                        fontsize=10,
                        fontweight='bold'
                    )

                ax.axvline(
                    x=50,
                    color='red',
                    linestyle='--',
                    linewidth=2,
                    alpha=0.7,
                    label='Target 50%'
                )

                ax.set_xlabel(
                    'Rata-rata Persentase Terkumpul (%)',
                    fontsize=12
                )

                ax.set_title(
                    'Q1: Rata-rata Persentase Pencapaian per Goal\n(Status: Belum Selesai | Top 10 Goal)',
                    fontsize=14,
                    fontweight='bold'
                )

                ax.legend()

                ax.grid(
                    axis='x',
                    alpha=0.3
                )

                plt.tight_layout()

                st.pyplot(fig)

            with col_text_q1:

                st.markdown("""
                ### Insight
                - Dana Darurat adalah goal yang paling tertinggal pencapaiannya meskipun termasuk dalam top 10 paling sering dipilih.
                - Hal ini menunjukkan bahwa user lebih konsisten menabung untuk tujuan yang menyenangkan (kamera, PC gaming, liburan) dibandingkan kebutuhan esensial seperti dana darurat.
                - Ada indikasi bahwa motivasi emosional (reward, lifestyle) lebih kuat dibanding motivasi rasional (kebutuhan darurat).
                """)
        # Pertanyaan bisnis 2
        with sub_Q2:

            st.markdown("""
            ### Q2
            "Bagaimana distribusi jarak_hari_nabung (dalam hari) untuk tabungan dengan status 'Selesai pada tahun 2022-2025, dan berapa median jarak antar setoran?"
            """)

            df_q2 = df[
                (df['hasil_akhir'] == 'Selesai') &
                (df['tahun'].between(2022, 2025))
            ].copy()

            median_value = df_q2[
                'jarak_hari_nabung'
            ].median()

            fig, (ax1, ax2) = plt.subplots(
                1,
                2,
                figsize=(14, 5)
            )

            ax1.hist(
                df_q2['jarak_hari_nabung'],
                bins=30,
                edgecolor='black',
                color='steelblue',
                alpha=0.7
            )

            ax1.axvline(
                median_value,
                color='red',
                linestyle='--',
                linewidth=2,
                label=f'Median: {median_value:.0f} hari'
            )

            ax1.set_xlabel('Jarak Hari Nabung')
            ax1.set_ylabel('Frekuensi')
            ax1.set_title('Distribusi Jarak Nabung')

            ax1.legend()

            ax2.boxplot(
                df_q2['jarak_hari_nabung'],
                vert=False,
                patch_artist=True,
                boxprops=dict(
                    facecolor='steelblue',
                    alpha=0.7
                )
            )

            ax2.axvline(
                median_value,
                color='red',
                linestyle='--',
                linewidth=2,
                label=f'Median: {median_value:.0f} hari'
            )

            ax2.set_xlabel('Jarak Hari Nabung')
            ax2.set_title('Ringkasan Statistik')

            ax2.legend()

            plt.suptitle(
                'Q2: Jarak Antar Setoran',
                fontsize=14,
                fontweight='bold'
            )

            plt.tight_layout()

            st.pyplot(fig)

            st.markdown("""
            ### Insight

            - Pola umum: pengguna yang berhasil menyelesaikan tabungan di periode 2022–2025 cenderung menabung sekitar 2–3 minggu sekali.
            - Outlier menunjukkan adanya perilaku ekstrem: sebagian langsung menyelesaikan dalam waktu singkat (0 hari, sekali setor besar), sebagian lain menabung sangat jarang.
            - Konsistensi menabung dalam interval ≤ 1 bulan tampaknya menjadi faktor penting keberhasilan.
            """)
    # Dataset
    with tab3:

        st.header("Data Transaksi")

        csv = df.to_csv(index=False)

        st.download_button(
            'Download Dataset (CSV)',
            csv,
            'data_keuangan.csv',
            'text/csv'
        )

        st.dataframe(
            df,
            use_container_width=True
        )

if __name__ == "__main__":
    tampilan_regresi()