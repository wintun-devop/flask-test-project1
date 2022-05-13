from primary_module import db
import datetime

class Brand(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200),nullable=False,unique=True)
    
class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False,unique=True)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    model=db.Column(db.String(255),nullable=False)
    price=db.Column(db.Numeric(15,2),nullable=False)
    discount=db.Column(db.Integer,default=0)
    stock=db.Column(db.Integer,nullable=False)
    color=db.Column(db.String(255),nullable=False)
    description=db.Column(db.Text(),nullable=False)
    #brand relationship
    brand_id=db.Column(db.Integer,db.ForeignKey("brand.id"),nullable=False)
    brand=db.relationship("Brand",backref=db.backref("brand",lazy=True))
    category_id=db.Column(db.Integer,db.ForeignKey("category.id"),nullable=False)
    category=db.relationship("Category",backref=db.backref("category",lazy=True))
    image=db.Column(db.String(255),nullable=False,default="default_image.jpg")
    lastupdate=db.Column(db.DateTime,default=datetime.datetime.utcnow())
    def __repr__(self):
        return "<Products %r>" % self.name