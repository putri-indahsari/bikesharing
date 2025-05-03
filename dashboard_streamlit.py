import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Set style
sns.set(style="whitegrid")

# Judul utama
st.title("Dashboard Analisis Penyewaan Sepeda (2011–2012)")

# ===============================
# PERTANYAAN BISNIS 1
# ===============================
st.header("Pertanyaan 1: Bagaimana perbedaan jumlah penyewaan sepeda antara musim panas dan musim dingin pada tahun 2011–2012?")

# Pra-pemrosesan
day_df['season_name'] = day_df['season'].map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
day_df['year'] = day_df['yr'].map({0: '2011', 1: '2012'})
day_df['workingday_label'] = day_df['workingday'].map({0: 'Libur', 1: 'Hari Kerja'})
filtered = day_df[day_df['season'].isin([1, 3])]  # Hanya summer dan winter

st.subheader("Perbandingan Penyewaan Sepeda per Musim (2011–2012)")
season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
day_df_filtered = day_df[day_df['yr'].isin([0, 1])].copy()
day_df_filtered['season_name'] = day_df_filtered['season'].map(season_mapping)

seasonal_avg = day_df_filtered.groupby(['yr', 'season_name'])['cnt'].mean().reset_index()
seasonal_avg['yr'] = seasonal_avg['yr'].map({0: '2011', 1: '2012'})

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season_name', y='cnt', hue='yr', data=seasonal_avg, ax=ax)
plt.title('Perbandingan Rata-Rata Penyewaan Sepeda per Musim (2011–2012)')
plt.xlabel('Musim')
plt.ylabel('Rata-Rata Penyewaan')
plt.legend(title='Tahun')
st.pyplot(fig)

# Visualisasi rata-rata penyewaan
ax.set_title('Perbandingan Rata-Rata Penyewaan Sepeda: 2011 vs 2012 (Musim Panas dan Dingin)', fontsize=14)
ax.set_xlabel('Tahun', fontsize=12)
ax.set_ylabel('Rata-Rata Penyewaan Sepeda', fontsize=12)
ax.legend(title='Musim', bbox_to_anchor=(1, 1))
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Visualisasi suhu
st.subheader("Rata-rata Suhu Udara")
fig, ax = plt.subplots()
sns.barplot(data=filtered, x='season_name', y='temp', palette='coolwarm', ax=ax)
st.pyplot(fig)

# Visualisasi kelembapan
st.subheader("Rata-rata Kelembapan Udara")
fig, ax = plt.subplots()
sns.barplot(data=filtered, x='season_name', y='hum', palette='coolwarm', ax=ax)
st.pyplot(fig)

# Visualisasi kondisi cuaca
filtered['weather_label'] = filtered['weathersit'].map({
    1: 'Cerah / Sebagian Berawan',
    2: 'Berkabut + Berawan',
    3: 'Hujan Ringan / Salju',
    4: 'Hujan Lebat / Badai'
})
st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered, x='weather_label', y='cnt', hue='season_name', ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# Hari kerja vs libur
st.subheader("Hari Kerja vs Libur: Summer vs Winter")
fig, ax = plt.subplots()
sns.barplot(data=filtered, x='workingday_label', y='cnt', hue='season_name', ax=ax)
st.pyplot(fig)

# ===============================
# PERTANYAAN BISNIS 2
# ===============================
st.header("Pertanyaan 2: Bagaimana pengaruh hari libur terhadap jumlah penyewaan sepeda pada tahun 2011–2012?")

hour_df['year'] = hour_df['yr'].map({0: 2011, 1: 2012})

# Hari libur per jam
st.subheader("Pola Penyewaan Sepeda per Jam di Hari Libur")
holiday_hourly = hour_df[hour_df['holiday'] == 1]
hourly_avg = holiday_hourly.groupby(['hr', 'year'])['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=hourly_avg, x='hr', y='cnt', hue='year', palette={2011: 'skyblue', 2012: 'coral'}, ax=ax)
st.pyplot(fig)

# Hari libur per bulan
st.subheader("Pola Penyewaan Sepeda per Bulan di Hari Libur")
day_df['month'] = day_df['mnth']
holiday_monthly = day_df[day_df['holiday'] == 1]
monthly_avg = holiday_monthly.groupby(['month', 'year'])['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=monthly_avg, x='month', y='cnt', hue='year', marker='o', ax=ax)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
st.pyplot(fig)

# Rata-rata penyewaan: libur vs kerja
st.subheader("Rata-Rata Penyewaan: Hari Libur vs Hari Kerja")
hour_df['holiday_type'] = hour_df['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})
holiday_avg = hour_df.groupby(['year', 'holiday_type'])['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=holiday_avg, x='year', y='cnt', hue='holiday_type', palette={'Hari Libur': 'red', 'Hari Kerja': 'blue'}, ax=ax)
st.pyplot(fig)

# Per jam: libur vs kerja
st.subheader("Pola Penyewaan per Jam: Hari Libur vs Hari Kerja")
hourly_avg = hour_df.groupby(['hr', 'holiday_type'])['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=hourly_avg, x='hr', y='cnt', hue='holiday_type', palette={'Hari Kerja': 'blue', 'Hari Libur': 'red'}, ax=ax)
st.pyplot(fig)
