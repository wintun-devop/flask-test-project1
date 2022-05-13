from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms.validators import DataRequired,EqualTo,Email,Length
from wtforms import StringField,SubmitField,IntegerField,SelectField,PasswordField,TextAreaField

class AddBrand(FlaskForm):
    f_brandname=StringField("Add Brand:",validators=[DataRequired()],render_kw={"placeholder": "Brand Name...."})
    submit=SubmitField("Submit")

class AddCategory(FlaskForm):
    f_category=StringField("Add Category:",validators=[DataRequired()],render_kw={"placeholder":"Category...."})
    submit=SubmitField("Submit")

class AddProduct(FlaskForm):
    f_name=StringField("Item Name:",validators=[DataRequired()],render_kw={"placeholder": "Item Name...."})
    f_model=StringField("Item Model:",validators=[DataRequired()],render_kw={"placeholder": "Item Model...."})
    f_price=IntegerField("Price:",validators=[DataRequired()],render_kw={"placeholder": "Price.."})
    f_discount=IntegerField("Discount:",validators=[DataRequired()],default=0,render_kw={"placeholder": "Price.."})
    f_stock=IntegerField("Stock:",validators=[DataRequired()],render_kw={"placeholder": "Stock.."})
    f_color=StringField("Color:",validators=[DataRequired()],render_kw={"placeholder": "Color."})
    f_desc=TextAreaField("Description",validators=[DataRequired()],render_kw={"placeholder":"Description"})
    f_image=FileField("Product Image:",validators=[FileRequired(),FileAllowed(["jpg","png","gif","jpeg"])])
    submit=SubmitField("Submit")