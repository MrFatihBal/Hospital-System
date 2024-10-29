import threading
import requests
from faker import Faker
import random
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


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


def send_request(session,index):
    fake = Faker()

    for i in range(random.randint(1,5)):
        data = {
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "birthdate": fake.date_of_birth(minimum_age=25, maximum_age=70).strftime('%d-%m-%Y'),
            "gender": random.choice(["Erkek", "Kadın","Non-Binary","Transgender","Atak Helikopteri"]),
            "phone": generate_password(20),
            "address": fake.address(),
        }
        response = session.post("http://localhost:3000/userregister", data=data)
        print(response.status_code)

with requests.Session() as ses:
    threads = []
    
    for i in range(len(tıp_branşları)):
        t = threading.Thread(target=send_request,args=(ses,i))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
        
# cur.execute("INSERT INTO admins(name,surname,password,birthdate,gender,phone,address) VALUES (?,?,?,?,?,?,?)",("admin","admin","admin","admin","admin","admin","admin"))
# c.commit()
# c.close()
    