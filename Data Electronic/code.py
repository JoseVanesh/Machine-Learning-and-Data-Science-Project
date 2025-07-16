import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Memuat Data
print("=== MEMUAT DATA ===")
try:
    df = pd.read_csv('electronic_sales.csv', parse_dates=['Tanggal'])
    print("Data berhasil dimuat!")
    print(f"Jumlah record: {len(df)}")
except FileNotFoundError:
    print("File 'electronic_sales.csv' tidak ditemukan")
    exit()

# 2. Membersihkan Data
print("\n=== MEMBERSIHKAN DATA ===")
print("Data sebelum pembersihan:")
print(df.info())

# Handle missing values
df['Harga'].fillna(df['Harga'].median(), inplace=True)
df['Kuantitas'].fillna(1, inplace=True)
df['Kategori'].fillna('Lainnya', inplace=True)

# Buat kolom baru
df['Total'] = df['Harga'] * df['Kuantitas']
df['Bulan'] = df['Tanggal'].dt.month_name()
df['Tahun'] = df['Tanggal'].dt.year

print("\nData setelah pembersihan:")
print(df.info())

# 3. Analisis Data
print("\n=== ANALISIS DATA ===")

# Statistik dasar
print("\nStatistik Penjualan:")
print(df[['Harga', 'Kuantitas', 'Total']].describe())

# Penjualan per kategori
print("\nPenjualan per Kategori:")
kategori_sales = df.groupby('Kategori')['Total'].sum().sort_values(ascending=False)
print(kategori_sales)

# Tren bulanan
print("\nTren Penjualan Bulanan:")
monthly_sales = df.groupby(['Tahun', 'Bulan'])['Total'].sum().unstack()
print(monthly_sales)

# 4. Visualisasi Data
plt.style.use('ggplot')
plt.figure(figsize=(15, 12))

# Grafik 1: Distribusi Harga Produk
plt.subplot(2, 2, 1)
plt.hist(df['Harga'], bins=15, color='royalblue', edgecolor='black')
plt.title('Distribusi Harga Produk')
plt.xlabel('Harga (Rp)')
plt.ylabel('Jumlah Produk')
plt.grid(True, linestyle='--', alpha=0.6)

# Grafik 2: Penjualan per Kategori
plt.subplot(2, 2, 2)
kategori_sales.plot(kind='bar', color='forestgreen')
plt.title('Total Penjualan per Kategori')
plt.xlabel('Kategori Produk')
plt.ylabel('Total Penjualan (Rp)')
plt.xticks(rotation=45)
plt.grid(True, axis='y', linestyle='--', alpha=0.6)

# Grafik 3: Tren Bulanan
plt.subplot(2, 2, 3)
months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December']
monthly_sales.T.plot(marker='o', linewidth=2)
plt.title('Tren Penjualan Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Total Penjualan (Rp)')
plt.xticks(np.arange(12), months_order, rotation=45)
plt.legend(title='Tahun')
plt.grid(True, linestyle='--', alpha=0.6)

# Grafik 4: Scatter Harga vs Kuantitas
plt.subplot(2, 2, 4)
plt.scatter(df['Harga'], df['Kuantitas'], alpha=0.6, color='coral')
plt.title('Hubungan Harga dan Kuantitas Penjualan')
plt.xlabel('Harga Produk (Rp)')
plt.ylabel('Kuantitas Terjual')
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

# Grafik Tambahan: Pie Chart Market Share
plt.figure(figsize=(8, 8))
kategori_sales.plot(kind='pie', autopct='%1.1f%%', 
                   startangle=90, shadow=True,
                   colors=['gold', 'lightcoral', 'lightskyblue', 'lightgreen'])
plt.title('Market Share per Kategori Produk')
plt.ylabel('')
plt.show()

# 5. Menyimpan Hasil
df.to_csv('cleaned_electronic_sales.csv', index=False)
print("\nData yang sudah dibersihkan disimpan sebagai 'cleaned_electronic_sales.csv'")