################################################################################################################################
# *** Copyright Notice ***
#
# "Price Based Local Power Distribution Management System (Local Power Distribution Manager) v1.0" 
# Copyright (c) 2016, The Regents of the University of California, through Lawrence Berkeley National Laboratory 
# (subject to receipt of any required approvals from the U.S. Dept. of Energy).  All rights reserved.
#
# If you have questions about your rights to use or distribute this software, please contact 
# Berkeley Lab's Innovation & Partnerships Office at  IPO@lbl.gov.
################################################################################################################################


# TUTORIAL CODE for restful API server, TO BE ADAPTED FOR OUR PURPOSES
# from https://github.com/miguelgrinberg/REST-tutorial which is MIT licensed as of 20161205:  https://github.com/miguelgrinberg/REST-tutorial/blob/master/LICENSE

#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
import laptop_control

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

# We can add more security features here as necessary, since remote controlling
# laptops shouldn't be an open interface.
@auth.get_***REMOVED***
def get_***REMOVED***(username):
    if username == '***REMOVED***':
        return '***REMOVED***'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
    
@app.route('/laptoppower/api/v1.0/profiles', methods = ['GET'])
@auth.login_required
def get_list():
    return jsonify(laptop_control.list())

@app.route('/laptoppower/api/v1.0/profiles/<guid>', methods = ['GET'])
@auth.login_required
def get_profile(guid):
    profile = laptop_control.query(guid)
    if not profile:
        abort(404) 
    return jsonify({'profile': profile})

@app.route('/laptoppower/api/v1.0/profiles/aliases', methods = ['GET'])
@auth.login_required
def get_aliases():
    return jsonify({'aliases': laptop_control.get_aliases()})

@app.route('/laptoppower/api/v1.0/profiles/active', methods = ['GET'])
@auth.login_required
def get_active():
    return jsonify({'plan': laptop_control.get_active()})

@app.route('/laptoppower/api/v1.0/battery/soc', methods = ['GET'])
@auth.login_required
def get_soc():
    return jsonify(laptop_control.get_estimated_charge_remaining())

@app.route('/laptoppower/api/v1.0/battery/soc/estimatedruntime', methods = ['GET'])
@auth.login_required
def get_estimated_run_time():
    return jsonify(laptop_control.get_estimated_run_time())

@app.route('/laptoppower/api/v1.0/profiles/setprofile', methods = ['POST'])
@auth.login_required
def set_profile():
    if not request.json or not 'guid' in request.json:
        abort(400)
    response = laptop_control.set_active(request.json['guid'])
    return jsonify( { 'response': response } ), 201

@app.route('/laptoppower/api/v1.0/profiles/setprofilebyname', methods = ['POST'])
@auth.login_required
def set_profile_by_name():
    if not request.json or not 'name' in request.json:
        abort(400)
    response = laptop_control.set_active_by_name(request.json['name'])
    return jsonify( { 'response': response } ), 201

@app.route('/laptoppower/api/v1.0/profiles/deleteprofile/<guid>', methods = ['DELETE'])
@auth.login_required
def delete_profile(guid):
    if len(guid) == 0:
        abort(404)
    response = laptop_control.delete_scheme(guid)
    return jsonify( { 'response': response } )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
