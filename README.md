# Proyek Analisis DataSet [ Bike Sharing Dataset ]

## Deskripsi : 
Bertujuan untuk menganalisis dataset yang ada di Bike Sharing (day_df & hour_df) menggunakan teknik-teknik analisis data dan visualisasi data. Serta pembuatan Dashboard menggunakan < Streamlitt > untuk menampilkan web interaktif. 

---

## Struktur Folder
```
analisis-bike-dataset
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt
```

## Libary
```
streamlit==1.41.1
pandas==2.2.3
seaborn==0.13.2
matplotlib==3.9.3
```

### Cara Menjalankan Dashboard / Streamlit
---

### 1. Mendownload & Clone Repository Ke Local Env
### 2. Instalasi Libary yang diperlukan 
```
pip install -r requirements.txt
```
### 3. Menjalankan Dashboard
```bash
streamlit run dashboard/dashboard.py
```
### 4. Akses Dashboard Menggunakan URL yang ada di terminal 'http://localhost:8501'
