from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import app, db
from app.models import User, Invoice

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_invoice', methods=['GET', 'POST'])
@login_required
def upload_invoice():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado na solicitação
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado', 'danger')
            return redirect(request.url)

        file = request.files['file']

        # Verifica se o nome do arquivo é permitido
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Salva o arquivo na pasta de uploads
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Cria um novo objeto de Invoice no banco de dados
            new_invoice = Invoice(filename=filename, user_id=current_user.id)
            db.session.add(new_invoice)
            db.session.commit()

            flash('Nota fiscal enviada com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Formato de arquivo não permitido. Envie um arquivo PDF.', 'danger')

    return render_template('upload_invoice.html')
