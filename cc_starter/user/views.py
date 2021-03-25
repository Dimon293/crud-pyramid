from pyramid.exceptions import NotFound
from pyramid.view import view_config, view_defaults

from .. import db_session
from .models import User


@view_defaults(renderer='json')
class UserViews:
    def __init__(self, request):
        self.request = request
        self.view_name = 'UserViews'

    @view_config(request_method='GET', route_name='users')
    def get_users(self):
        users = db_session.query(User).all()
        # return [user.to_json() for user in users]
        return list(map(lambda user: user.to_json(), users))

    @view_config(request_method='GET', route_name='user')
    def get_user(self):
        if 'id' not in self.request.matchdict:
            NotFound()
        user = db_session.query(User).get(self.request.matchdict['id'])
        return user.to_json()

    @view_config(request_method='POST', route_name='users')
    def add_user(self):
        name = self.request.params.get('name')
        role = self.request.params.get('role')
        password_hash = self.request.params.get('password_hash')
        user = User(name=name, role=role, password_hash=password_hash)
        db_session.add(user)
        db_session.commit()
        return {'id': user.id}

    @view_config(request_method='PUT', route_name='user')
    def edit_user(self):
        if 'id' not in self.request.matchdict:
            NotFound()
        user = db_session.query(User).filter_by(id=self.request.matchdict['id'])
        name = self.request.params.get('name')
        role = self.request.params.get('role')
        password_hash = self.request.params.get('password_hash')
        user.update({'name': name, 'role': role, 'password_hash': password_hash})
        db_session.commit()
        return {'id': self.request.matchdict['id']}

    @view_config(request_method='DELETE', route_name='user')
    def delete_user(self):
        if 'id' not in self.request.matchdict:
            NotFound()
        user = db_session.query(User).get(self.request.matchdict['id'])
        db_session.delete(user)
        db_session.commit()
        return {'id': self.request.matchdict['id']}