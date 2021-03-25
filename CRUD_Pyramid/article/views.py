from pyramid.exceptions import NotFound
from pyramid.view import view_config, view_defaults

from .. import db_session
from .models import Article


@view_defaults(renderer='json')
class ArticleViews:
    def __init__(self, request):
        self.request = request
        self.view_name = 'ArticleViews'

    @view_config(request_method='GET', route_name='articles')
    def get_articles(self):
        articles = db_session.query(Article).all()
        # return [user for user in articles]
        return list(map(lambda article: article, articles))

    @view_config(request_method='GET', route_name='article')
    def get_article(self):
        article = db_session.query(Article).get(self.request.matchdict['id'])
        return article

    @view_config(request_method='POST', route_name='articles')
    def add_article(self):
        article = Article(**self.request.POST)
        user_id = self.request.POST.get('user_id')
        if user_id is None or user_id <= 0:
            NotFound()
        db_session.add(article)
        db_session.commit()
        return {'id': article.id, 'id_user': user_id}

    @view_config(request_method='PUT', route_name='article')
    def edit_article(self):
        if 'id' not in self.request.matchdict:
            NotFound()
        article = db_session.query(Article).filter_by(id=self.request.matchdict['id'])
        user_id = self.request.POST.get('user_id')
        if user_id is None or user_id <= 0:
            NotFound()
        article.update({**self.request.POST})
        db_session.commit()
        return {'id': self.request.matchdict['id']}

    @view_config(request_method='DELETE', route_name='article')
    def delete_article(self):
        if 'id' not in self.request.matchdict:
            NotFound()
        article = db_session.query(Article).get(self.request.matchdict['id'])
        db_session.delete(article)
        db_session.commit()
        return {'id': self.request.matchdict['id']}


def includeme(config):
    config.add_route('articles', '/articles')
    config.add_route('article', '/articles/{id:\d+}')
