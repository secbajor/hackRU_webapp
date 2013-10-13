from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True

client = MongoClient('localhost',27017)
db = client.userdb
xdb = client.productdb
col = db['purchases']
col2 = xdb['products']

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/htmlpg')
def render_this():
    return render_template('landing.html')

#handle form submission 
@app.route('/product_entry', methods=['GET', 'POST'])
def form_submission():
    if request.method == 'GET':
        return render_template('landing.html')
    elif request.method == 'POST':
        for input_name, val in request.form.iteritems():
            col.insert({'name': val})
        return render_template('landing.html')
        

@app.route('/userdata')
def userdata():
    # find all the purchases in the purchases column of the database
    purchases = col.find()
    # pass along the purchases in the purchases variable to the template
    return render_template('userdata.html', purchases=purchases)

@app.route('/userscore')
def userscore():
    # find the average score of entries
    products = col.find()
    products = [product for product in products]
    total = avg = count = 0
    for product in products:
        productName = product['name']
        print productName, " <--product"
        found_product = col2.find_one({"name": productName})
        print "product found was", found_product
        total += found_product['ovr']
        count += 1
    avg = total/count
    
    return render_template('userscore.html', avg = avg)

@app.route('/productdata')
def productdata():
    # find all the products in the products column of the database
    products = col2.find()
    # pass along the products in the product variable to the template
    return render_template('productdata.html', products=products)

@app.route('/view_all', methods=['POST'])
def view_all():
    return redirect(url_for('userdata'))

@app.route('/view_product_db', methods=['POST'])
def view_product_db():
    return redirect(url_for('productdata'))

@app.route('/view_score', methods=['POST'])
def view_userscore():
    return redirect(url_for('userscore'))


if __name__ == '__main__':  
    app.run()
