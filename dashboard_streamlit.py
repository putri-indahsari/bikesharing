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
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Set style
sns.set(style="whitegrid")

# Sidebar for interactive filters
st.sidebar.header('Filter Data')

# Date range filter
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()
date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Year filter
year_options = ['Semua'] + sorted(day_df['yr'].map({0: 2011, 1: 2012}).unique())
selected_year = st.sidebar.selectbox('Pilih Tahun', year_options)

# Season filter
season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
season_options = ['Semua'] + list(season_mapping.values())
selected_season = st.sidebar.selectbox('Pilih Musim', season_options)

# Weather filter
weather_mapping = {
    1: 'Cerah / Sebagian Berawan',
    2: 'Berkabut + Berawan', 
    3: 'Hujan Ringan / Salju',
    4: 'Hujan Lebat / Badai'
}
weather_options = ['Semua'] + list(weather_mapping.values())
selected_weather = st.sidebar.selectbox('Pilih Kondisi Cuaca', weather_options)

# Apply filters
def apply_filters(df):
    # Date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['dteday'] >= pd.to_datetime(start_date)) & 
                (df['dteday'] <= pd.to_datetime(end_date))]
    
    # Year filter
    if selected_year != 'Semua':
        year_map = {2011: 0, 2012: 1}
        df = df[df['yr'] == year_map[selected_year]]
    
    # Season filter
    if selected_season != 'Semua':
        reverse_season_map = {v: k for k, v in season_mapping.items()}
        df = df[df['season'] == reverse_season_map[selected_season]]
    
    # Weather filter
    if selected_weather != 'Semua':
        reverse_weather_map = {v: k for k, v in weather_mapping.items()}
        df = df[df['weathersit'] == reverse_weather_map[selected_weather]]
    
    return df

filtered_day_df = apply_filters(day_df)
filtered_hour_df = apply_filters(hour_df)

# Judul utama
st.title("Dashboard Analisis Penyewaan Sepeda (2011–2012)")

# Show filter summary
st.subheader("Filter yang Aktif")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rentang Tanggal", f"{date_range[0]} to {date_range[1]}")
col2.metric("Tahun", selected_year if selected_year != 'Semua' else "Semua")
col3.metric("Musim", selected_season if selected_season != 'Semua' else "Semua")
col4.metric("Cuaca", selected_weather if selected_weather != 'Semua' else "Semua")

# ===============================
# PERTANYAAN BISNIS 1
# ===============================
st.header("Pertanyaan 1: Bagaimana perbedaan jumlah penyewaan sepeda antara musim panas dan musim dingin?")

# Add season names
filtered_day_df['season_name'] = filtered_day_df['season'].map(season_mapping)
filtered_day_df['year'] = filtered_day_df['yr'].map({0: '2011', 1: '2012'})
filtered_day_df['workingday_label'] = filtered_day_df['workingday'].map({0: 'Libur', 1: 'Hari Kerja'})

# Interactive selection for seasons to compare
selected_seasons = st.multiselect(
    "Pilih musim untuk dibandingkan",
    options=list(season_mapping.values()),
    default=['Summer', 'Winter']
)

if selected_seasons:
    # Filter data for selected seasons
    reverse_season_map = {v: k for k, v in season_mapping.items()}
    season_codes = [reverse_season_map[s] for s in selected_seasons]
    season_comparison_df = filtered_day_df[filtered_day_df['season'].isin(season_codes)]
    
    st.subheader(f"Perbandingan Penyewaan Sepeda: {', '.join(selected_seasons)}")
    
    # Visualization 1: Seasonal comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x='season_name', 
        y='cnt', 
        hue='year', 
        data=season_comparison_df,
        ax=ax
    )
    ax.set_title(f'Perbandingan Rata-Rata Penyewaan Sepeda ({", ".join(selected_seasons)})')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-Rata Penyewaan')
    st.pyplot(fig)
    
    # Visualization 2: Weather impact
    st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
    weather_comparison = season_comparison_df.copy()
    weather_comparison['weather_label'] = weather_comparison['weathersit'].map(weather_mapping)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=weather_comparison, 
        x='weather_label', 
        y='cnt', 
        hue='season_name',
        ax=ax
    )
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Visualization 3: Working day vs holiday
    st.subheader("Hari Kerja vs Libur")
    fig, ax = plt.subplots()
    sns.barplot(
        data=season_comparison_df, 
        x='workingday_label', 
        y='cnt', 
        hue='season_name',
        ax=ax
    )
    st.pyplot(fig)

# ===============================
# PERTANYAAN BISNIS 2
# ===============================
st.header("Pertanyaan 2: Bagaimana pengaruh hari libur terhadap jumlah penyewaan sepeda?")

# Interactive toggle for hourly/monthly view
analysis_view = st.radio(
    "Pilih Tampilan Analisis",
    options=['Per Jam', 'Per Bulan'],
    horizontal=True
)

if analysis_view == 'Per Jam':
    st.subheader("Pola Penyewaan Sepeda per Jam di Hari Libur")
    holiday_hourly = filtered_hour_df[filtered_hour_df['holiday'] == 1]
    
    if not holiday_hourly.empty:
        hourly_avg = holiday_hourly.groupby(['hr', 'year'])['cnt'].mean().reset_index()
        fig, ax = plt.subplots()
        sns.lineplot(
            data=hourly_avg, 
            x='hr', 
            y='cnt', 
            hue='year', 
            palette={2011: 'skyblue', 2012: 'coral'},
            marker='o',
            ax=ax
        )
        ax.set_xticks(range(0, 24))
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data yang tersedia untuk filter yang dipilih")

else:
    st.subheader("Pola Penyewaan Sepeda per Bulan di Hari Libur")
    filtered_day_df['month'] = filtered_day_df['mnth']
    holiday_monthly = filtered_day_df[filtered_day_df['holiday'] == 1]
    
    if not holiday_monthly.empty:
        monthly_avg = holiday_monthly.groupby(['month', 'year'])['cnt'].mean().reset_index()
        fig, ax = plt.subplots()
        sns.lineplot(
            data=monthly_avg, 
            x='month', 
            y='cnt', 
            hue='year', 
            marker='o', 
            ax=ax
        )
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data yang tersedia untuk filter yang dipilih")

# Additional interactive comparison
st.subheader("Perbandingan Hari Libur vs Hari Kerja")
compare_option = st.selectbox(
    "Pilih Metode Perbandingan",
    options=['Rata-rata Penyewaan', 'Pola per Jam']
)

if compare_option == 'Rata-rata Penyewaan':
    filtered_hour_df['holiday_type'] = filtered_hour_df['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})
    holiday_avg = filtered_hour_df.groupby(['year', 'holiday_type'])['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots()
    sns.barplot(
        data=holiday_avg, 
        x='year', 
        y='cnt', 
        hue='holiday_type', 
        palette={'Hari Libur': 'red', 'Hari Kerja': 'blue'}, 
        ax=ax
    )
    st.pyplot(fig)
else:
    hourly_avg = filtered_hour_df.groupby(['hr', 'holiday_type'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(
        data=hourly_avg, 
        x='hr', 
        y='cnt', 
        hue='holiday_type', 
        palette={'Hari Kerja': 'blue', 'Hari Libur': 'red'}, 
        ax=ax
    )
    ax.set_xticks(range(0, 24))
    st.pyplot(fig)

# Show raw data option
if st.checkbox('Tampilkan Data Mentah'):
    st.subheader('Data Mentah')
    st.write(filtered_day_df)
