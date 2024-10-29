from flask import  Flask,url_for,redirect,flash,render_template,request,session
import sqlite3,random,string,datetime,hashlib
from functools import wraps

from flask_wtf.csrf import CSRFProtect

import base64
from flask_apscheduler import APScheduler

scheduler = APScheduler()

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


app = Flask(__name__)
# csrf = CSRFProtect(app)

app.secret_key = "sdfjnnjfdsnjfdfdsjdfsnsfjnsjndfnjdfsnjdsfjkdwdaskadskmd"
app.config["SCHEDULER_API_ENABLED"] = True
scheduler.init_app(app)

con = sqlite3.connect("mydatabase.db")
cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS patients (patientID INTEGER PRIMARY KEY,name TEXT,surname TEXT,username TEXT,email TEXT,password TEXT,birthdate TEXT,gender TEXT,phone TEXT,address TEXT)")
con.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS doctors (doctorID INTEGER PRIMARY KEY,name TEXT,surname TEXT,email TEXT,username TEXT,password TEXT,birthdate TEXT,gender TEXT,phone TEXT,address TEXT,department TEXT,hospital TEXT)")
con.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS admins (adminID INTEGER PRIMARY KEY,name TEXT,surname TEXT,email TEXT,password TEXT,birthdate TEXT,gender TEXT,phone TEXT,address TEXT)")
con.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS appointments (appointmentID INTEGER PRIMARY KEY,patientID INTEGER,doctorID INTEGER,appointment_date TEXT,appointment_time TEXT,appointment_details TEXT,granted TEXT,FOREIGN KEY (patientID) REFERENCES doctors(patientID),FOREIGN KEY (doctorID) REFERENCES doctors(doctorID))")
con.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS medical_reports (reportID INTEGER PRIMARY KEY,patientID INTEGER,doctorID INTEGER,report_date TEXT,report_time TEXT,report_content TEXT,URL VARCHAR(255),FOREIGN KEY (patientID) REFERENCES patients(patientID),FOREIGN KEY (doctorID) REFERENCES doctors(doctorID))")
con.commit()
con.close()

@app.template_filter('get_index')
def get_index(lst, idx):
    return lst[idx]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntelemek için admin girişi yapın","info")
            return redirect(url_for("index"))
    return decorated_function



def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "patientID" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntelemek için giriş yapın","info")
            return redirect(url_for("index"))
    return decorated_function

def doctor_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "doctorID" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntelemek için admin girişi yapın","info")
            return redirect(url_for("index"))
    return decorated_function


def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "adminID" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntelemek için admin girişi yapın","info")
            return redirect(url_for("index"))
    return decorated_function


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/userregister",methods=["GET","POST"])
def userregister():
    if request.method=="GET":
        return render_template("userregister.html")
    elif request.method=="POST":
        
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("emailhead") + "@" + request.form.get("emailbottom")
        username = request.form.get("username")
        password = hashlib.sha256(request.form.get("password").encode()).hexdigest()
        birthdate = request.form.get("birthdate")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        address = request.form.get("address")
       
        
        
        con = sqlite3.connect("mydatabase.db")
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM patients WHERE username=?",(username,))
        if(len(cursor.fetchall())>0):
            flash("Bu kullanıcı adı daha önce kullanılmıştır","danger")
            return redirect(url_for("userregister"))
        
        cursor.execute("SELECT * FROM patients WHERE phone=?",(phone,))
        if(len(cursor.fetchall())>0):
            flash("Bu telefon daha önce kullanılmıştır","danger")
            return redirect(url_for("userregister"))
        
        cursor = con.cursor()
        cursor.execute("INSERT INTO patients (name, surname, email, username, password, birthdate, gender, phone, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, surname, email, username, password, birthdate, gender, phone, address))
        con.commit()
        
        flash(f"Kullanici olusturuldu, sifre:{password} ","success")
        
        return redirect(url_for("index"))


@app.route("/doctorregister",methods=["GET","POST"])
@admin_login_required
def doctorregister():
    if request.method=="GET":
        return render_template("doctorregister.html")
    elif request.method=="POST":
        
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("emailhead") + "@" + request.form.get("emailbottom")
        username = request.form.get("username")
        password = hashlib.sha256(request.form.get("password").encode()).hexdigest()
        birthdate = request.form.get("birthdate")
        gender = request.form.get("gender")
        department = request.form.get("profession")
        phone = request.form.get("phone")
        address = request.form.get("address")
        hospital = request.form.get("hospital")
        
        
        conn = sqlite3.connect('mydatabase.db')  # Veritabanı adını ve yolunu değiştirin
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM doctors WHERE phone=?",(phone,))
        if(len(cursor.fetchall())>0):
            flash("Bu telefon numarası daha önce kullanılmıştır","danger")
            return redirect(url_for("doctorregister"))
        
        cursor.execute("SELECT * FROM doctors WHERE username=?",(phone,))
        if(len(cursor.fetchall())>0):
            flash("Bu kullanıcı adı daha önce kullanılmıştır","danger")
            return redirect(url_for("doctorregister"))

        cursor.execute("INSERT INTO doctors (name, surname, email, username, password, birthdate, gender, department, phone, address, hospital) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, surname, email, username, password, birthdate, gender, department, phone, address, hospital))
        conn.commit()
        
        
        flash(f"Doktor olusturuldu, sifre:{password} ","success")
        
        return redirect(url_for("index"))

        
@app.route("/adminlogin",methods=["GET","POST"])
def adminlogin():
    
    if "logged_in" in session:
        flash("Zaten giriş yaptınız","warning")
        return redirect(url_for("index"))
    
    if request.method=="GET":
        return render_template("login.html")
    
    elif request.method=="POST":
        
        email = request.form.get("email")
        password = request.form.get("password")
        
        con = sqlite3.connect("mydatabase.db")
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM admins WHERE email=?",(email,))
        user = cursor.fetchone()
        
        if not user:
            flash("Böyle bir kullanıcı yok","info")
            return redirect(url_for("adminlogin"))
        
        
        if user[4]==password:
            flash("Başarıyla giriş yaptınız.","success")
            
            session["logged_in"] = True
            session["adminID"] = user[0]
            
            return redirect(url_for("index"))
        
        else:
            flash("Şifre yanlış","danger")
        
            return redirect(url_for("adminlogin"))
        
        
@app.route("/doctorlogin",methods=["GET","POST"])
def doctorlogin():
    
    if "logged_in" in session:
        flash("Zaten giriş yaptınız","warning")
        return redirect(url_for("index"))
    
    if request.method=="GET":
        return render_template("login.html")
    
    elif request.method=="POST":
        
        email = request.form.get("email")
        password = hashlib.sha256(request.form.get("password").encode()).hexdigest()
        
        con = sqlite3.connect("mydatabase.db")
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM doctors WHERE email=?",(email,))
        user = cursor.fetchone()
        
        if not user:
            flash("Böyle bir kullanıcı yok","info")
            return redirect(url_for("doctorlogin"))
        
        
        if user[5]==password:
            flash("Başarıyla giriş yaptınız.","success")
            
            session["logged_in"] = True
            session["doctorID"] = user[0]
            
            return redirect(url_for("index"))
        
        else:
            flash("Şifre yanlış","danger")
        
            return redirect(url_for("doctorlogin"))
        
        
@app.route("/userlogin",methods=["GET","POST"])
def userlogin():
    
    if "logged_in" in session:
        flash("Zaten giriş yaptınız","warning")
        return redirect(url_for("index"))
    
    if request.method=="GET":
        return render_template("login.html")
    
    elif request.method=="POST":
        
        email = request.form.get("email")
        password = hashlib.sha256(request.form.get("password").encode()).hexdigest()
        
        print(password)
        
        con = sqlite3.connect("mydatabase.db")
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM patients WHERE email=?",(email,))
        user = cursor.fetchone()
        
        if not user:
            flash("Böyle bir kullanıcı yok","info")
            return redirect(url_for("userlogin"))
        
        
        if user[5]==password:
            flash("Başarıyla giriş yaptınız.","success")
            
            session["logged_in"] = True
            session["patientID"] = user[0]
            
            print(session["patientID"])
            
            return redirect(url_for("index"))
        
        else:
            flash("Şifre yanlış","danger")
        
            return redirect(url_for("userlogin"))
        
        
@app.route("/appointment",methods=["GET","POST"])
@user_login_required
def appointment():
    con = sqlite3.connect("mydatabase.db")
    cursor = con.cursor()
        
    cursor.execute("SELECT name,surname,birthdate,gender,phone,address FROM patients WHERE patientID = ?",(session["patientID"],))
    data = cursor.fetchall()
    
    
    if request.method=="GET":
        

        return render_template("appointment.html",data=data[0],date=data[0][2])
    
    else:
        real_apps = []
        
        tarih_nesnesi = datetime.datetime.strptime(request.form.get("appointment_date"), "%Y-%m-%d")

        yeni_tarih = tarih_nesnesi.strftime("%d-%m-%Y")
        
        cursor.execute("SELECT doctorID from doctors WHERE department=?",(request.form.get("department") ,))

        ids = cursor.fetchall()
        
        print(ids)
        
        cursor.execute("SELECT * FROM appointments WHERE appointment_date=? AND appointment_time=? AND granted=0",(yeni_tarih,request.form.get("time")))

        apps = cursor.fetchall()
        
        for app in apps:
            if(app[2]==ids[0][0] or app[2]==ids[1][0]):
                real_apps.append(app)
        
        return render_template("appointment.html",indexx=0,time=request.form.get("time"),info=real_apps,data=data[0])
    
    

    
@app.route("/grant_appointment/<int:id>", methods=['GET'])
def grant_appointment(id):
    con = sqlite3.connect("mydatabase.db")
    cursor = con.cursor()

    cursor.execute("UPDATE appointments SET granted = 1,patientID = ? WHERE appointmentID=?",(session["patientID"],id))
    con.commit()
    
    
    flash("Randevu Oluşturuldu","success")
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/doctor-profile")
def doctorprofile():
    con = sqlite3.connect("mydatabase.db")
    cursor = con.cursor()
    
    patients = []
    
    cursor.execute("SELECT * FROM doctors WHERE doctorID = ?",(session["doctorID"],))
    doctor = cursor.fetchone()
    
    cursor.execute("SELECT * FROM appointments WHERE doctorID=? and granted=?",(session["doctorID"],1))
    apps = cursor.fetchall()
    
    for app in apps:
        print(app[1])
        cursor.execute("SELECT * FROM patients WHERE patientID=? ",(app[1],))

        patients.append(cursor.fetchone())
        
    print(doctor,apps,patients)
    
    return render_template("doctorprofile.html",doctor=doctor,apps=enumerate(apps),patients=patients)


@app.route("/dashboard")
@admin_login_required
def dashboard():
    more_than_ten = False
    con = sqlite3.connect("mydatabase.db")
    cursor = con.cursor()
    
    cursor.execute("SELECT * FROM doctors")
    data = cursor.fetchall()
    
    if len(data)>=10:
        data = data[:10]
        more_than_ten = True
        
    
    return render_template("dashboard.html",data=data,mt=more_than_ten)  


@app.route("/deletedoctor/<int:id>")  
@admin_login_required
def deletedoctor(id):
    con = sqlite3.connect("mydatabase.db")
    cursor = con.cursor()
    
    cursor.execute("DELETE FROM doctors WHERE doctorID = ?",(id,))  
    con.commit()
    
    flash('Doktor Silindi','danger')  
    
    return redirect(url_for("dashboard"))




@app.route("/deletedoctor_grant/<int:id>")
@admin_login_required
def deletedoctor_grant(id):
    con = sqlite3.connect("mydatabase.db")
    cursor = con.cursor()
    
    cursor.execute("SELECT * FROM doctors WHERE doctorID = ?",(id,))
    data = cursor.fetchone()
    
    return render_template("remove_doctor.html",data=data)



@app.route("/editdoctor_grant/<int:id>",methods=["GET","POST"])
@admin_login_required
def editdoctor_grant(id):
    if request.method=="GET":
        con = sqlite3.connect("mydatabase.db")
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM doctors WHERE doctorID = ?",(id,))
        data = cursor.fetchone()
        
        indexx = tıp_branşları.index(data[10])
        
        return render_template("edit_doctor.html",data=data,index=indexx)
    else:
        con = sqlite3.connect("mydatabase.db")
        cursor = con.cursor()
        
        name = request.form.get("name")
        surname = request.form.get("surname")
        birthdate = request.form.get("birthdate")
        profession = request.form.get("profession")
        phone = request.form.get("phone")
        address = request.form.get("address")
        
        cursor.execute("UPDATE doctors SET name=?,surname=?,department=?,birthdate=?,phone=?,address=? WHERE doctorID = ?",(name,surname,profession,birthdate,phone,address,id))  
        con.commit()
        
        flash('Doktor Düzenlendi','warning')  
        
        return redirect(url_for("dashboard"))
    
@app.route("/myappointments")
def my_appointments():
    con = sqlite3.connect("mydatabase.db")
    cursor = con.cursor()
    
    cursor.execute("SELECT * FROM appointments WHERE granted=1")
    apps = cursor.fetchall()
    
    return render_template("my_appointments.html",appointments=enumerate(apps))


@app.route("/doctors")
@admin_login_required
def show_doctors():
    con = sqlite3.connect("mydatabase.db")
    cursor = con.cursor()
    
    cursor.execute("SELECT * FROM doctors")
    data = cursor.fetchall()
    
    return render_template("doctos.html",data=data)




if __name__=="__main__":
    # scheduler.add_job(func=bruh,trigger="interval",seconds=5,id="gener",args=(10,))
    # scheduler.start()
    app.run(host="localhost",port=3000,debug=True)
    
    