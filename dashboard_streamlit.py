import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# Visualisasi rata-rata penyewaan
st.subheader("Rata-rata Penyewaan Sepeda: Musim Panas vs Musim Dingin")
seasonal_avg = filtered.groupby(['year', 'season_name'])['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=seasonal_avg, x='year', y='cnt', hue='season_name', palette='coolwarm', ax=ax)
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
plt.xticks(rotation=15)
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
