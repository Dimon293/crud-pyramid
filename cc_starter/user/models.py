from sqlalchemy import Column, Integer, Text

from .. import Base


class User(Base):
    __table_args__ = {'comment': 'Пользователь'}
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)
    password_hash = Column(Text)

    def __json__(self, *args, **kwargs):
        return {'id': self.id, 'name': self.name, 'role': self.role, 'password_hash': self.password_hash}