import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Atur gaya Seaborn untuk plot
sns.set(style='whitegrid')

# Muat dataset
data_sewa_sepeda = pd.read_csv("bike_day.csv")

# Header aplikasi Streamlit
st.title("🚴‍♂️ Dashboard Sewa Sepeda 🚴‍♀️")
st.markdown("### Menganalisis Pengaruh Cuaca dan Penyewaan Sepeda dengan Teknik Analisis Lanjutan")

# Sidebar untuk navigasi
st.sidebar.header("Navigasi")
options = st.sidebar.selectbox("Pilih tampilan:", ["Analisis Cuaca", "Analisis Hari Kerja dan Libur", "RFM Analysis", "Geoanalysis", "Clustering Sederhana"])

# Fungsi untuk menampilkan analisis cuaca
def tampilkan_analisis_cuaca():
    st.subheader("Analisis Cuaca")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Plot sebar untuk 'temp' vs 'count'
    sns.scatterplot(
        x='temp',
        y='count',
        data=data_sewa_sepeda,
        alpha=0.6,
        color='royalblue',
        ax=axes[0]
    )
    axes[0].set_title('Suhu vs Penyewaan', fontsize=16)
    axes[0].set_xlabel('Suhu (°C)', fontsize=12)
    axes[0].set_ylabel('Jumlah Penyewaan', fontsize=12)

    # Plot sebar untuk 'atemp' vs 'count'
    sns.scatterplot(
        x='atemp',
        y='count',
        data=data_sewa_sepeda,
        alpha=0.6,
        color='forestgreen',
        ax=axes[1]
    )
    axes[1].set_title('Suhu Terasa vs Penyewaan', fontsize=16)
    axes[1].set_xlabel('Suhu Terasa (°C)', fontsize=12)
    axes[1].set_ylabel('Jumlah Penyewaan', fontsize=12)

    # Plot sebar untuk 'hum' vs 'count'
    sns.scatterplot(
        x='hum',
        y='count',
        data=data_sewa_sepeda,
        alpha=0.6,
        color='gold',
        ax=axes[2]
    )
    axes[2].set_title('Kelembapan vs Penyewaan', fontsize=16)
    axes[2].set_xlabel('Kelembapan (%)', fontsize=12)
    axes[2].set_ylabel('Jumlah Penyewaan', fontsize=12)

    # Tampilkan plot sebar
    st.pyplot(fig)

# Fungsi untuk menampilkan analisis hari kerja dan libur
def tampilkan_analisis_hari():
    st.subheader("Analisis Hari Kerja dan Libur")
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))

    # Plot batang untuk penyewaan pada hari libur
    sns.barplot(
        x='holiday',
        y='count',
        data=data_sewa_sepeda,
        ax=axes[0],
        palette='pastel'
    )
    axes[0].set_title('Penyewaan Sepeda pada Hari Libur', fontsize=16)
    axes[0].set_xlabel('Hari Libur', fontsize=12)
    axes[0].set_ylabel('Jumlah Penyewaan', fontsize=12)

    # Plot batang untuk penyewaan pada hari kerja
    sns.barplot(
        x='weekday',
        y='count',
        data=data_sewa_sepeda,
        ax=axes[1],
        palette='pastel'
    )
    axes[1].set_title('Penyewaan Sepeda pada Hari Kerja', fontsize=16)
    axes[1].set_xlabel('Hari Kerja', fontsize=12)
    axes[1].set_ylabel('Jumlah Penyewaan', fontsize=12)

    # Tampilkan plot batang
    st.pyplot(fig)

# Fungsi untuk RFM analysis
def rfm_analysis():
    st.subheader("RFM Analysis")
    
    # Ubah kolom 'dateday' menjadi format datetime (bukan 'dteday')
    data_sewa_sepeda['dateday'] = pd.to_datetime(data_sewa_sepeda['dateday'])
    
    # Recency: Hari sejak penyewaan terakhir
    today = data_sewa_sepeda['dateday'].max()  # Ambil tanggal terakhir dari dataset
    recency = (today - data_sewa_sepeda['dateday']).dt.days
    
    # Frequency: Jumlah penyewaan per tanggal (bisa diganti per pengguna jika tersedia)
    frequency = data_sewa_sepeda.groupby('dateday')['count'].sum().reset_index()
    
    # Monetary: Total sepeda yang disewa (gunakan 'count' untuk menggambarkan monetary)
    monetary = data_sewa_sepeda.groupby('dateday')['count'].sum().reset_index()

    # Gabungkan hasil RFM dalam satu DataFrame
    rfm = pd.DataFrame({
        'Date': data_sewa_sepeda['dateday'],
        'Recency': recency,
        'Frequency': frequency['count'],
        'Monetary': monetary['count']
    })
    
    # Tampilkan hasil RFM
    st.write(rfm)


# Fungsi untuk geoanalysis
def geoanalysis():
    st.subheader("Geoanalysis (Berbasis Waktu)")
    # Plot jumlah penyewaan berdasarkan season dan weekday
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='season', y='count', data=data_sewa_sepeda, palette='coolwarm')
    ax.set_title('Penyewaan Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

# Fungsi untuk clustering sederhana
def clustering_sederhana():
    st.subheader("Clustering Sederhana Berdasarkan Cuaca")
    # Membagi data menjadi kategori tinggi, sedang, rendah
    data_sewa_sepeda['temp_cluster'] = pd.cut(data_sewa_sepeda['temp'], bins=3, labels=['Rendah', 'Sedang', 'Tinggi'])
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='temp_cluster', data=data_sewa_sepeda, palette='viridis')
    ax.set_title('Jumlah Penyewaan Berdasarkan Kategori Suhu')
    ax.set_xlabel('Kategori Suhu')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

# Menampilkan konten berdasarkan pilihan pengguna
if options == "Analisis Cuaca":
    tampilkan_analisis_cuaca()
elif options == "Analisis Hari Kerja dan Libur":
    tampilkan_analisis_hari()
elif options == "RFM Analysis":
    rfm_analysis()
elif options == "Geoanalysis":
    geoanalysis()
elif options == "Clustering Sederhana":
    clustering_sederhana()

# Footer
st.markdown("---")
st.markdown("**Data Sumber:** Data sewa sepeda yang dianalisis berasal dari dataset yang telah disediakan.")
