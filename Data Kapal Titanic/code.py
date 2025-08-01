import pandas as pd
import matplotlib.pyplot as plt

# 1. Memuat Data
try:
    df = pd.read_csv('titanic.csv')
    print("Data berhasil dimuat!")
    print(f"Jumlah penumpang: {len(df)}")
except FileNotFoundError:
    print("File 'titanic.csv' tidak ditemukan")
    exit()

# 2. Membersihkan Data
print("\n=== Sebelum Pembersihan ===")
print("Data kosong per kolom:")
print(df.isnull().sum())

# Mengisi nilai yang kosong
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
df['Cabin'].fillna('Tidak Diketahui', inplace=True)

print("\n=== Setelah Pembersihan ===")
print("Data kosong per kolom:")
print(df.isnull().sum())

# 3. Analisis Data
print("\n=== Hasil Analisis ===")

# Statistik dasar
print("\nStatistik Umum:")
print(df.describe())

# Tingkat kelangsungan hidup
total_survived = df['Survived'].sum()
survival_rate = (total_survived / len(df)) * 100
print(f"\nTotal yang selamat: {total_survived} ({survival_rate:.1f}%)")

# Kelangsungan hidup berdasarkan gender
gender_survival = df.groupby('Sex')['Survived'].mean() * 100
print("\nKelangsungan hidup berdasarkan gender:")
print(gender_survival)

# Kelangsungan hidup berdasarkan kelas
class_survival = df.groupby('Pclass')['Survived'].mean() * 100
print("\nKelangsungan hidup berdasarkan kelas:")
print(class_survival)

# 4. Visualisasi Data
plt.figure(figsize=(15, 12))

# Grafik 1: Distribusi Usia
plt.subplot(2, 2, 1)
plt.hist(df['Age'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribusi Usia Penumpang')
plt.xlabel('Usia')
plt.ylabel('Jumlah Penumpang')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Grafik 2: Kelangsungan hidup berdasarkan gender
plt.subplot(2, 2, 2)
gender_counts = df['Sex'].value_counts()
gender_survived = df[df['Survived'] == 1]['Sex'].value_counts()
gender_not_survived = gender_counts - gender_survived

plt.bar(['Laki-laki', 'Perempuan'], gender_not_survived, 
        color='lightcoral', label='Tidak Selamat')
plt.bar(['Laki-laki', 'Perempuan'], gender_survived, 
        bottom=gender_not_survived, color='lightgreen', label='Selamat')

plt.title('Kelangsungan Hidup Berdasarkan Gender')
plt.xlabel('Gender')
plt.ylabel('Jumlah Penumpang')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Grafik 3: Kelangsungan hidup berdasarkan kelas
plt.subplot(2, 2, 3)
class_survival = df.groupby('Pclass')['Survived'].mean() * 100
plt.bar(['Kelas 1', 'Kelas 2', 'Kelas 3'], class_survival, 
        color=['gold', 'silver', 'brown'])
plt.title('Persentase Selamat Berdasarkan Kelas')
plt.xlabel('Kelas Tiket')
plt.ylabel('Persentase Selamat (%)')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Grafik 4: Distribusi usia berdasarkan kelangsungan hidup
plt.subplot(2, 2, 4)
survived = df[df['Survived'] == 1]['Age']
not_survived = df[df['Survived'] == 0]['Age']

plt.hist([survived, not_survived], bins=15, 
         color=['lightgreen', 'lightcoral'], 
         label=['Selamat', 'Tidak Selamat'],
         stacked=True)
plt.title('Distribusi Usia Berdasarkan Kelangsungan Hidup')
plt.xlabel('Usia')
plt.ylabel('Jumlah Penumpang')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# Grafik tambahan: Kelangsungan hidup berdasarkan usia
plt.figure(figsize=(10, 6))
age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
age_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80']
df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)

age_survival = df.groupby('AgeGroup')['Survived'].mean() * 100
plt.plot(age_labels, age_survival, marker='o', 
         color='blue', linestyle='-', linewidth=2)
plt.title('Tingkat Kelangsungan Hidup Berdasarkan Kelompok Usia')
plt.xlabel('Kelompok Usia')
plt.ylabel('Persentase Selamat (%)')
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# Simpan data yang sudah dibersihkan
df.to_csv('titanic_clean.csv', index=False)
print("\nData yang sudah dibersihkan disimpan sebagai 'titanic_clean.csv'")