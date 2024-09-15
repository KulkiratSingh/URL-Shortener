#!/usr/bin/env python3
import random
import string
import sys
import uuid
from flask import Flask, jsonify, abort, request, make_response, session, redirect
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import pymysql
import pymysql.cursors
import ssl
import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST

Session(app)

@app.errorhandler(400) 
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

@app.errorhandler(500)
def not_found(error):
	return make_response(jsonify( { 'status': 'Internal server error' } ), 500)

dbConnection = pymysql.connect(host=settings.DB_HOST,
					user=settings.DB_USER,
					password=settings.DB_PASSWD,
					database=settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)

sqlProcName = 'checkUserInDb'

class Root(Resource):
	def get(self):
		return app.send_static_file('index.html')
	
def generate_alias():
    # Generate a random UUID
    link_id = str(uuid.uuid4())

    # Extract the first six characters to use as the short link
    short_link = link_id[:6]

    return short_link

class SignIn(Resource):
	""" 
		curl -i -H "Content-Type: application/json" -X POST -d '{"username": "username", "password": "password"}' -c cookie-jar -k https://cs3103.cs.unb.ca:8009/signin
	"""
	def post(self):

		if not request.json:
			abort(400)

		parser = reqparse.RequestParser()
		try:
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400)
		
		if request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				
			
				cursor = dbConnection.cursor()
				cursor.callproc('checkUserInDb', [request_params['username']])
				
				results = cursor.fetchall()

				for row in results:
					user_exists_in_database = row['count'] > 0
					if(not(user_exists_in_database)):
						cursor.callproc('insertUserIntoDB', [request_params['username']])
						dbConnection.commit()
						print("user added to db -> " , request_params['username'])
					else:
						print("user exists already -> " , request_params['username'])
				
				session['username'] = request_params['username']

				#read user by sending session username which in return will give us userid to be added in sessio 
				cursor.callproc('readUser', [session['username']])
				results = cursor.fetchall()
				session['user_id'] = results[0]['user_id']

				response = {'Authentication': 'success', 
							'user': request_params['username'],
							'userID': session['user_id'],
							}
				responseCode = 201
			except LDAPException:
				response = {'status': 'Access denied'}
				print(response)
				responseCode = 401
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)
	
	def delete(self):
		if 'username' in session:
			session.clear()
			response = {'status': 'Sign Out Successful' }
			responseCode = 200
		else:
			response = {'status': 'Not Signed In' }
			responseCode = 401

		return make_response(jsonify(response), responseCode)
	


class All_LinksForUser(Resource):
	""" 
		curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:8009/users/{user_id}/links
	"""
	def get(self, user_id):
		print("Session ID: ", session['user_id'])
		print("Local ID: ", user_id)
		print(session['user_id']==user_id)
		if 'username' in session and session['user_id']==user_id:
			try:
				cursor = dbConnection.cursor()
				cursor.callproc('getUserURLs', [user_id])
				dbConnection.commit()
				
				results = cursor.fetchall()
				print("results -> " , results)
				response = results
				responseCode = 200
			except Exception as e:
				print("Error:", e)
				dbConnection.rollback()
				response = {'Error': "Internal Server Error"}
				responseCode = 500
				return make_response(jsonify(response), responseCode)
		else:
			response = {'status': 'unauthorized'}
			responseCode = 401

		return make_response(jsonify(response), responseCode)
	

class GiveShortURL(Resource):
	""" 
		curl -i -H "Content-Type: application/json" -X POST -d '{"originalURL": "url"}' -b cookie-jar -k https://cs3103.cs.unb.ca:8009/users/{user_id}/link
	"""
	def post(self, user_id):
		print("Session ID: ", session['user_id'])
		print("Local ID: ", user_id)
		print(session['user_id']==user_id)
		if 'username' in session and session['user_id']==user_id:
			print("Logic to create a tinyURL")

			# Parsing originalLink sent in body
			parser = reqparse.RequestParser()
			parser.add_argument('originalURL', type=str, required=True)
			args = parser.parse_args()

			original_url = args['originalURL']
			if original_url:
				print("Original URL:", original_url)

				#Logic to create a tinyURL using the originalLink
				alias = generate_alias()
				print('alias is ' , alias)

				try:
					cursor = dbConnection.cursor()
					print("SAVING INTO DB ....")
					cursor.callproc('insertURLIntoDB', [original_url, alias, user_id])
					dbConnection.commit()
				except Exception as e:
					print("Error:", e)
					dbConnection.rollback()
					response = {'Error': "Internal Server Error"}
					responseCode = 500
					return make_response(jsonify(response), responseCode)
					
				
				return {"shortLink": "https://cs3103.cs.unb.ca:" + str(settings.APP_PORT) + "/" + alias,
						"success": True,
						"userID": user_id
					}
			else:
				return make_response(jsonify( { 'status': 'Bad request' } ), 400)

		else:
			return make_response(jsonify({'status': 'Unauthorized'}), 401)


class Get_Del_Update_Link(Resource):
	""" 
		curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:8009/users/{user_id}/links/{link_id}
	"""
	def get(self, user_id, link_id):
		if 'username' in session and session['user_id']==user_id:
			try:
				cursor = dbConnection.cursor()
				cursor.callproc('getUserURL', [link_id , user_id])
				dbConnection.commit()

				results = cursor.fetchall()
				response = results[0]
				responseCode = 200

			except Exception as e:
				print("Error:", e)
				dbConnection.rollback()
				response = {'Error': "Internal Server Error, Check your url id and linkID. No link associated with given userID"}
				responseCode = 500
				return make_response(jsonify(response), responseCode)
		else:
			response = {'status': 'unauthorized'}
			responseCode = 401

		return make_response(jsonify(response), responseCode)

	""" 
		curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8009/users/{user_id}/links/{link_id}
	"""
	def delete(self, user_id, link_id):
		if 'username' in session and session['user_id']==user_id:
			try:
				cursor = dbConnection.cursor()
				cursor.callproc('deleteURL', [link_id , user_id])

				dbConnection.commit()
				response = {}
				responseCode = 204 #204 No content so no response returned

			except Exception as e:
				print("Error:", e)
				dbConnection.rollback()
				response = {'Error': "Internal Server Error, Check your url id and linkID. No link associated with given userID"}
				responseCode = 500
				return make_response(jsonify(response), responseCode)
		else:
			response = {'status': 'unauthorized'}
			responseCode = 401

		return make_response(jsonify(response), responseCode)
	
	def put(self, user_id, link_id):
		if 'username' in session and session['user_id'] == user_id:
			try:
				data = request.get_json()

				if 'alias' not in data:
					raise ValueError("Missing alias in request body")

				alias = data['alias']

				print("updated", alias)

				# Get specified short url for user
				cursor = dbConnection.cursor()
				cursor.callproc('getUserURL', [link_id, user_id])
				results = cursor.fetchall()

				if results:
					original_url = results[0]['url']

					cursor.callproc('updateShort', [link_id, user_id, alias])
					dbConnection.commit()

					response = {
						'message': 'Short URL alias added successfully',
						'shortURL': "https://cs3103.cs.unb.ca:" + str(settings.APP_PORT) + "/" + alias,
						'org_url': original_url
					}
					responseCode = 200
				else:
					response = {'Error': "Link not found for the given user ID and link ID"}
					responseCode = 404
			except Exception as e:
				print("Error:", e)
				dbConnection.rollback()
				response = {'Error': "Internal Server Error, Check your url id and linkID. No link associated with given userID"}
				responseCode = 500
				return make_response(jsonify(response), responseCode)
		else:
			response = {'status': 'unauthorized'}
			responseCode = 401

		return make_response(jsonify(response), responseCode)

class Validate_Session(Resource):
	def get(self):
		if 'username' in session:
			cursor = dbConnection.cursor()
			cursor.callproc('readUser', [session['username']])
			dbConnection.commit()
			results = cursor.fetchall()
			print("VALIDATE SESSION RESULTS not(results) -> " , not(results))
			if(not(results)):
				session.clear()
				return make_response(jsonify({"isAuthenticated": False}), 401)
			else:
				return make_response(jsonify({"isAuthenticated": True, "userID": session["user_id"]}), 200)
		else:
			return make_response(jsonify({"isAuthenticated": False}), 401)

class DeleteUser(Resource):
	def delete(self, user_id):
		if 'username' in session and session['user_id'] == user_id:
			cursor = dbConnection.cursor()
			cursor.callproc('deleteUser' , [user_id])
			dbConnection.commit()
			response = {}
			responseCode = 204 #204 No content so no response returned
		else:
			response = {'status': 'unauthorized'}
			responseCode = 401

		return make_response(jsonify(response), responseCode)

class VisitLink(Resource):
	def get(self, alias):
		cursor = dbConnection.cursor()
		cursor.callproc('getURLFromAlias', [alias])
		results = cursor.fetchall()
		if results:
			url_id = results[0]["url_id"]
			cursor.callproc('incrementCounter', [url_id])
			dbConnection.commit()
			print(results)
			return redirect(results[0]["url"], 302)

api = Api(app)
api.add_resource(Root,'/')
api.add_resource(SignIn, '/signin')
api.add_resource(DeleteUser, '/delete_user/<int:user_id>')
api.add_resource(GiveShortURL, '/users/<int:user_id>/link')
api.add_resource(All_LinksForUser, '/users/<int:user_id>/links')
api.add_resource(Get_Del_Update_Link, '/users/<int:user_id>/links/<int:link_id>')
api.add_resource(Validate_Session, '/validate_session')
api.add_resource(VisitLink, '/<string:alias>')

if __name__ == "__main__":
	context = ('cert.pem', 'key.pem')
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)