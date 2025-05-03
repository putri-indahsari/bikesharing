import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Set style
sns.set(style="whitegrid")
plt.style.use('seaborn')

# Judul utama dengan styling
st.markdown("""
    <style>
        .title {
            font-size: 36px !important;
            color: #2c3e50;
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 2px solid #3498db;
        }
        .header {
            color: #3498db;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">Dashboard Analisis Penyewaan Sepeda (2011–2012)</h1>', unsafe_allow_html=True)

# ===============================
# SIDEBAR FILTER
# ===============================
st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=['2011', '2012'],
    default=['2011', '2012']
)

# Konversi filter ke kode tahun
year_filter = [0 if '2011' in selected_year else None, 
              1 if '2012' in selected_year else None]
year_filter = [x for x in year_filter if x is not None]

# Filter data berdasarkan tahun yang dipilih
day_df_filtered = day_df[day_df['yr'].isin(year_filter)]
hour_df_filtered = hour_df[hour_df['yr'].isin(year_filter)]

# ===============================
# PERTANYAAN BISNIS 1
# ===============================
st.markdown('<h2 class="header">Pertanyaan 1: Perbedaan Penyewaan Sepeda Musim Panas vs Musim Dingin</h2>', unsafe_allow_html=True)

# Pra-pemrosesan
day_df_filtered['season_name'] = day_df_filtered['season'].map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
day_df_filtered['year'] = day_df_filtered['yr'].map({0: '2011', 1: '2012'})
day_df_filtered['workingday_label'] = day_df_filtered['workingday'].map({0: 'Libur', 1: 'Hari Kerja'})
filtered_season = day_df_filtered[day_df_filtered['season'].isin([1, 3])]  # Hanya summer dan winter

# Visualisasi baru dari Colab
st.subheader("Perbandingan Rata-Rata Penyewaan Sepeda per Musim")
season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
day_df_filtered['season_name'] = day_df_filtered['season'].map(season_mapping)
seasonal_avg = day_df_filtered.groupby(['yr', 'season_name'])['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season_name', y='cnt', hue='yr', data=seasonal_avg, 
            palette={0: '#3498db', 1: '#e74c3c'}, ax=ax)
ax.set_title('Perbandingan Rata-Rata Penyewaan Sepeda per Musim (2011-2012)')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-Rata Penyewaan Sepeda')
ax.legend(title='Tahun', labels=['2011', '2012'])
st.pyplot(fig)

# Container untuk visualisasi musim
season_col1, season_col2 = st.columns(2)

with season_col1:
    # Visualisasi rata-rata penyewaan
    st.subheader("Rata-rata Penyewaan: Musim Panas vs Dingin")
    seasonal_avg_filtered = filtered_season.groupby(['year', 'season_name'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=seasonal_avg_filtered, x='year', y='cnt', hue='season_name', 
                palette='coolwarm', ax=ax)
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)

with season_col2:
    # Visualisasi suhu
    st.subheader("Rata-rata Suhu Udara")
    fig, ax = plt.subplots()
    sns.barplot(data=filtered_season, x='season_name', y='temp', 
                palette='coolwarm', ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Suhu (normalisasi)')
    st.pyplot(fig)

# Container untuk kelembapan dan cuaca
weather_col1, weather_col2 = st.columns(2)

with weather_col1:
    # Visualisasi kelembapan
    st.subheader("Rata-rata Kelembapan Udara")
    fig, ax = plt.subplots()
    sns.barplot(data=filtered_season, x='season_name', y='hum', 
                palette='coolwarm', ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Kelembapan (normalisasi)')
    st.pyplot(fig)

with weather_col2:
    # Visualisasi kondisi cuaca
    filtered_season['weather_label'] = filtered_season['weathersit'].map({
        1: 'Cerah',
        2: 'Berkabut',
        3: 'Hujan Ringan',
        4: 'Hujan Lebat'
    })
    st.subheader("Pengaruh Cuaca terhadap Penyewaan")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=filtered_season, x='weather_label', y='cnt', 
                hue='season_name', ax=ax, palette='coolwarm')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Penyewaan')
    plt.xticks(rotation=15)
    st.pyplot(fig)

# Hari kerja vs libur
st.subheader("Pola Penyewaan: Hari Kerja vs Libur")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=filtered_season, x='workingday_label', y='cnt', 
            hue='season_name', palette='coolwarm', ax=ax)
ax.set_xlabel('Jenis Hari')
ax.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig)

# ===============================
# PERTANYAAN BISNIS 2
# ===============================
st.markdown('<h2 class="header">Pertanyaan 2: Pengaruh Hari Libur terhadap Penyewaan Sepeda</h2>', unsafe_allow_html=True)

hour_df_filtered['year'] = hour_df_filtered['yr'].map({0: 2011, 1: 2012})

# Container untuk visualisasi hari libur
holiday_col1, holiday_col2 = st.columns(2)

with holiday_col1:
    # Hari libur per jam
    st.subheader("Pola Penyewaan per Jam di Hari Libur")
    holiday_hourly = hour_df_filtered[hour_df_filtered['holiday'] == 1]
    hourly_avg = holiday_hourly.groupby(['hr', 'year'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(data=hourly_avg, x='hr', y='cnt', hue='year', 
                 palette={2011: 'skyblue', 2012: 'coral'}, ax=ax)
    ax.set_xlabel('Jam (0-23)')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.set_xticks(range(0, 24, 2))
    st.pyplot(fig)

with holiday_col2:
    # Hari libur per bulan
    st.subheader("Pola Penyewaan per Bulan di Hari Libur")
    day_df_filtered['month'] = day_df_filtered['mnth']
    holiday_monthly = day_df_filtered[day_df_filtered['holiday'] == 1]
    monthly_avg = holiday_monthly.groupby(['month', 'year'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(data=monthly_avg, x='month', y='cnt', hue='year', 
                 marker='o', palette={2011: 'skyblue', 2012: 'coral'}, ax=ax)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 
                       'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)

# Container untuk perbandingan hari libur vs kerja
holiday_col3, holiday_col4 = st.columns(2)

with holiday_col3:
    # Rata-rata penyewaan: libur vs kerja
    st.subheader("Perbandingan Hari Libur vs Hari Kerja")
    hour_df_filtered['holiday_type'] = hour_df_filtered['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})
    holiday_avg = hour_df_filtered.groupby(['year', 'holiday_type'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=holiday_avg, x='year', y='cnt', hue='holiday_type', 
                palette={'Hari Libur': '#e74c3c', 'Hari Kerja': '#3498db'}, ax=ax)
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)

with holiday_col4:
    # Per jam: libur vs kerja
    st.subheader("Pola Penyewaan per Jam: Libur vs Kerja")
    hourly_avg = hour_df_filtered.groupby(['hr', 'holiday_type'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(data=hourly_avg, x='hr', y='cnt', hue='holiday_type', 
                 palette={'Hari Kerja': '#3498db', 'Hari Libur': '#e74c3c'}, ax=ax)
    ax.set_xlabel('Jam (0-23)')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.set_xticks(range(0, 24, 2))
    st.pyplot(fig)

# ===============================
# INSIGHTS & KESIMPULAN
# ===============================
st.markdown('<h2 class="header">Insights & Kesimpulan</h2>', unsafe_allow_html=True)

with st.expander("Kesimpulan Analisis Musim"):
    st.write("""
    - **Penyewaan tertinggi** terjadi pada musim panas (summer) dan terendah pada musim dingin (winter)
    - Tahun 2012 menunjukkan peningkatan penyewaan dibandingkan 2011 di semua musim
    - Suhu yang lebih hangat berkorelasi positif dengan jumlah penyewaan
    - Cuaca cerah mendominasi penyewaan sepeda dibanding kondisi cuaca buruk
    - Pada hari kerja, penyewaan lebih tinggi dibanding hari libur di musim panas
    """)

with st.expander("Kesimpulan Analisis Hari Libur"):
    st.write("""
    - Pola penyewaan di hari libur menunjukkan puncak pada jam 12-15 siang
    - Bulan dengan hari libur terbanyak (Juni-Agustus) menunjukkan penyewaan tinggi
    - Rata-rata penyewaan di hari kerja lebih tinggi dibanding hari libur
    - Pola harian penyewaan berbeda signifikan antara hari kerja dan libur
    - Hari kerja menunjukkan pola commute (puncak pagi dan sore)
    """)

# Menambahkan informasi dataset
st.sidebar.markdown("---")
st.sidebar.subheader("Informasi Dataset")
st.sidebar.write(f"Jumlah Data Harian: {len(day_df)} baris")
st.sidebar.write(f"Jumlah Data Per Jam: {len(hour_df)} baris")
st.sidebar.write("Sumber: Capital Bikeshare (2011-2012)")
