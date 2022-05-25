from flask import render_template,redirect,flash,url_for,request,send_from_directory
from primary_module import app,db
from .webforms import AddBrand,AddCategory,AddProduct
from .models import Brand,Category,Products
from werkzeug.utils import secure_filename
import uuid as uuid

#image upload location for product
app.config["UPLOAD_FOLDER_PRODUCTS"]="D:\\github-working\\flask-test-project1\\flask-modular-sample-app-1\\primary_module\\static\\images\\products\\"


#delete product for admin page
@app.route("/deleteproduct/<int:id>",methods=["GET","POST"])
def productdelete(id):
    product_to_delete=Products.query.get_or_404(id)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        flash("Item has been deleted successfully!")
        return redirect(url_for("productlist"))
    except:
        flash("Something went wrong in deleteing Product.Try again!")
        return redirect(url_for("productlist"))

#update product for admin page
@app.route("/updateproduct/<int:id>",methods=["GET","POST"])
def productupdate(id):
    product_to_update=Products.query.get_or_404(id)
    brands=Brand.query.all()
    categories=Category.query.all()
    product_update_form=AddProduct()
    if request.method == "POST":
        product_to_update.name=product_update_form.f_name.data
        product_to_update.model=product_update_form.f_model.data
        product_to_update.price=product_update_form.f_price.data
        product_to_update.brand_id=request.form["brand"]
        product_to_update.category_id=request.form["category"]
        product_to_update.discount=product_update_form.f_discount.data
        product_to_update.stock=product_update_form.f_stock.data
        product_to_update.color=product_update_form.f_color.data
        product_to_update.description=product_update_form.f_desc.data
        product_to_update.image=product_to_update.image
        db.session.add(product_to_update)
        db.session.commit()
        flash("Product has been updated successfully!")
        return redirect(url_for("productlist"))
    product_update_form.f_name.data=product_to_update.name
    product_update_form.f_model.data=product_to_update.model
    #change nuneric to integer type for input
    product_update_form.f_price.data=int(product_to_update.price)
    product_update_form.f_discount.data=product_to_update.discount
    product_update_form.f_stock.data=product_to_update.stock
    product_update_form.f_color.data=product_to_update.color
    product_update_form.f_desc.data=product_to_update.description
    return render_template("products/update_product.html",productupdateform=product_update_form,brands=brands,
                           categories=categories)

#product list for admin
@app.route("/listproduct",methods=["GET","POST"])
def productlist():
    product_list=Products.query.all()
    return render_template("products/list_product.html",productlist=product_list)

#add product page for admin panel
@app.route("/addproduct",methods=["GET","POST"])
def productadd():
    product_add_form=AddProduct()
    brands=Brand.query.all()
    categories=Category.query.all()
    if request.method == "POST":
        name=product_add_form.f_name.data
        model=product_add_form.f_model.data
        price=product_add_form.f_price.data
        brand=request.form["brand"]
        category=request.form["category"]
        discount=product_add_form.f_discount.data
        stock=product_add_form.f_stock.data
        color=product_add_form.f_color.data
        description=product_add_form.f_desc.data
        #image file from form input
        image_file=product_add_form.f_image.data
        #image file name
        image_file_name=secure_filename(image_file.filename)
        #system secure file name
        image_name=str(uuid.uuid1())+"_"+image_file_name
        #save image to your custom location
        image_file.save(app.config["UPLOAD_FOLDER_PRODUCTS"]+image_name)
        product=Products(name=name,model=model,price=price,discount=discount,stock=stock,color=color,
                         description=description,brand_id=brand,category_id=category,image=image_name)
        db.session.add(product)
        db.session.commit()
        flash("Product has been added successfully.!")
        return redirect(url_for("productlist"))
    return render_template("products/add_product.html",productaddform=product_add_form,brands=brands,
                           categories=categories)

#update category for admin page
@app.route("/updatecategory/<int:id>",methods=["GET","POST"])
def catetoryupdate(id):
    category_to_update=Category.query.get_or_404(id)
    category_update_form=AddCategory()
    if category_update_form.validate_on_submit():
        category_to_update.name=category_update_form.f_category.data
        db.session.add(category_to_update)
        db.session.commit()
        flash("Category updated Successfully!")
        return redirect(url_for("categorylist"))
    category_update_form.f_category.data=category_to_update.name
    return render_template("products/update_category.html",categoryupdateform=category_update_form)

#list category for admin page
@app.route("/listcategory",methods=["GET","POST"])
def categorylist():
    category_list=Category.query.all()
    return render_template("products/list_category.html",categorylist=category_list)

#Add category for admin page
@app.route("/addcategory",methods=["GET","POST"])
def categoryadd():
    add_category_form=AddCategory()
    if add_category_form.validate_on_submit():
        category=Category.query.filter_by(name=add_category_form.f_category.data).first()
        if category is None: 
            category=Category(name=add_category_form.f_category.data)
            db.session.add(category)
            db.session.commit()
            add_category_form.f_category.data=""
            flash("Category Added Successfully!")
            return redirect(url_for("categorylist"))
        else:
            flash("Category name already exist!")
            return redirect(url_for("categorylist"))
    return render_template("products/add_category.html",addcatform=add_category_form)


#update brand name for admin page
@app.route("/updatebrand/<int:id>",methods=["GET","POST"])
def brandupdate(id):
    brand_to_update=Brand.query.get_or_404(id)
    brand_update_form=AddBrand()
    if brand_update_form.validate_on_submit():
        brand_to_update.name=brand_update_form.f_brandname.data
        db.session.add(brand_to_update)
        db.session.commit()
        flash("Brand updated successfully!","info")
        return redirect(url_for("brandlist"))
    brand_update_form.f_brandname.data=brand_to_update.name
    return render_template("products/update_brand.html",brandupdateform=brand_update_form)


#list brand and admin page
@app.route("/listbrand",methods=["GET","POST"])
def brandlist():
    brand_list=Brand.query.all()
    return render_template("products/list_brand.html",brandlist=brand_list)

#add brand for admin page
@app.route("/addbrand",methods=["GET","POST"])
def brandadd():
    add_brand_form=AddBrand()
    if add_brand_form.validate_on_submit():
        brand=Brand.query.filter_by(name=add_brand_form.f_brandname.data).first()
        if brand is None:
            brand=Brand(name=add_brand_form.f_brandname.data)
            db.session.add(brand)
            db.session.commit()
            add_brand_form.f_brandname.data=""
            flash("Brand Added Successfully!")
            return redirect(url_for("brandlist"))
        else:
            flash("Brand name already exist!")
            return redirect(url_for("brandlist"))
    return render_template("products/add_brand.html",addbrandform=add_brand_form)

@app.route("/category/<int:id>",methods=["GET","POST"])
def product_by_category(id):
    product_by_category_display=Products.query.filter_by(category_id=id)
    brands=Brand.query.join(Products,(Brand.id == Products.brand_id)).all()
    categories=Category.query.join(Products,(Category.id == Products.category_id)).all()
    return render_template("products/index.html",product_by_category_display=product_by_category_display,categories=categories,brands=brands)
    

@app.route("/<int:id>",methods=["GET","POST"])
def product_by_brand_display(id):
    display_brand=Products.query.filter_by(brand_id=id)
    brands=Brand.query.join(Products,(Brand.id == Products.brand_id)).all()
    categories=Category.query.join(Products,(Category.id == Products.category_id)).all()
    return render_template("products/index.html",displaybrand=display_brand,brands=brands,categories=categories)

@app.route("/")
def index():
    #display product by page limit
    page=request.args.get("page",1,type=int)
    #Display products only on available stock
    product_list=Products.query.filter(Products.stock > 0).paginate(page=page,per_page=4)
    #only display for instock brand
    brands=Brand.query.join(Products,(Brand.id == Products.brand_id)).all()
    categories=Category.query.join(Products,(Category.id == Products.category_id)).all()
    return render_template("products/index.html",display_products=product_list,brands=brands,categories=categories)

@app.route("/css/products/main.css")
def cert_style():
    return send_from_directory("templates", "css/products/main.css")








