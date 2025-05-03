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
# insight/penjelasan
st.markdown("""
**Insight:**
Rata-rata penyewaan sepeda lebih tinggi pada musim panas dibandingkan musim dingin. 
Pertumbuhan penyewaan sepeda meningkat signifikan dari 2011 ke 2012, terutama pada musim panas. 
Perbedaan antara musim panas dan dingin semakin lebar pada 2012, menunjukkan peluang strategi khusus musim dingin.
""")

st.subheader("Perbandingan Penyewaan Sepeda: Musim Panas vs Dingin (2011-2012)")

# 1. Filter data untuk musim panas (2) dan dingin (4) serta tahun 2011-2012
summer_winter_df = day_df[day_df['season'].isin([2, 4]) & day_df['yr'].isin([0, 1])].copy()

# 2. Mapping nilai musim dan tahun
summer_winter_df['season_name'] = summer_winter_df['season'].map({2: 'Summer', 4: 'Winter'})
summer_winter_df['year'] = summer_winter_df['yr'].map({0: '2011', 1: '2012'})

# 3. Hitung rata-rata penyewaan per musim dan tahun
seasonal_avg = summer_winter_df.groupby(['year', 'season_name'])['cnt'].mean().reset_index()

# 4. Visualisasi dengan Streamlit
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='year',
    y='cnt',
    hue='season_name',
    data=seasonal_avg,
    palette={'Summer': 'salmon', 'Winter': 'lightblue'},
    ax=ax
)

ax.set_title('Perbandingan Rata-Rata Penyewaan Sepeda: 2011 vs 2012 (Musim Panas dan Dingin)', fontsize=14)
ax.set_xlabel('Tahun', fontsize=12)
ax.set_ylabel('Rata-Rata Penyewaan Sepeda', fontsize=12)
ax.legend(title='Musim', bbox_to_anchor=(1, 1))
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Tambahkan insight/penjelasan
st.markdown("""
**Insight:**
- Terlihat perbedaan yang signifikan antara penyewaan di musim panas dan dingin
- Penyewaan di musim panas lebih tinggi dibanding musim dingin di kedua tahun
- Terjadi peningkatan jumlah penyewaan dari 2011 ke 2012 untuk kedua musim
""")

# Visualisasi suhu
st.subheader("Rata-rata Suhu Udara")
fig, ax = plt.subplots()
sns.barplot(data=filtered, x='season_name', y='temp', palette='coolwarm', ax=ax)
st.pyplot(fig)
# insight/penjelasan
st.markdown("""
**Insight:**
suhu rata-rata pada musim panas (Summer) jauh lebih tinggi dibandingkan musim dingin (Winter).
Ini bisa menjadi salah satu alasan utama mengapa jumlah penyewaan sepeda meningkat saat musim panas—karena kondisi lebih nyaman untuk bersepeda. 
Semakin tinggi suhu (dalam skala normalisasi), semakin nyaman untuk bersepeda. Jadi, musim panas → lebih banyak penyewaan.
""")

# Visualisasi kelembapan
st.subheader("Rata-rata Kelembapan Udara")
fig, ax = plt.subplots()
sns.barplot(data=filtered, x='season_name', y='hum', palette='coolwarm', ax=ax)
st.pyplot(fig)
# insight/penjelasan
st.markdown("""
**Insight:**
Kelembapan pada musim dingin selisish sedikit daripada musim panas.
Kelembapan yang tinggi bisa membuat pengguna merasa tidak nyaman saat beraktivitas fisik seperti bersepeda karena Jika kelembapan tinggi,
udara terasa lebih pengap dan tidak nyaman,ini bisa menyebabkan penurunan aktivitas luar ruangan seperti bersepeda.
""")

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
# insight/penjelasan
st.markdown("""
**Insight:**
Musim panas menunjukkan penyewaan sepeda tertinggi, terutama saat cuaca cerah. Sebaliknya, cuaca buruk menurunkan penyewaan drastis, terutama di musim dingin. 
Pola ini konsisten, menunjukkan preferensi pengguna untuk bersepeda lebih tinggi di musim panas terlepas dari kondisi cuaca.

""")

# Hari kerja vs libur
st.subheader("Hari Kerja vs Libur: Summer vs Winter")
fig, ax = plt.subplots()
sns.barplot(data=filtered, x='workingday_label', y='cnt', hue='season_name', ax=ax)
st.pyplot(fig)
# insight/penjelasan
st.markdown("""
**Insight:**
- Musim panas menunjukkan penyewaan tinggi baik saat hari kerja (~5700) maupun hari libur (~5500), menandakan tingginya aktivitas bersepeda untuk rekreasi dan aktivitas harian.
Musim dingin justru lebih aktif saat hari kerja (~2800) dibanding hari libur (~2300), kemungkinan karena bersepeda digunakan sebagai moda transportasi rutin
- promosi diasarankan fokus pada musim dingin pada pengguna rutin (pekerja/pelajar).
Sediakan fasilitas pendukung seperti: Shelter untuk cuaca buruk,Jalur sepeda bebas salju,Sistem pelacakan real-time demi keamanan.
""")

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
# insight/penjelasan
st.markdown("""
**Insight:**
- dari tahun 2011 ke 2012 mengalami peningkatan pola penyewaan,terlihat 2012 memiliki pola penyewaan tertinggi dibanding tahun sebelumnya 2011
di kedua pola konsisten penyewaan tahun 2011 & 2012 memiliki kesamaan pola tren dijam yang hampir sama yakni dijam 11.00 siang - 14.00 dan juga di jam 16.00-18.00 sore
mungkin di jam jam tersebut merupakan waktu yang ideal untuk aktivistas liburan bersepeda bersama terutaman setelah makan siang dan sebelum makan malam
bisa saja penyewaan sepeda menjadi alternatif untuk wisata lokal /city tour karena cuaca di jam tersebut nyaman.
untuk lebih meningkatkan penyewaan dibanding hari kerja terdapat rekomendasi seperti pembukaan jalur sepeda baru, peningkatan infrastruktur, 
atau penambahan spot menarik yang dapat dikunjungi dengan sepeda.Lalu merupakan promosi dan kampanye hidup sehat / produktif untuk berolahraga bersepeda selama liburan
""")

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
# insight/penjelasan
st.markdown("""
**Insight:**
- Puncak penyewaan terjadi di Agustus, dengan lonjakan awal musim bersepeda pada Mei 2012. 
Rekomendasi nya melakukan kolaborasi event lokal, prediksi berbasis cuaca, dan kampanye keluarga musiman. Fokus promosi di Mei sebagai pengganti bulan-bulan sepi (Desember–Februari) untuk optimalkan pendapatan.
""")

# Rata-rata penyewaan: libur vs kerja
st.subheader("Rata-Rata Penyewaan: Hari Libur vs Hari Kerja")
hour_df['holiday_type'] = hour_df['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})
holiday_avg = hour_df.groupby(['year', 'holiday_type'])['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=holiday_avg, x='year', y='cnt', hue='holiday_type', palette={'Hari Libur': 'red', 'Hari Kerja': 'blue'}, ax=ax)
st.pyplot(fig)
# insight/penjelasan
st.markdown("""
**Insight:**
- Penyewaan naik signifikan dari 2011 ke 2012, terutama di hari kerja (±62%).
Untuk meningkatkan pendapatan rekomendasinya untuk tambah sepeda saat jam sibuk, 
kerja sama penyediaan jalur commuting, dan tawarkan diskon langganan bagi pekerja/pelajar untuk mendorong penggunaan rutin.
""")

# Per jam: libur vs kerja
st.subheader("Pola Penyewaan per Jam: Hari Libur vs Hari Kerja")
hourly_avg = hour_df.groupby(['hr', 'holiday_type'])['cnt'].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=hourly_avg, x='hr', y='cnt', hue='holiday_type', palette={'Hari Kerja': 'blue', 'Hari Libur': 'red'}, ax=ax)
st.pyplot(fig)
# insight/penjelasan
st.markdown("""
**Insight:**
- Hari kerja menunjukkan dua puncak penyewaan (7–9 & 16–19), 
sementara hari libur lebih merata. Disarankan distribusi sepeda difokuskan ke area komuter saat jam sibuk, sistem harga dinamis, 
serta paket langganan khusus komuter dan rekreasional untuk maksimalkan penggunaan di semua waktu.
""")
