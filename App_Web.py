#Mohamed Ben Hammou
from flask import Flask, request, render_template, redirect, url_for, session
import App_detec

app = Flask(__name__)
app.secret_key = 'mclave_segura'

@app.route("/")
def inici():
    if session.get('correu'):
        return render_template('Page_Web_User.html', correu=session.get('correu'))
    else:
        return render_template('base.html')

@app.route('/pageprincipal', methods=['POST', 'GET'])
def pageprincipal():
        return redirect(url_for('inici'))

@app.route('/access_user', methods=['POST', 'GET'])
def getaccess():
    error_msg = None

    if session.get('correu'):
        return render_template('Page_Web_User.html', correu=session.get('correu'))
    else:    
        if request.method == 'POST':
            mail = request.form['correu']
            password = request.form['contraseña']
            
            try:
                nombre, correu, contraseña = App_detec.getaccess(mail, password)

                # Si llegamos aquí es dicer hay un mensaje
                session['correu'] = mail
                return render_template('Page_Web_User.html', nombre=nombre, correu=correu, contraseña=contraseña)
            except ValueError as e:
                error_msg = "Credenciales de acceso incorrectas. Inténtalo de nuevo."

        return render_template('Page_Web_Access.html', error_msg=error_msg)


@app.route('/registrar', methods=['POST', 'GET'])
def registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        resultado = App_detec.register_account(nombre, apellido, correo, contraseña)

        if resultado == App_detec.AFEGIT:
            return render_template('Page_Web_User.html', nombre=nombre)
        elif resultado == App_detec.JAEXISTEIX:
            return render_template('Page_Web_User.html', mensaje="Usuario ya registrado. Por favor, inicia sesión.")
    
    return render_template('Page_Web_User.html')


@app.route("/logout")
def logout():
    if session.get('correu'):
        session.pop('correu',default=None)
    return redirect(url_for('inici'))


@app.route('/about')
def about():
    return render_template('show_contenido.html', content='This is the About Us page.')

@app.route('/location')
def news():
    return render_template('show_contenido.html', content='Check out our latest updates.')

@app.route('/sites')
def location():
    return render_template('show_contenido.html', content='Find us at the following location.')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    mensaje_agradecimiento = None

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        comentario = request.form['comentario']

        with open('comentarios.txt', 'a') as file:
            file.write(f'Nombre: {nombre}\nApellido: {apellido}\nCorreo: {correo}\nComentario: {comentario}\n\n')

        # Establecer un mensaje
        mensaje_agradecimiento = "¡Gracias por tu comentario!"

    return render_template('show_contenido.html', mensaje_agradecimiento=mensaje_agradecimiento)


@app.route('/show_datos')
def show_datos():
    if 'correu' in session:
        mail = session['correu']
        nombre, apellido, correu = App_detec.muestradatos(mail)
        return render_template('Page_Web_User.html', nombre=nombre, apellido=apellido, correu=correu)
    else:
        return redirect(url_for('inici'))

@app.route('/modificar_datos', methods=['GET', 'POST'])
def modificar_datos():
    resultado = None  # Asigna un valor predeterminado

    if 'correu' in session:
        mail = session['correu']

        if request.method == 'POST':
            nuevo_nombre = request.form['nombre']
            nuevo_apellido = request.form['apellido']
            nuevo_correu = request.form['correu']
            nueva_contrasena = request.form['contraseña']

            resultado = App_detec.modificardatos(mail, nuevo_nombre, nuevo_apellido, nuevo_correu, nueva_contrasena)

            if resultado == 'MODIFICAT':
                return render_template('Page_Web_User.html', nombre=nuevo_nombre, apellido=nuevo_apellido, correu=nuevo_correu, contraseña=nueva_contrasena, resultado=resultado)

    return render_template('Page_Web_User.html', resultado=resultado)


if __name__ == '__main__':
    app.run(debug=True)