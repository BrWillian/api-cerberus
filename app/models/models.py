from app import db
from datetime import date

# models here


class UploadImage(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    img_ori = db.Column(db.BLOB)
    img_prd = db.Column(db.BLOB)
    date = db.Column(db.Date, default=date.today)

    def __init__(self, img_ori, img_prd):
        self.img_ori = img_ori
        self.img_prd = img_prd