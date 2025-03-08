# Submission Dicoding " Belajar Analisis Data dengan Python " ✨

Proyek ini bertujuan untuk menganalisis data Bike Sharing. Hal ini digunakan untuk memahami faktor-faktor yang dapat mempengaruhi penyewaan sepeda, seperti waktu, cuaca, dll.

## 📂 Dataset

Dataset yang digunakan tersimpan dalam folder data yang berisi:

- day.csv: Data penyewaan sepeda per hari.
- hour.csv: Data penyewaan sepeda per jam.

## Setup Environment

### Setup anaconda

```plaintext
conda create --name main-ds python=3.13.2
conda activate main-ds
pip install -r requirements.txt
```

### Setup Shell / Terminal

```
mkdir bike_sharing_analysis
cd bike_sharing_analysis
pipenv install
pipenv shell
pip install -r requirements.txt
```

### Menjalankan Dashboard

```
streamlit run dashboard.py
```
