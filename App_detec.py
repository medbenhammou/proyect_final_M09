#Mohamed Ben Hammou
import mysql.connector

#creamos una tabla la base de datos llamada usuarios que tiene 4 colomnas (nombre, apellido,correu,contraseña)
mydb = mysql.connector.connect(
    host="localhost",
    user="mohamed",
    password="asixstudent",
    database="my_base_datos"
)

NOTROBAT = "NOTROBAT"
AFEGIT = "AFEGIT"
MODIFICAT = "MODIFICAT"
JAEXISTEIX = "JAEXISTEIX"


def getaccess(mail,password):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM usuarios")
    myresult = mycursor.fetchall()
    for x in myresult:
        if mail == x[2] and password==x[3]:
            nom=x[0]
            return nom,mail,password
    return NOTROBAT

def register_account(nombre, apellido, correo, contrasena):
    mycursor = mydb.cursor()

    existing_account = get_account(nombre)

    if existing_account == NOTROBAT:
        sql = "INSERT INTO usuarios (nombre, apellido, correo, contraseña) VALUES (%s, %s, %s, %s)"
        val = (nombre, apellido, correo, contrasena)
        mycursor.execute(sql, val)
        mydb.commit()
        return AFEGIT

    return JAEXISTEIX
def get_account(nombre):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (nombre,))
    account = mycursor.fetchone()

    if account:
        return account
    else:
        return NOTROBAT

def muestradatos(mail):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM usuarios")
    myresult = mycursor.fetchall()
    for x in myresult:
        if mail == x[2]:
            nom=x[0]
            apellido=x[1]
            return nom, apellido, mail
    return NOTROBAT
    
def modificardatos(mail, nuevo_nombre, nuevo_apellido, nuevo_correu, nueva_contrasena):
    mycursor = mydb.cursor()

    # Actualiza los datos del usuario en la base de datos
    mycursor.execute("UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s, contraseña = %s WHERE correo = %s",
                     (nuevo_nombre, nuevo_apellido, nuevo_correu, nueva_contrasena, mail))

    mydb.commit()

    return MODIFICAT
