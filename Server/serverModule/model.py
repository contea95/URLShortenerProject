from serverModule import db


class Url(db.Model):
    __tablename__ = 'url'

    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    origin_url = db.Column(db.String(128))

    def __init__(self, origin_url):
        self.origin_url = origin_url

    #   id 기준으로 url 찾기
    def search_url_by_id(self, id):
        return Url.query.filter_by(id=id).first()

    #   origin_url 기준으로 id찾기
    def search_id_by_origin_url(self, origin_url):
        return Url.query.filter_by(origin_url=origin_url).first()
