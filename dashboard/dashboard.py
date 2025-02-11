import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    file_path = "dashboard/data_df.csv" 
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
date_range = st.sidebar.date_input("Pilih Rentang Waktu", [df['dteday'].min(), df['dteday'].max()], min_value=df['dteday'].min(), max_value=df['dteday'].max())
season_filter = st.sidebar.multiselect("Pilih Musim", options=df['season'].unique(), default=df['season'].unique())
weather_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=df['weathersit'].unique(), default=df['weathersit'].unique())

# Filter dataset berdasarkan pilihan pengguna
df_filtered = df[(df['dteday'] >= pd.to_datetime(date_range[0])) &
                 (df['dteday'] <= pd.to_datetime(date_range[1])) &
                 (df['season'].isin(season_filter)) &
                 (df['weathersit'].isin(weather_filter))]

hour_to_day_sum = df_filtered.groupby("dteday").agg({
    "season": "first", 
    "yr": "first",
    "mnth": "first",
    "holiday": "first",
    "weekday": "first",
    "workingday": "first",
    "weathersit": "first",
    "temp": "mean",
    "atemp": "mean",
    "hum": "mean",
    "windspeed": "mean",
    "casual": "sum", 
    "registered": "sum",
    "cnt": "sum"  
}).reset_index()
sum_to_day = df_filtered.groupby('dteday').sum()

st.title("Dashboard Analisis Sepeda Penggunaan Sepeda")
st.text("Dashboard Visualisasi Analisis Penggunaan Sepeda")
st.subheader('Pengguna')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Keseluruhan", value=df_filtered['cnt'].sum())
with col2:
    st.metric("Casual", value=df_filtered['casual'].sum())
with col3:
    st.metric("Registered", value=df_filtered['registered'].sum())


# 1. Rata-rata pengguna berdasarkan kondisi cuaca 
st.subheader("Rata-rata Pengguna berdasarkan Kondisi Cuaca")
avg_users_weather = df_filtered.groupby(["dteday", "weathersit"])["cnt"].sum().groupby("weathersit").mean().reset_index()
st.bar_chart(avg_users_weather.set_index("weathersit"))

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tertinggi", value=round(avg_users_weather['cnt'].max()))
with col2:
    st.metric("Rata-Rata", value=round(avg_users_weather['cnt'].mean()))
with col3:
    st.metric("Terendah", value=round(avg_users_weather['cnt'].min()))



# 2. Rata-rata pengguna berdasarkan musim 
st.subheader("Rata-rata Pengguna berdasarkan Musim")
avg_users_season = df_filtered.groupby(["dteday","season"])["cnt"].sum().groupby("season").mean().reset_index()
st.bar_chart(avg_users_season.set_index("season"))
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tertinggi", value=round(avg_users_season['cnt'].max()))
with col2:
    st.metric("Rata-Rata", value=round(avg_users_season['cnt'].mean()))
with col3:
    st.metric("Terendah", value=round(avg_users_season['cnt'].min()))


# 3. Rata-rata pengguna berdasarkan suhu, kelembaban, dan suhu terasa
st.subheader("Rata-rata Pengguna dalam Kondisi Suhu")
st.scatter_chart(hour_to_day_sum, x="temp", y="cnt",x_label='Temperatur')
st.subheader("Rata-rata Pengguna dalam Kondisi Atemp ")
st.scatter_chart(hour_to_day_sum, x="atemp", y="cnt",x_label='ATEMP')
st.subheader("Rata-rata Pengguna dalam Kondisi Humidity")
st.scatter_chart(hour_to_day_sum, x="hum", y="cnt",x_label="Humadity")

# 4. Hubungan cuaca, suhu, dan jumlah peminjaman
st.subheader("Hubungan Cuaca, Suhu, dan Jumlah Peminjaman")
st.dataframe(df_filtered[['temp', 'atemp', 'hum', 'cnt']].corr())

# 5. Perbandingan jumlah peminjaman berdasarkan Musim & Cuaca
st.subheader("Perbandingan Jumlah Peminjaman berdasarkan Musim & Cuaca")
season_weather_avg = df_filtered.groupby(["dteday","season", "weathersit"])["cnt"].sum().groupby(["season","weathersit"]).mean().reset_index()
season_weather_pivot = season_weather_avg.pivot(index="season", columns="weathersit", values="cnt").fillna(0)
st.bar_chart(season_weather_pivot)

# 6. Rata-rata pengguna dalam 1 hari (Total, Casual, Registered)
st.subheader("Rata-rata Pengguna dalam 1 Hari")
st.line_chart(df_filtered.groupby('hr')[['casual', 'registered', 'cnt']].mean())

# 7. Rata-rata pengguna berdasarkan hari dalam seminggu
st.subheader("Rata-rata Pengguna berdasarkan Hari dalam Seminggu")
st.bar_chart(df_filtered.groupby('weekday')['cnt'].mean())

# 8. Pola peminjaman antara hari kerja dan akhir pekan
st.subheader("Pola Peminjaman antara Hari Kerja dan Akhir Pekan")

fig, ax = plt.subplots()
sns.barplot(data=df_filtered, x="workingday", y="cnt", ax=ax)
ax.set_xticklabels(["Akhir Pekan", "Hari Kerja"])
ax.set_xlabel("Jenis Hari")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)
