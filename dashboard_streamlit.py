import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set judul dashboard
st.title('Analisis Data Penyewaan Sepeda')
st.markdown("""
**Nama:** Putri Indah Sari  
**Email:** putri04213@gmail.com  
**ID Dicoding:** MC813D5X1836
""")

# Load data
@st.cache_data
def load_data():
    hour_df = pd.read_csv('hour.csv')
    day_df = pd.read_csv('day.csv')
    return hour_df, day_df

hour_df, day_df = load_data()

# Konversi kolom dteday ke datetime
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar untuk navigasi
st.sidebar.title('Navigasi')
page = st.sidebar.radio("Pilih Halaman:", 
                        ["Pertanyaan Bisnis", 
                         "Eksplorasi Data", 
                         "Analisis Musiman", 
                         "Analisis Hari Libur"])

if page == "Pertanyaan Bisnis":
    st.header("Pertanyaan Bisnis")
    st.markdown("""
    1. Bagaimana perbedaan jumlah penyewaan sepeda antara musim panas dan musim dingin dalam tahun 2011-2012, dan faktor apa saja yang berkontribusi terhadap perbedaan tersebut?
    2. Bagaimana pengaruh hari libur terhadap jumlah penyewaan sepeda pada tahun 2011-2012, dan apakah ada pola tertentu yang dapat diidentifikasi?
    """)

elif page == "Eksplorasi Data":
    st.header("Eksplorasi Data")
    
    st.subheader("Data Hour")
    st.write(hour_df.head())
    st.write(f"Jumlah baris: {hour_df.shape[0]}, Jumlah kolom: {hour_df.shape[1]}")
    
    st.subheader("Data Day")
    st.write(day_df.head())
    st.write(f"Jumlah baris: {day_df.shape[0]}, Jumlah kolom: {day_df.shape[1]}")
    
    st.subheader("Statistik Deskriptif")
    st.write(day_df.describe())
    
    st.subheader("Distribusi Variabel Numerik")
    num_cols = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
    
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    for i, col in enumerate(num_cols):
        sns.boxplot(y=day_df[col], ax=axes[i//3, i%3])
        axes[i//3, i%3].set_title(f"Boxplot {col}")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Analisis Musiman":
    st.header("Analisis Musiman")
    
    # Mapping season
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    day_df['season_name'] = day_df['season'].map(season_map)
    
    # Perbedaan penyewaan antar musim
    st.subheader("Perbandingan Penyewaan Sepeda per Musim")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season_name', y='cnt', data=day_df, ax=ax, order=['Spring', 'Summer', 'Fall', 'Winter'])
    ax.set_title('Rata-rata Penyewaan Sepeda per Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)
    
    # Faktor yang mempengaruhi (suhu, kelembaban, kecepatan angin)
    st.subheader("Faktor yang Mempengaruhi Penyewaan Sepeda per Musim")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Suhu
    sns.boxplot(x='season_name', y='temp', data=day_df, ax=axes[0], order=['Spring', 'Summer', 'Fall', 'Winter'])
    axes[0].set_title('Distribusi Suhu per Musim')
    axes[0].set_xlabel('Musim')
    axes[0].set_ylabel('Suhu (normalized)')
    
    # Kelembaban
    sns.boxplot(x='season_name', y='hum', data=day_df, ax=axes[1], order=['Spring', 'Summer', 'Fall', 'Winter'])
    axes[1].set_title('Distribusi Kelembaban per Musim')
    axes[1].set_xlabel('Musim')
    axes[1].set_ylabel('Kelembaban')
    
    # Kecepatan Angin
    sns.boxplot(x='season_name', y='windspeed', data=day_df, ax=axes[2], order=['Spring', 'Summer', 'Fall', 'Winter'])
    axes[2].set_title('Distribusi Kecepatan Angin per Musim')
    axes[2].set_xlabel('Musim')
    axes[2].set_ylabel('Kecepatan Angin')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Korelasi faktor dengan jumlah penyewaan
    st.subheader("Korelasi Faktor Cuaca dengan Jumlah Penyewaan")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Suhu vs Penyewaan
    sns.scatterplot(x='temp', y='cnt', data=day_df, ax=axes[0])
    axes[0].set_title('Suhu vs Jumlah Penyewaan')
    axes[0].set_xlabel('Suhu (normalized)')
    axes[0].set_ylabel('Jumlah Penyewaan')
    
    # Kelembaban vs Penyewaan
    sns.scatterplot(x='hum', y='cnt', data=day_df, ax=axes[1])
    axes[1].set_title('Kelembaban vs Jumlah Penyewaan')
    axes[1].set_xlabel('Kelembaban')
    axes[1].set_ylabel('Jumlah Penyewaan')
    
    # Kecepatan Angin vs Penyewaan
    sns.scatterplot(x='windspeed', y='cnt', data=day_df, ax=axes[2])
    axes[2].set_title('Kecepatan Angin vs Jumlah Penyewaan')
    axes[2].set_xlabel('Kecepatan Angin')
    axes[2].set_ylabel('Jumlah Penyewaan')
    
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Analisis Hari Libur":
    st.header("Analisis Pengaruh Hari Libur")
    
    # Mapping holiday
    holiday_map = {0: 'Bukan Hari Libur', 1: 'Hari Libur'}
    day_df['holiday_name'] = day_df['holiday'].map(holiday_map)
    
    # Perbandingan penyewaan hari libur vs bukan libur
    st.subheader("Perbandingan Penyewaan Sepeda: Hari Libur vs Bukan Libur")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='holiday_name', y='cnt', data=day_df, ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda: Hari Libur vs Bukan Libur')
    ax.set_xlabel('Status Hari')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)
    
    # Penyewaan per hari dalam minggu
    st.subheader("Pola Penyewaan Sepeda per Hari dalam Minggu")
    
    # Mapping weekday
    weekday_map = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 
                  4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    day_df['weekday_name'] = day_df['weekday'].map(weekday_map)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weekday_name', y='cnt', data=day_df, 
                order=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'], ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda per Hari dalam Minggu')
    ax.set_xlabel('Hari dalam Minggu')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)
    
    # Perbandingan pengguna casual vs registered di hari libur
    st.subheader("Perbandingan Pengguna Casual vs Registered di Hari Libur")
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Hari Libur
    libur_data = day_df[day_df['holiday'] == 1]
    sns.barplot(x='holiday_name', y='casual', data=libur_data, ax=axes[0])
    axes[0].set_title('Pengguna Casual di Hari Libur')
    axes[0].set_xlabel('Status Hari')
    axes[0].set_ylabel('Jumlah Pengguna Casual')
    
    sns.barplot(x='holiday_name', y='registered', data=libur_data, ax=axes[1])
    axes[1].set_title('Pengguna Registered di Hari Libur')
    axes[1].set_xlabel('Status Hari')
    axes[1].set_ylabel('Jumlah Pengguna Registered')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Perbandingan pengguna casual vs registered di hari kerja
    st.subheader("Perbandingan Pengguna Casual vs Registered di Hari Kerja")
    
    kerja_data = day_df[day_df['workingday'] == 1]
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.barplot(x='weekday_name', y='casual', data=kerja_data, 
                order=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'], ax=axes[0])
    axes[0].set_title('Pengguna Casual di Hari Kerja')
    axes[0].set_xlabel('Hari dalam Minggu')
    axes[0].set_ylabel('Jumlah Pengguna Casual')
    
    sns.barplot(x='weekday_name', y='registered', data=kerja_data, 
                order=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'], ax=axes[1])
    axes[1].set_title('Pengguna Registered di Hari Kerja')
    axes[1].set_xlabel('Hari dalam Minggu')
    axes[1].set_ylabel('Jumlah Pengguna Registered')
    
    plt.tight_layout()
    st.pyplot(fig)