# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, Response, jsonify
import requests, random, json
import sys
from datetime import datetime
from elasticsearch import Elasticsearch

app = Flask(__name__)

###### FUNCOES ######
def elastic_insert(nome,sobrenome,ElkIP):

	es = Elasticsearch([ElkIP])

	doc = {
	    'nome': nome ,
	    'sobrenome': sobrenome,
	}

	res = es.index(index="usuarios", body=doc)
	print(res['result'])

	#res = es.get(index="usuarios", doc_type='tweet', id=1)
	#print(res['_source'])

	es.indices.refresh(index="usuarios")

def elastic_search(nome,sobrenome,ElkIP):
	es = Elasticsearch([ElkIP])

	doc = {
	    'nome': nome ,
	    'sobrenome': sobrenome,
	}

	#print "\n\n" + str(doc) + "\n\n"
	sobrenome = str(doc['sobrenome'])
	nome = str(doc['nome'])
	#print sobrenome
	#print nome
	if nome == "all" or sobrenome == "all":
		res = es.search(index="usuarios", body={"query": {"match_all": {}}})
		#res = es.search(index="usuarios", body={"query": {"query_string": { "query": "nome: %s AND sobrenome: %s" % (nome,sobrenome)}}})
	else:
		res = es.search(index="usuarios", body={"query": {"query_string": { "query": "nome: %s AND sobrenome: %s" % (nome,sobrenome)}}})
	#	res = es.search(index="usuarios", body={"query": {"match_all": {}}})
	#print "\n\n" + str(res) + "\n\n" 
	print("Got %d Hits:" % res['hits']['total']['value'])
	result_list = []
	for hit in res['hits']['hits']:
		print hit
		#print "ID: %s " % hit["_id"]
		print("ID: %s | Nome: %s e Sobrenome: %s" % (hit["_id"], hit["_source"]["nome"],hit["_source"]["sobrenome"]))
		result_list.append("ID: %s | Nome: %s e Sobrenome: %s" % (hit["_id"], hit["_source"]["nome"],hit["_source"]["sobrenome"]))
	return result_list


#####################################

@app.route('/')
def home():
	# serve index template
	return render_template('index.html')

@app.route('/index.html')
def home2():
	# serve index template
	return render_template('index.html')

@app.route('/cadastro.html')
def cadastro():
	# serve index template
	return render_template('cadastro.html')

@app.route('/cadastro',methods= ['POST'])
def create_cadastro():
	ipElk = request.form['ipElk']
	usuario = request.form['usuario']
	senha = request.form['senha']
	elastic_insert(usuario,senha,ipElk)
	#print request.form
	#print "\n\nBateu aqui!"
	return jsonify({'output' : 'Usuario '+request.form['usuario']+' cadastrado!!'})

@app.route('/login.html')
def login():
	# serve index template
	#print request
	#print "\n\nUhuuuu"
	#return render_template('login.html', name=nome)
	#return "hello world"
	#usuario = request.form['usuario']
	usuario = "Fulaninho"
	return render_template('login.html', name=usuario)

@app.route('/login',methods= ['POST'])
def login_user():
	ipElk = request.form['ipElk']
	usuario = request.form['usuario']
	senha = request.form['senha']
	search_result = elastic_search(usuario,senha,ipElk)
	#print request.form
	output = search_result

	if len(output) > 0:
		#return "teste"
		#return login()
		#return login(usuario)
		return jsonify({'output': output[0] })
		#return render_template('login.html', name=usuario)
	else:
		return jsonify({'output' : 'Usuario nao encontrado!'})

if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)