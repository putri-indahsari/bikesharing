import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Penyewaan Sepeda",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv('day.csv')
    hour_df = pd.read_csv('hour.csv')
    return day_df, hour_df

day_df, hour_df = load_data()

# Set style
sns.set_style("whitegrid")
plt.style.use('seaborn')

# CSS Custom
st.markdown("""
    <style>
        .main-title {
            font-size: 36px !important;
            color: #2c3e50;
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 2px solid #3498db;
        }
        .section-header {
            color: #3498db;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
            margin-top: 30px !important;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stPlot {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Judul utama
st.markdown('<h1 class="main-title">🚴 Dashboard Analisis Penyewaan Sepeda (2011–2012)</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Filter Data")
    selected_years = st.multiselect(
        "Pilih Tahun",
        options=['2011', '2012'],
        default=['2011', '2012']
    )
    
    st.markdown("---")
    st.markdown("""
    **Informasi Dataset:**
    - Data harian: {} baris
    - Data per jam: {} baris
    - Sumber: Capital Bikeshare
    """.format(len(day_df), len(hour_df)))

# Pra-pemrosesan data
day_df['season_name'] = day_df['season'].map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
day_df['year'] = day_df['yr'].map({0: '2011', 1: '2012'})
day_df['workingday_label'] = day_df['workingday'].map({0: 'Libur', 1: 'Hari Kerja'})
day_df['weather_label'] = day_df['weathersit'].map({
    1: 'Cerah',
    2: 'Berkabut',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
})

hour_df['year'] = hour_df['yr'].map({0: 2011, 1: 2012})
hour_df['holiday_type'] = hour_df['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})

# Filter data berdasarkan tahun yang dipilih
year_filter = [0 if '2011' in selected_years else None, 1 if '2012' in selected_years else None]
year_filter = [x for x in year_filter if x is not None]

if year_filter:
    day_df = day_df[day_df['yr'].isin(year_filter)]
    hour_df = hour_df[hour_df['yr'].isin(year_filter)]

# ===============================
# METRICS UTAMA
# ===============================
st.markdown("### 📊 Ringkasan Utama")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Penyewaan", f"{day_df['cnt'].sum():,}")

with col2:
    avg_rental = day_df['cnt'].mean()
    st.metric("Rata-rata Harian", f"{avg_rental:,.0f}")

with col3:
    max_day = day_df.loc[day_df['cnt'].idxmax()]
    st.metric("Hari Puncak", f"{max_day['cnt']:,}", 
              f"{max_day['dteday']} ({max_day['season_name']})")

with col4:
    min_day = day_df.loc[day_df['cnt'].idxmin()]
    st.metric("Hari Terendah", f"{min_day['cnt']:,}", 
              f"{min_day['dteday']} ({min_day['season_name']})")

# ===============================
# PERTANYAAN BISNIS 1
# ===============================
st.markdown('<h2 class="section-header">❄️ vs ☀️ Perbandingan Musim</h2>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Analisis Musim", "Kondisi Cuaca", "Pola Harian"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Penyewaan per Musim")
        seasonal_avg = day_df.groupby(['year', 'season_name'])['cnt'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(
            x='season_name', 
            y='cnt', 
            hue='year', 
            data=seasonal_avg,
            order=['Winter', 'Spring', 'Summer', 'Fall'],
            palette='coolwarm',
            ax=ax
        )
        ax.set_title('Rata-Rata Penyewaan per Musim')
        ax.set_xlabel('Musim')
        ax.set_ylabel('Penyewaan')
        st.pyplot(fig)
        
    with col2:
        st.subheader("Perbandingan Suhu & Kelembapan")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        sns.barplot(
            data=day_df, 
            x='season_name', 
            y='temp', 
            order=['Winter', 'Spring', 'Summer', 'Fall'],
            palette='coolwarm',
            ax=ax1
        )
        ax1.set_title('Rata-Rata Suhu')
        ax1.set_xlabel('Musim')
        ax1.set_ylabel('Suhu (normalisasi)')
        
        sns.barplot(
            data=day_df, 
            x='season_name', 
            y='hum', 
            order=['Winter', 'Spring', 'Summer', 'Fall'],
            palette='coolwarm',
            ax=ax2
        )
        ax2.set_title('Rata-Rata Kelembapan')
        ax2.set_xlabel('Musim')
        ax2.set_ylabel('Kelembapan (normalisasi)')
        
        plt.tight_layout()
        st.pyplot(fig)

with tab2:
    st.subheader("Pengaruh Cuaca terhadap Penyewaan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(
        data=day_df,
        x='weather_label',
        y='cnt',
        hue='season_name',
        palette='coolwarm',
        order=['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Lebat'],
        ax=ax
    )
    ax.set_title('Distribusi Penyewaan berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.legend(title='Musim')
    st.pyplot(fig)

with tab3:
    st.subheader("Pola Penyewaan: Hari Kerja vs Libur")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=day_df,
        x='workingday_label',
        y='cnt',
        hue='season_name',
        palette='coolwarm',
        ax=ax
    )
    ax.set_title('Rata-Rata Penyewaan: Hari Kerja vs Libur')
    ax.set_xlabel('')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

# ===============================
# PERTANYAAN BISNIS 2
# ===============================
st.markdown('<h2 class="section-header">🎉 Pengaruh Hari Libur</h2>', unsafe_allow_html=True)

tab4, tab5 = st.tabs(["Analisis Temporal", "Perbandingan Hari"])

with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pola Harian di Hari Libur")
        holiday_hourly = hour_df[hour_df['holiday'] == 1]
        hourly_avg = holiday_hourly.groupby(['hr', 'year'])['cnt'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(
            data=hourly_avg, 
            x='hr', 
            y='cnt', 
            hue='year', 
            palette={2011: '#3498db', 2012: '#e74c3c'},
            marker='o',
            ax=ax
        )
        ax.set_title('Pola Penyewaan per Jam di Hari Libur')
        ax.set_xlabel('Jam (0-23)')
        ax.set_ylabel('Rata-Rata Penyewaan')
        ax.set_xticks(range(0, 24, 2))
        st.pyplot(fig)
        
    with col2:
        st.subheader("Pola Bulanan di Hari Libur")
        day_df['month'] = day_df['mnth']
        holiday_monthly = day_df[day_df['holiday'] == 1]
        monthly_avg = holiday_monthly.groupby(['month', 'year'])['cnt'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(
            data=monthly_avg, 
            x='month', 
            y='cnt', 
            hue='year', 
            palette={2011: '#3498db', 2012: '#e74c3c'},
            marker='o',
            ax=ax
        )
        ax.set_title('Pola Penyewaan per Bulan di Hari Libur')
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Rata-Rata Penyewaan')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
        st.pyplot(fig)

with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Perbandingan Hari Libur vs Kerja")
        holiday_avg = hour_df.groupby(['year', 'holiday_type'])['cnt'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(
            data=holiday_avg, 
            x='year', 
            y='cnt', 
            hue='holiday_type', 
            palette={'Hari Libur': '#e74c3c', 'Hari Kerja': '#3498db'},
            ax=ax
        )
        ax.set_title('Rata-Rata Penyewaan: Hari Libur vs Kerja')
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Rata-Rata Penyewaan')
        st.pyplot(fig)
        
    with col2:
        st.subheader("Pola Harian: Libur vs Kerja")
        hourly_avg = hour_df.groupby(['hr', 'holiday_type'])['cnt'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(
            data=hourly_avg, 
            x='hr', 
            y='cnt', 
            hue='holiday_type', 
            palette={'Hari Kerja': '#3498db', 'Hari Libur': '#e74c3c'},
            ax=ax
        )
        ax.set_title('Pola Penyewaan per Jam: Libur vs Kerja')
        ax.set_xlabel('Jam (0-23)')
        ax.set_ylabel('Rata-Rata Penyewaan')
        ax.set_xticks(range(0, 24, 2))
        st.pyplot(fig)

# ===============================
# KESIMPULAN
# ===============================
st.markdown('<h2 class="section-header">📝 Kesimpulan & Insight</h2>', unsafe_allow_html=True)

with st.expander("Kesimpulan Analisis Musim"):
    st.write("""
    1. **Pola Musiman Kuat**: Penyewaan tertinggi di musim panas (summer) dan terendah di musim dingin (winter)
    2. **Peningkatan Tahun 2012**: Terjadi peningkatan signifikan dari 2011 ke 2012 di semua musim
    3. **Pengaruh Cuaca**: Kondisi cerah mendominasi penyewaan tinggi, terutama di musim panas
    4. **Pola Harian**: Hari kerja memiliki pola penyewaan lebih tinggi dibanding hari libur
    """)

with st.expander("Kesimpulan Analisis Hari Libur"):
    st.write("""
    1. **Pola Berbeda**: Hari libur menunjukkan pola penyewaan yang berbeda dengan hari kerja
    2. **Puncak Siang Hari**: Penyewaan di hari libur cenderung memuncak di siang hari (12-15)
    3. **Musiman Liburan**: Bulan-bulan liburan (Juni-Agustus) menunjukkan aktivitas penyewaan tinggi
    4. **Frekuensi Lebih Rendah**: Rata-rata penyewaan di hari libur lebih rendah dibanding hari kerja
    """)
