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
    
    # Convert date columns
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Add useful columns
    day_df['year'] = day_df['yr'].map({0: 2011, 1: 2012})
    hour_df['year'] = hour_df['yr'].map({0: 2011, 1: 2012})
    hour_df['holiday_type'] = hour_df['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Set style
sns.set(style="whitegrid")

# Sidebar for filters
st.sidebar.header('Filter Data')

# Simple year filter
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
def filter_data(df):
    # Year filter
    if selected_year != 'Semua':
        df = df[df['year'] == selected_year]
    
    # Day type filter
    if day_type != 'Semua':
        if 'holiday' in df.columns:  # For day_df
            df = df[df['holiday'] == (1 if day_type == 'Hari Libur' else 0)]
        elif 'holiday_type' in df.columns:  # For hour_df
            df = df[df['holiday_type'] == day_type]
    
    return df

filtered_day = filter_data(day_df)
filtered_hour = filter_data(hour_df)

# Main dashboard
st.title("Dashboard Analisis Penyewaan Sepeda (2011-2012)")

# Show active filters
st.subheader("Filter Aktif")
col1, col2 = st.columns(2)
col1.metric("Tahun", selected_year)
col2.metric("Jenis Hari", day_type)

# ===============================
# PERTANYAAN 1: ANALISIS MUSIMAN
# ===============================
st.header("Analisis Musiman")

# Add season names
season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
filtered_day['season'] = filtered_day['season'].map(season_map)

# Seasonal analysis
st.subheader("Pola Penyewaan per Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=filtered_day,
    x='season',
    y='cnt',
    hue='year',
    ax=ax,
    order=['Winter', 'Spring', 'Summer', 'Fall']
)
ax.set_title('Rata-rata Penyewaan Sepeda per Musim')
st.pyplot(fig)

# Weather impact
st.subheader("Pengaruh Cuaca")
weather_map = {
    1: 'Cerah',
    2: 'Berawan', 
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}
filtered_day['weather'] = filtered_day['weathersit'].map(weather_map)

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(
    data=filtered_day,
    x='weather',
    y='cnt',
    hue='season',
    ax=ax,
    order=['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Lebat']
)
plt.xticks(rotation=45)
st.pyplot(fig)

# ===============================
# PERTANYAAN 2: ANALISIS HARI LIBUR
# ===============================
st.header("Analisis Hari Libur vs Hari Kerja")

# Hourly pattern comparison
st.subheader("Pola Per Jam")

# Get hourly data based on filters
hourly_data = filtered_hour.groupby(['hr', 'holiday_type'])['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=hourly_data,
    x='hr',
    y='cnt',
    hue='holiday_type',
    style='holiday_type',
    markers=True,
    dashes=False,
    ax=ax
)
ax.set_xticks(range(0, 24))
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_title('Pola Penyewaan per Jam: Hari Kerja vs Hari Libur')
st.pyplot(fig)

# Monthly comparison
st.subheader("Perbandingan Bulanan")

monthly_data = filtered_day.groupby(['mnth', 'holiday'])['cnt'].mean().reset_index()
monthly_data['holiday_type'] = monthly_data['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=monthly_data,
    x='mnth',
    y='cnt',
    hue='holiday_type',
    style='holiday_type',
    markers=True,
    dashes=False,
    ax=ax
)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig)
