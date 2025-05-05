import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv('day.csv')
    hour_df = pd.read_csv('hour.csv')
    
    # Convert and add necessary columns
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    day_df['year'] = day_df['yr'].map({0: 2011, 1: 2012})
    hour_df['year'] = hour_df['yr'].map({0: 2011, 1: 2012})
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Set style
sns.set(style="whitegrid")

# Sidebar filters
st.sidebar.header('Filter Data')

# Year filter
selected_year = st.sidebar.selectbox(
    'Pilih Tahun',
    options=['Semua', 2011, 2012]
)

# Day type filter
day_type = st.sidebar.radio(
    "Jenis Hari",
    options=['Semua', 'Hari Kerja', 'Hari Libur'],
    horizontal=True
)

# Apply filters
def filter_data(df, is_day_df=True):
    # Year filter
    if selected_year != 'Semua':
        df = df[df['year'] == selected_year]
    
    # Day type filter
    if day_type != 'Semua':
        if is_day_df:
            df = df[df['holiday'] == (1 if day_type == 'Hari Libur' else 0)]
        else:
            df = df[df['holiday'] == (1 if day_type == 'Hari Libur' else 0)]
    
    return df

# Main dashboard
st.title("Dashboard Analisis Penyewaan Sepeda (2011-2012)")

# Show active filters
st.subheader("Filter Aktif")
col1, col2 = st.columns(2)
col1.metric("Tahun", selected_year)
col2.metric("Jenis Hari", day_type)

# ===================================
# VISUALISASI PERTANYAAN 1: ANALISIS MUSIMAN
# ===================================
st.header("Analisis Musiman")

# Visualisasi 1: Perbandingan Musim
st.subheader("Perbandingan Rata-Rata Penyewaan Sepeda per Musim (2011-2012)")

# Filter data untuk visualisasi musim
season_df = filter_data(day_df.copy())
season_df = season_df[season_df['yr'].isin([0, 1])]  # 0: 2011, 1: 2012

season_mapping = {1: 'winter', 2: 'spring', 3: 'summer', 4: 'fall'}
season_df['season_name'] = season_df['season'].map(season_mapping)
seasonal_avg = season_df.groupby(['yr', 'season_name'])['cnt'].mean().reset_index()

# Plot visualisasi asli
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x='season_name', y='cnt', hue='yr', data=seasonal_avg)
plt.title('Perbandingan Rata-Rata Penyewaan Sepeda per Musim (2011-2012)')
plt.xlabel('Musim')
plt.ylabel('Rata-Rata Penyewaan Sepeda')
plt.legend(title='Tahun', labels=['2011', '2012'])
st.pyplot(fig1)

# Visualisasi 2: Summer vs Winter
st.subheader("Perbandingan Summer vs Winter")

summer_winter_df = filter_data(day_df.copy())
summer_winter_df = summer_winter_df[summer_winter_df['season'].isin([2, 4]) & summer_winter_df['yr'].isin([0, 1])].copy()
summer_winter_df['season_name'] = summer_winter_df['season'].map({2: 'Summer', 4: 'Winter'})
summer_winter_df['year'] = summer_winter_df['yr'].map({0: '2011', 1: '2012'})
seasonal_avg = summer_winter_df.groupby(['year', 'season_name'])['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='year',
    y='cnt',
    hue='season_name',
    data=seasonal_avg,
    palette={'Summer': 'salmon', 'Winter': 'lightblue'}
)
plt.title('Perbandingan Rata-Rata Penyewaan Sepeda: 2011 vs 2012 (Musim Panas dan Dingin)', fontsize=14)
plt.xlabel('Tahun', fontsize=12)
plt.ylabel('Rata-Rata Penyewaan Sepeda', fontsize=12)
plt.legend(title='Musim', bbox_to_anchor=(1, 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig2)

# Visualisasi 3: Pengaruh Cuaca
st.subheader("Pengaruh Kondisi Cuaca")

weather_df = filter_data(day_df.copy())
weather_df = weather_df[weather_df['season'].isin([1, 3])]
weather_df['season_label'] = weather_df['season'].map({1: 'Winter', 3: 'Summer'})
weathersit_map = {
    1: 'Clear / Partly Cloudy',
    2: 'Mist + Cloudy', 
    3: 'Light Snow / Rain',
    4: 'Heavy Rain / Snow'
}
weather_df['weather_label'] = weather_df['weathersit'].map(weathersit_map)

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=weather_df,
    x='weather_label',
    y='cnt',
    hue='season_label',
    palette={'Summer': 'salmon', 'Winter': 'lightblue'}
)
plt.title('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda (Summer vs Winter)', fontsize=14)
plt.xlabel('Kondisi Cuaca', fontsize=12)
plt.ylabel('Jumlah Rata-Rata Penyewaan Sepeda', fontsize=12)
plt.legend(title='Musim')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig3)

# ===================================
# VISUALISASI PERTANYAAN 2: ANALISIS HARI LIBUR
# ===================================
st.header("Analisis Hari Libur")

# Visualisasi 4: Pola per Jam
st.subheader("Pola Penyewaan per Jam pada Hari Libur")

hourly_df = filter_data(hour_df.copy(), is_day_df=False)
holiday_hourly = hourly_df[hourly_df['holiday'] == 1]
hourly_avg = holiday_hourly.groupby(['hr', 'year'])['cnt'].mean().reset_index()

fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=hourly_avg, 
    x='hr', 
    y='cnt', 
    hue='year', 
    palette={2011: 'skyblue', 2012: 'coral'}
)
plt.title('Pola Rata-Rata Penyewaan Sepeda per Jam pada Hari Libur (2011–2012)', fontsize=14)
plt.xlabel('Jam (0–23)', fontsize=12)
plt.ylabel('Rata-Rata Jumlah Penyewaan', fontsize=12)
plt.xticks(range(0, 24))
plt.legend(title='Tahun')
plt.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig4)

# Visualisasi 5: Perbandingan Hari Libur vs Kerja
st.subheader("Perbandingan Hari Libur vs Hari Kerja")

holiday_compare_df = filter_data(hour_df.copy(), is_day_df=False)
holiday_compare_df['holiday_type'] = holiday_compare_df['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})
hourly_avg = holiday_compare_df.groupby(['hr', 'holiday_type'])['cnt'].mean().reset_index()

fig5, ax5 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x='hr',
    y='cnt',
    hue='holiday_type',
    data=hourly_avg,
    palette={'Hari Kerja': 'blue', 'Hari Libur': 'red'}
)
plt.title('Pola Penyewaan Sepeda per Jam: Hari Libur vs Hari Kerja')
plt.xlabel('Jam dalam Sehari (0-23)')
plt.ylabel('Rata-Rata Penyewaan')
plt.xticks(range(0, 24))
plt.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig5)
