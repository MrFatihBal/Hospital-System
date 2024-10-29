import sqlite3
from datetime import datetime, timedelta

tıp_branşları = [
    "Anatomi",
    "Biyofizik",
    "Tıbbi Biyoloji",
    "Tıp Eğitimi",
    "Tıp Etiği ve Tıp Tarihi",
    "İmmünoloji",
    "Fizyoloji",
    "Histoloji ve Embriyoloji",
    "Tıbbi Mikrobiyoloji",
    "Tıp Bilişimi",
    "Tıbbi Biyokimya",
    "Dahili Tıp Bilimleri",
    "Acil Tıp",
    "Adli Tıp",
    "Çocuk Ruh Sağlığı",
    "Çocuk Sağlığı ve Hastalıkları",
    "Dermatoloji",
    "Enfeksiyon Hastalıkları",
    "Fiziksel Tıp ve Rehabilitasyon",
    "Göğüs Hastalıkları",
    "Halk Sağlığı",
    "İç Hastalıkları",
    "Kardiyoloji",
    "Nöroloji",
    "Nükleer Tıp",
    "Radyasyon Onkolojisi",
    "Radyoloji",
    "Psikiyatri",
    "Tıbbi Farmakoloji",
    "Tıbbi Genetik",
    "Cerrahi Tıp Bilimleri",
    "Anestezi ve Reanimasyon",
    "Beyin ve Sinir Cerrahisi",
    "Çocuk Cerrahisi",
    "Genel Cerrahi",
    "Kalp ve Damar Cerrahisi",
    "Göğüs Cerrahisi",
    "Göz Hastalıkları",
    "Kadın Hastalıkları ve Doğum",
    "Kulak Burun Boğaz",
    "Ortopedi ve Travmatoloji",
    "Tıbbi Patoloji",
    "Üroloji",
    "Plastik Rekonstrüktif ve Estetik Cerrahi"
]

clocks = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

con =sqlite3.connect("mydatabase.db")
cursor = con.cursor()

baslangic_tarihi = datetime.strptime("01-05-2024", "%d-%m-%Y")
bitis_tarihi = datetime.strptime("01-01-2025", "%d-%m-%Y")


mevcut_tarih = baslangic_tarihi

cursor.execute("SELECT doctorID from doctors")
ids = []
data = cursor.fetchall()
for i in data:
    ids.append(i[0])
    print(i)
    
    
while mevcut_tarih <= bitis_tarihi:
    for clock in clocks:
        tarih = mevcut_tarih.strftime("%d-%m-%Y")
        for i in ids:
            cursor.execute("INSERT INTO appointments(patientID,doctorID,appointment_date,appointment_time,appointment_details,granted) VALUES (?,?,?,?,?,?)",
                (0,i,tarih,clock," ",0))
        
    
    mevcut_tarih += timedelta(days=1)
    print(mevcut_tarih)
    
con.commit()