from datetime import datetime
from tomomisaweddingapp.app import Database

class Images(Database.Model):
    id = Database.Column(Database.Integer, primary_key=True)
    public_id = Database.Column(Database.Text)
    url = Database.Column(Database.Text)
    ts = Database.Column(Database.DateTime)

    def __init__(self, public_id, url, ts=None):
        __tablename__ = 'images'
        self.public_id = public_id
        self.url = url
        if ts is None:
            self.ts = datetime.utcnow()
