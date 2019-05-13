from flask_restplus import Namespace, Resource
import status

ns = Namespace('auth', description='Authorizations')


@ns.route('/')
class Auth(Resource):
    @ns.doc(responses={
            status.HTTP_200_OK: 'HTTP_200_OK',
            status.HTTP_401_UNAUTHORIZED: 'HTTP_401_UNAUTHORIZED'
            })
    def get(self):
        from flask import request
        ip = request.remote_addr
        if ip:
            from app.models import Visitor
            has = Visitor.query.filter(Visitor.addr == ip).first()
            if not has:
                from app import db
                visitor = Visitor(addr=remote_addr)
                db.session.add(visitor)
                db.session.commit()
            from werkzeug.security import generate_password_hash
            return {'code': status.HTTP_200_OK, 'token': generate_password_hash(ip)}
        else:
            return {'code': status.HTTP_401_UNAUTHORIZED}
