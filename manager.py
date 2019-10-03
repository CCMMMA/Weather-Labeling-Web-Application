"""This file contains the classes to create a web app to manage the users"""

from dbMongo import *
from flask import Flask,render_template,request,url_for,session,redirect
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
from wtforms import form, fields, Form, BooleanField, StringField, PasswordField, validators,RadioField
from flask_admin.model.fields import InlineFormField, InlineFieldList
from flask_admin import Admin, BaseView, expose
from werkzeug.security import generate_password_hash,check_password_hash


class UserForm(form.Form):
    name = fields.StringField('name',[validators.required(), validators.length(max=30)])
    surname = fields.StringField('surname',[validators.required(), validators.length(max=30)])
    username = fields.StringField('username',[validators.required(), validators.length(max=30)])
    password = fields.PasswordField('password',[validators.required(), validators.length(max=30)])
    role = RadioField('role',[validators.Required()],choices=[('ADMIN','ADMIN'),('USER','USER')],default='USER')

class UserView(ModelView):
    column_list = ('name','surname','username', 'password','role')
    column_sortable_list = ('name','surname','username', 'password','role')
    form = UserForm

    def on_model_change(self, form, model, is_created):
        try:
            count1 = managedb.getCountLoginDB(session["username"])
            if count1 == 0:
                session.clear()
        except Exception as e:
            session.clear()
            print("Error DB",str(e))
        password = model.get('password')
        model['password'] = generate_password_hash(password, method='pbkdf2:sha256')

    def on_model_delete(self,model):
        username = model.get('username')
        try:
            count1 = managedb.getCountLoginDB(session["username"])
            if count1 == 0:
                session.clear()
            managedb.deletePolygonDBonUsername(username)
        except Exception as e:
            session.clear()
            print("Error DB",str(e))

    def is_accessible(self):
        try:
            if(session["username"] == "ADMIN"):
                count1 = managedb.getCountLoginDB(session["username"])
                if count1 == 0:
                    session.clear()
        except Exception as e:
            session.clear()
            print("Error DB",str(e))
        return (session["role"] == "ADMIN")
