import threading
import requests
from faker import Faker
import random
import string,sqlite3,hashlib

def generate_password(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

fake = Faker()
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

con = sqlite3.connect("mydatabase.db")
cursor = con.cursor()

for brans in tıp_branşları:
    for i in range(2):
        name = fake.name().split(" ")[0]
        surname = fake.name().split(" ")[1]
        email = fake.email()
        username = fake.user_name()
        birthdate = "1998-08-08"
        password = hashlib.sha256("123456".encode()).hexdigest() 
        gender = "man"
        phone = fake.phone_number()
        address = fake.address()
        hospital = "cerrahpaşa"
        
        
        cursor.execute("INSERT INTO doctors(name,surname,email,username,password,birthdate,gender,phone,address,department,hospital) VALUES (?,?,?,?,?,?,?,?,?,?,?)",(name,surname,email,username,password,birthdate,gender,phone,address,brans,hospital))



con.commit()



    