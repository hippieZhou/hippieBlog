from app.api.v1 import api
from flask import request
from werkzeug.security import generate_password_hash
from flask_restplus import Resource
import status

ns = api.namespace('auth', description='Authorizations')


@ns.route('/')
class Authorized(Resource):
    @api.doc(responses={
        status.HTTP_401_UNAUTHORIZED: 'HTTP_401_UNAUTHORIZED'
    })
    def get(self):
        ip = request.remote_addr
        from app.models import Visitor
        has = Visitor.query.filter(Visitor.addr == ip).first()
        if not has:
            from app import db
            visitor = Visitor(addr=remote_addr)
            db.session.add(visitor)
            db.session.commit()
        return {
            'code': status.HTTP_200_OK,
            'token': ip
        } if ip != None else {
            'code': status.HTTP_401_UNAUTHORIZED,
        }
