from flask import jsonify, request
from flask_restful import Resource
from models.sea import Sea
from app import db
from sqlalchemy.exc import IntegrityError 
from flask_jwt_extended import jwt_required
