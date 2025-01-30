import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# df = pd.read_csv("main_data.csv")

dir_name = '.'
dataframes = []
for filename in os.listdir(dir_name):
    if filename.endswith('.csv'):
        df = pd.read_csv(os.path.join(filename))
        dataframes.append(df)

df = pd.concat(dataframes, ignore_index=True)

df['created_at'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
df['created_at'] = pd.to_datetime(df['created_at'])

# Mengurutkan data berdasarkan tanggal
df.sort_values(by="created_at", inplace=True)
df.reset_index(inplace=True)

# Filter data
min_date = df["created_at"].min()
max_date = df["created_at"].max()

# Membuat sidebar untuk penyaringan tanggal awal dan akhir
with st.sidebar:
   # Menambahkan logo
   st.image("images.jpg")
   
   # Mengambil start_date & end_date dari date_input
   start_date, end_date = st.date_input(
       label='Rentang Waktu',min_value=min_date,
       max_value=max_date,
       value=[min_date, max_date]
   )

   feature = st.selectbox(
           label= 'Pilih metrik kualitas udara',
           options=('O3', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM')

   )

main_df = df[(df["created_at"] >= str(start_date)) & (df["created_at"] <= str(end_date))]

# feature = 'CO'
mean_ozone_per_year = main_df.groupby('year')[feature].mean().reset_index()
mean_ozone_per_month = main_df.groupby('year_month')[feature].mean().reset_index()
min_ozone_per_station = main_df.groupby('station')[feature].min().reset_index()
max_ozone_per_station = main_df.groupby('station')[feature].max().reset_index()
mean_ozone_per_station = main_df.groupby('station')[feature].mean().reset_index()
temp_per_year = df.groupby(['station', 'year'])[feature].mean().reset_index()
numeric_df = df[[feature, 'TEMP', 'PRES', 'DEWP', 'RAIN']]
corr_matrix = numeric_df.corr()

st.header(f'Dashboard Kualitas %s di Udara :sparkles:' % feature)
st.subheader(f'Kualitas %s Per Tahun' % feature)

col1, col2 = st.columns(2)

with col1:
    st.metric("Minimum", value= mean_ozone_per_year[feature].min())

with col2:
    st.metric("Maksimum", value= mean_ozone_per_year[feature].max())

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(mean_ozone_per_year['year'], mean_ozone_per_year[feature], marker='o', linestyle='-')
plt.title(f'Rata-rata %s per Tahun' % feature)
plt.xlabel('Tahun')
plt.ylabel(f'Rata-rata %s' % feature)
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
st.pyplot(fig)

st.subheader(f'Kualitas %s Per Bulan' % feature)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(mean_ozone_per_month['year_month'], mean_ozone_per_month[feature], marker='o', linestyle='-')
plt.title(f'Rata-rata %s per Bulan' % feature)
plt.xlabel('Tahun Bulan')
plt.ylabel(f'Rata-rata %s' % feature)
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
st.pyplot(fig)

st.subheader(f'Minimum, Maksimum, dan Rata-rata %s Per Station' % feature)

fig, ax = plt.subplots(figsize=(12, 6))
plt.barh(min_ozone_per_station['station'], min_ozone_per_station[feature], color='skyblue')
plt.xlabel('Station')
plt.ylabel(f'Minimum %s' % feature)
plt.title(f'Minimum %s per Station' % feature)
plt.xticks(rotation=90)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
plt.barh(max_ozone_per_station['station'], min_ozone_per_station[feature], color='skyblue')
plt.xlabel('Station')
plt.ylabel(f'Maksimum %s' % feature)
plt.title(f'Maksimum %s per Station' % feature)
plt.xticks(rotation=90)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
plt.barh(mean_ozone_per_station['station'], mean_ozone_per_station[feature], color='skyblue')
plt.xlabel('Station')
plt.ylabel(f'Rata-rata %s' % feature)
plt.title(f'Rata-rata %s per Station' % feature)
plt.xticks(rotation=90)
st.pyplot(fig)

st.subheader(f'Rata-rata %s per Tahun per Station' % feature)
fig, ax = plt.subplots(figsize=(14, 7))
sns.lineplot(data=temp_per_year, x='year', y=feature, hue='station', marker='o')
plt.title('Rata-rata ' + feature + ' per Tahun per Stasiun')
plt.xlabel('Tahun')
plt.ylabel('Rata-rata ' + feature)
plt.legend(title='Stasiun')
plt.grid(True)
st.pyplot(fig)

st.subheader('Heatmap Meteorologi dengan Metrik Kualitas Udara')
fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title(f'Heatmap Metrik %s dengan TEMP, PRES, DEWP, dan RAIN' % feature)
st.pyplot(fig)
