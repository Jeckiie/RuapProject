from flask import Blueprint, render_template, request, flash, redirect
from . import db
from .models import Image
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .prediction import getPrediction
from flask import send_file
import os


main = Blueprint('main', __name__)
lastClassifiedImgID = 0;

@main.route('/')
@login_required
def index():
    images = Image.query.order_by(Image.id.desc()).first()
    if not images:
        return render_template('index.html', name=current_user.name, imageID = 0, lastClassifiedImg=lastClassifiedImgID)
    return render_template('index.html', name=current_user.name, imageID = images.id, lastClassifiedImg=lastClassifiedImgID)

@main.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            mimetype = os.path.splitext(filename)[1]
            path = "/static/" + filename
            image = Image.query.filter_by(path=path).first()
            if not image:
                image = Image(mimetype=mimetype, path=path)
                db.session.add(image)
                db.session.commit()
                file.save(os.path.join('../static/', filename)) 
            
            label = getPrediction(filename)
           # label = label.decode('utf-8')
           # label = label[41:-5]
            flash(label)
            global lastClassifiedImgID
            lastClassifiedImgID = image.id
            return redirect('/')
        
@main.route('/<int:id>')
def get_img(id):
    image = Image.query.filter_by(id=id).first()
    if not image:
        return 'can not find image with that name', 404
    path = '..' + image.path;
    return send_file(path, mimetype='image');

   # return Response(response=image.id)
#@main.route('/profile')
#@login_required
#def profile():
#    return render_template('profile.html', name=current_user.name)