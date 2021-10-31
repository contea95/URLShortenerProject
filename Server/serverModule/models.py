from serverModule import db

# DB 설정


class Url(db.Model):
    __tablename__ = 'url'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    origin_url = db.Column(db.String(128))

    def __init__(self, origin_url):
        self.origin_url = origin_url
