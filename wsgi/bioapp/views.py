import json
import md5
import os

from flask import render_template, request
from flask import redirect, url_for, session
from werkzeug.utils import secure_filename

from flask.ext.classy import FlaskView, route
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from bioapp import bioapp
from bioapp import application
from forms import *
from models import *
from config import Config

from mod_auth.forms import *
from mod_auth.models import *


@bioapp.route('/')
@bioapp.route('/<username>')
def index(username=None):
    if username is None:
        return render_template('index.html', page_title='Biography just for you!', signin_form=SigninForm())

    user = Users.query.filter_by(username=username).first()
    if user is None:
        user = Users()
        user.username = username
        user.fullname = 'Batman, is that you?'
        user.tagline = 'Tagline of how special you are'
        user.bio = 'Explain to the rest of the world, why you are the very most unique person to look at'
        user.avatar = '/static/batman.jpeg'
        return render_template('themes/water/bio.html', page_title='Claim this name : ' + username, user=user,
                               signin_form=SigninForm(), portoform=PortoForm())
    else:
        return render_template('themes/water/bio.html', page_title=user.fullname, user=user, signin_form=SigninForm(),
                               portoform=PortoForm())




class SettingsView(FlaskView):
    @login_required
    def index(self):
        return render_template('profile.html', page_title='Customize your profile')


class PortfolioView(FlaskView):
    @route('add_update', methods=['POST'])
    @login_required
    def add_update(self):
        form = PortoForm(request.form)
        if form.validate():
            result = {}
            result['iserror'] = False

            if not form.portfolio_id.data:
                user = Users.query.filter_by(username=session['username']).first()
                if user is not None:
                    user.portfolio.append(
                        Portfolio(title=form.title.data, description=form.description.data, tags=form.tags.data))
                    print 'id ', form.portfolio_id
                    db.session.commit()
                    result['savedsuccess'] = True
                else:
                    result['savedsuccess'] = False
            else:
                portfolio = Portfolio.query.get(form.portfolio_id.data)
                form.populate_obj(portfolio)
                db.session.commit()
                result['savedsuccess'] = True

            return json.dumps(result)

        form.errors['iserror'] = True
        print form.errors
        return json.dumps(form.errors)


    @route('get/<id>')
    @login_required
    def get(self, id):
        portfolio = Portfolio.query.get(id)
        return json.dumps(portfolio._asdict())


    @route('delete/<id>')
    @login_required
    def delete(self, id):
        portfolio = Portfolio.query.get(id)
        db.session.delete(portfolio)
        db.session.commit()
        result = {}
        result['result'] = 'success';
        return json.dumps(result)

class BiographyView(FlaskView):
    @route('edit_biography', methods=['POST'])
    def edit_biography(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        user.bio = request.form["value"]
        result = {}
        db.session.commit()
        return json.dumps(result)

    @route('edit_fullname', methods=['POST'])
    def edit_fullname(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        user.fullname = request.form["value"]
        result = {}
        db.session.commit()
        return json.dumps(result)  #or, as it is an empty json, you can simply use return "{}"

    @route('edit_tagline', methods=['POST'])
    def edit_tagline(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        user.tagline = request.form["value"]
        result = {}
        db.session.commit()
        return json.dumps(result)

    @route('upload_avatar', methods=['POST'])
    def upload_avatar(self):
        if request.method == 'POST':
            id = request.form["avatar_user_id"]
            file = request.files['file']
            if file and allowed_file(str.lower(str(file.filename))):
                user = Users.query.get(id)
                filename = user.username + "_" + secure_filename(file.filename)
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                img = "/static/upload/" + filename

                user.avatar = img
                db.session.commit()
                return img

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


PortfolioView.register(bioapp)
BiographyView.register(bioapp)
SettingsView.register(bioapp)