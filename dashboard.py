import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_rfm_df(df):
    last_date = max(df['dteday'])
    rfm = df.groupby(by='registered', as_index=False).agg({
        'dteday': lambda x: (last_date - x.max()).days,
        'instant': 'count',
        'cnt': 'sum'
    })
    rfm.columns = ['registered', 'recency', 'frequency', 'monetary']

    return rfm

dayc_df = pd.read_csv("day_clean.csv")
hourc_df = pd.read_csv("hour_clean.csv")

datetime_columns = ["dteday"]
dayc_df.sort_values(by="dteday", inplace=True)
dayc_df.reset_index(inplace=True)   

hourc_df.sort_values(by="dteday", inplace=True)
hourc_df.reset_index(inplace=True)

for column in datetime_columns:
    dayc_df[column] = pd.to_datetime(dayc_df[column])
    hourc_df[column] = pd.to_datetime(hourc_df[column])

dayc_min_date = dayc_df["dteday"].min()
dayc_max_date = dayc_df["dteday"].max()

hourc_min_date = hourc_df["dteday"].min()
hourc_max_date = hourc_df["dteday"].max()

with st.sidebar:
    st.image("https://storage.googleapis.com/kaggle-datasets-images/130897/312329/20c79bcd928e6d481fca7d5dc9fa3ca4/dataset-cover.jpg?t=2019-05-24-07-06-55")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=dayc_min_date,
        max_value=dayc_max_date,
        value=[dayc_min_date, dayc_max_date])
  
dayc_main_df = dayc_df[(dayc_df["dteday"] >= str(start_date)) & 
                       (dayc_df["dteday"] <= str(end_date))]

hourc_main_df = hourc_df[(hourc_df["dteday"] >= str(start_date)) & 
                        (hourc_df["dteday"] <= str(end_date))]

dayc_df['year'] = dayc_df['dteday'].dt.year
dayc_df['month'] = dayc_df['dteday'].dt.month

rental_bulan = dayc_df.groupby(['year', 'month'])['cnt'].sum().unstack(0)

rental_musim = dayc_df.groupby("season")["cnt"].mean().sort_values()

sepeda_cuaca = hourc_df.groupby("weathersit")["cnt"].mean().sort_values()

rata_jam = hourc_df.groupby("hr")["cnt"].mean()

rfm_df = create_rfm_df(hourc_main_df)

st.title('Bike Sharing Dashboard')

#Plot Tren Penyewaan Sepeda Bulanan
st.subheader('Tren Penyewaan Sepeda Bulanan (2011 vs 2012)')
fig,ax = plt.subplots(figsize=(12,6))
for year in rental_bulan.columns:
    ax.plot(rental_bulan.index, rental_bulan[year], marker='o', label=f"Tahun {year}")
ax.set_xticks(range(1, 13))
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda Bulanan (2011 vs 2012)")
ax.legend(title="Tahun")
ax.grid(True)
st.pyplot(fig)
st.markdown('Berdasarkan grafik, terlihat bahwa tren jumlah penyewaan tahun 2012 meningkat dibandingkan tahun 2011, dan juga bentuk garis pada grafik menunjukkan bahwa penyewaan sepeda ini memiliki pola tren yang konsisten sepanjang tahun.')

# Plot Rata-rata Penyewaan Sepeda Berdasarkan Musim
st.subheader("Rata-Rata Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(rental_musim.index, rental_musim.values, color=['green', 'yellow', 'orange', 'blue'])
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Rata-Rata Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)
st.markdown('Berdasarkan grafik, menunjukkan bahwa musim gugur/fall memiliki jumlah penyewaan sepeda tertinggi, lalu musim semi/spring memiliki jumlah penyewaan sepeda terendah. Sedangkan musim dingin/winter dan musim panas/summer memiliki jumlah penyewaan sepeda yang kurang lebih mirip.')

# Plot Rata-rata Penyewaan Sepeda Berdasarkan Cuaca
st.subheader("Rata-Rata Penyewaan Sepeda Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(sepeda_cuaca.index, sepeda_cuaca.values, color=['green', 'yellow', 'orange', 'blue'])
ax.set_xlabel("Cuaca")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Rata-Rata Penyewaan Sepeda Berdasarkan Cuaca")
st.pyplot(fig)
st.markdown('Berdasarkan grafik, menunjukkan bahwa cuaca cerah/clear mendorong lebih banyak pelanggan untuk menyewa sepeda, kemudian hal ini berbanding lurus menurun dengan cuaca yang buruk. Jadi semakin baik cuaca hari itu, maka semakin banyak juga orang yang menyewa sepeda, begitu sebaliknya. Semakin buruk cuaca hari itu, maka semakin sedikit juga orang yang menyewa sepeda')

# Plot Rata-rata Penyewaan Sepeda per Jam
st.subheader("Rata-Rata Penyewaan Sepeda per Jam dalam Sehari")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(rata_jam.index, rata_jam.values, linestyle="-", color="royalblue", linewidth=2)
ax.set_xticks(range(0, 24))
ax.set_xlabel("Jam Dalam Hari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Rata-Rata Penyewaan Sepeda per Jam dalam Sehari")
ax.grid(True)
st.pyplot(fig)
st.markdown('Pada grafik menunjukkan bahwa terjadi dua lonjakan penyewaan sepeda yang terlihat pada jam 8 pagi dan jam 5-6 sore. Kemudian mulai menurun pada jam 7 malam. Hingga pada jam 5 pagi mulai terjadi pembalikan arah menjadi meningkat.')

st.subheader('Pelanggan Terbaik Berdasarkan RFM Analysis')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Rata-Rata Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Rata-Rata Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = round(rfm_df.monetary.mean(), 3) 
    st.metric("Rata-Rata Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

# Plot Rata-rata Recency
sns.barplot(y="recency", x="registered", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)

# Plot Rata-rata Frequecy
sns.barplot(y="frequency", x="registered", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

# Plot Rata-rata Monetary
sns.barplot(y="monetary", x="registered", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

plt.suptitle("Pelanggan Terbaik Berdasarkan RFM Analysis", fontsize=20)
plt.show()
st.pyplot(fig)
