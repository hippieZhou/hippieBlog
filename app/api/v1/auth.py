from flask_restplus import Namespace, Resource
import status

ns = Namespace('Auth', description='authorizations')


@ns.route('/')
class Auth(Resource):
    @ns.doc(security=[],
            responses={
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
                visitor = Visitor(addr=ip)
                db.session.add(visitor)
                db.session.commit()
            from hashlib import md5
            h = md5()
            h.update(ip.encode(encoding='utf-8'))
            return {'code': status.HTTP_200_OK, 'X-API-KEY': h.hexdigest()}
        else:
            return {'code': status.HTTP_401_UNAUTHORIZED}
