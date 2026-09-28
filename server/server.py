from flask import Flask, send_from_directory
from flask import request, render_template
from flask_cors import CORS, cross_origin
from sallinggroup.server.data.db_connection import *
from sallinggroup.server.data.update_offers_web import update_offers
import socket
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app = Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
host = socket.gethostname()
print ("IP:", ip_address)


@app.route("/")
@cross_origin()
def landing_page():
    context = {
        "IP_address": ip_address
    }
    return render_template("home.html", **context)



@app.route("/offers")
@cross_origin()
def offers_page():
    context = {
        "IP_address": ip_address
    }
    return render_template("home.html", **context)


@app.route("/contact")
@cross_origin()
def contact_page():
    context = {
        "IP_address": ip_address
    }
    return render_template("contact.html", **context)


@app.route("/cookies")
@cross_origin()
def cookies_page():
    context = {
        "IP_address": ip_address
    }
    return render_template("cookies_policy.html", **context)


@app.route("/privacy")
@cross_origin()
def privacy_page():
    context = {
        "IP_address": ip_address
    }
    return render_template("privacy_policy.html", **context)

@app.route("/terms")
@cross_origin()
def terms_page():
    context = {
        "IP_address": ip_address
    }
    return render_template("terms_and_conditions.html", **context)


@app.route("/disclaimer")
@cross_origin()
def disclaimer_page():
    context = {
        "IP_address": ip_address
    }
    return render_template("disclaimer.html", **context)



@app.route("/about")
@cross_origin()
def about_page():
    context = {
        "IP_address": ip_address
    }
    return render_template("about.html", **context)




@app.route("/closeby")
@cross_origin()
def closeby():
    locations = [float(request.args.get('l1')), float(request.args.get('l2'))]
    return get_closeby(locations)


@app.route("/store_products")
@cross_origin()
def store_products():
    store_id = request.args.get('store-code')
    return get_store_page(store_id)

    
@app.route("/store_offers")
@cross_origin()
def store_offers():
    store_id = request.args.get('store_id')
    print(store_id)
    return get_store_page_data(store_id)


@app.route("/closeby_address")
@cross_origin()
def closeby_address():
    locations = request.args.get('address')
    area = request.args.get('area')
    if area != "":
        locations = request.args.get('address')+", "+area

    return get_closeby_address(locations)


@app.route("/areas")
@cross_origin()
def areas():
    area = request.args.get('area')
    address = request.args.get('partial_address')
    listed_options = addresses_from_area(area, address)
    return listed_options


@app.route("/update_offers")
@cross_origin()
def update_offers_call():
    code = request.args.get('code')
    print(code)
    if code == "dhg30e83jbofu30jg79e2202KJGD0dG":
        update_offers()
        return 1
    return 0


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])