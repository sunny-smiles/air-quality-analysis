import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

#fungsi untuk menghitung rata-rata harian PM2.5 dan PM10
def create_daily_avg_df(df):
    daily_avg_df = df.resample(rule='D', on='datetime').agg({
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()
    return daily_avg_df

#fungsi untuk menghitung rata-rata bulanan PM2.5 dan PM10
def create_monthly_avg_df(df):
    df['month'] = df['datetime'].dt.month
    monthly_avg_df = df.groupby('month')[['PM2.5', 'PM10']].mean().reset_index()
    return monthly_avg_df

#fungsi untuk menghitung dampak kecepatan angin pada PM2.5 dan PM10
def create_wind_effect_df(df):
    wind_effect_df = df.groupby('WSPM').agg({
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()
    return wind_effect_df

#load data
main_data = pd.read_csv('Dashboard\main_data.csv')

#konversi kolom datetime (memastikan agar berformat datetime)
main_data['datetime'] = pd.to_datetime(main_data['datetime'])

#sidebar untuk memilih rentang waktu
st.sidebar.header("Pengaturan Visualisasi")
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu', min_value=main_data['datetime'].min().date(),
    max_value=main_data['datetime'].max().date(),
    value=[main_data['datetime'].min().date(), main_data['datetime'].max().date()]
)

#filter data berdasarkan rentang waktu
main_df = main_data[(main_data['datetime'] >= pd.to_datetime(start_date)) &
                    (main_data['datetime'] <= pd.to_datetime(end_date))]

#analisis data berdasarkan rentang waktu
daily_avg_df = create_daily_avg_df(main_df)
monthly_avg_df = create_monthly_avg_df(main_df)
wind_effect_df = create_wind_effect_df(main_df)

#header dan deskripsi dashboard
st.header('Dashboard Kualitas Udara')
st.write("Dashboard ini menampilkan analisis kualitas udara berdasarkan data PM2.5, PM10, kecepatan angin (WSPM), dan arah angin (wd).")

#visualisasi 1: rata-rata harian PM2.5 dan PM10
st.subheader('Rata-rata Harian PM2.5 dan PM10')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_avg_df['datetime'], daily_avg_df['PM2.5'], marker='o', color='r', label='PM2.5')
ax.plot(daily_avg_df['datetime'], daily_avg_df['PM10'], marker='o', color='b', label='PM10')
ax.set_title('Rata-rata Harian PM2.5 dan PM10')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Konsentrasi (µg/m³)')
ax.legend()
st.pyplot(fig)

#visualisasi 2: rata-rata bulanan PM2.5 dan PM10
st.subheader('Rata-rata Bulanan PM2.5 dan PM10')
fig2, ax2 = plt.subplots(figsize=(16, 8))
ax2.plot(monthly_avg_df['month'], monthly_avg_df['PM2.5'], marker='o', color='r', label='PM2.5')
ax2.plot(monthly_avg_df['month'], monthly_avg_df['PM10'], marker='o', color='b', label='PM10')
ax2.set_title('Rata-rata Bulanan PM2.5 dan PM10')
ax2.set_xlabel('Bulan')
ax2.set_ylabel('Konsentrasi (µg/m³)')
ax2.legend()
st.pyplot(fig2)

#visualisasi 3: dampak kecepatan angin pada PM2.5 dan PM10
st.subheader('Dampak Kecepatan Angin pada PM2.5 dan PM10')
fig3, ax3 = plt.subplots(figsize=(16, 8))
ax3.plot(wind_effect_df['WSPM'], wind_effect_df['PM2.5'], marker='o', color='r', label='PM2.5')
ax3.plot(wind_effect_df['WSPM'], wind_effect_df['PM10'], marker='o', color='b', label='PM10')
ax3.set_title('Dampak Kecepatan Angin pada PM2.5 dan PM10')
ax3.set_xlabel('Kecepatan Angin (m/s)')
ax3.set_ylabel('Konsentrasi (µg/m³)')
ax3.legend()
st.pyplot(fig3)

#footer
st.caption("Dashboard ini dibuat oleh Fikri Majid untuk memenuhi submission Dicoding")
