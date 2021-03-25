from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .. import Base


class Article(Base):
    __table_args__ = {'comment': 'Статья'}
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    data = Column(Text, nullable=False)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User')

    def __json__(self, *args, **kwargs):
        return {'id': self.id, 'name': self.name, 'data': self.data, 'user': str(self.user)}