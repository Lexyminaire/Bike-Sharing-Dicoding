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

rfm_df = create_rfm_df(hourc_main_df)

dayc_df['year'] = dayc_df['dteday'].dt.year
dayc_df['month'] = dayc_df['dteday'].dt.month

rental_bulan = dayc_df.groupby(['year', 'month'])['cnt'].sum().unstack(0)

rental_musim = dayc_df.groupby("season")["cnt"].mean().sort_values()

sepeda_cuaca = hourc_df.groupby("weathersit")["cnt"].mean().sort_values()

rata_jam = hourc_df.groupby("hr")["cnt"].mean()

st.title('Bike Sharing Dashboard')

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

st.subheader('Rata-Rata Penyewaan Sepeda Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(rental_musim.index, rental_musim.values, color=['green', 'yellow', 'orange', 'blue'])
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Rata-Rata Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

# Plot Rata-rata Penyewaan Sepeda Berdasarkan Musim
st.subheader("Rata-Rata Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(rental_musim.index, rental_musim.values, color=['green', 'yellow', 'orange', 'blue'])
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Rata-Rata Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

# Plot Rata-rata Penyewaan Sepeda Berdasarkan Cuaca
st.subheader("Rata-Rata Penyewaan Sepeda Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(sepeda_cuaca.index, sepeda_cuaca.values, color=['green', 'yellow', 'orange', 'blue'])
ax.set_xlabel("Cuaca")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Rata-Rata Penyewaan Sepeda Berdasarkan Cuaca")
st.pyplot(fig)

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

st.subheader('Best Customer Based on RFM Parameters')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = round(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)
