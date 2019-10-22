# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, Response, jsonify
import requests, random, json
import sys
from datetime import datetime
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch(['10.0.1.69'])

###### FUNCOES ######
def elastic_insert(nome,sobrenome,cpf,email,sexo,dtNasc,senha):

	#es = Elasticsearch([ElkIP])

	doc = {
	    'nome': nome,
	    'sobrenome': sobrenome,
	    'cpf': cpf,
	    'email': email,
	    'sexo': sexo,
	    'dtNasc': dtNasc,
	    'senha': senha,
	}

	res = es.index(index="usuarios", body=doc)
	print(res['result'])

	#res = es.get(index="usuarios", doc_type='tweet', id=1)
	#print(res['_source'])

	es.indices.refresh(index="usuarios")

def elastic_search(cpf,senha):
	#es = Elasticsearch([ElkIP])

	doc = {
	    'cpf': cpf ,
	    'senha': senha,
	}

	#print "\n\n" + str(doc) + "\n\n"
	senha = str(doc['senha'])
	cpf = str(doc['cpf'])
	#print sobrenome
	#print nome
	#if cpf == "all" or senha == "all":
		#res = es.search(index="usuarios", body={"query": {"match_all": {}}})
		#res = es.search(index="usuarios", body={"query": {"query_string": { "query": "nome: %s AND sobrenome: %s" % (nome,sobrenome)}}})
	#else:
	res = es.search(index="usuarios", body={"query": {"query_string": { "query": "cpf: %s AND senha: %s" % (cpf,senha)}}})
	#	res = es.search(index="usuarios", body={"query": {"match_all": {}}})
	#print "\n\n" + str(res) + "\n\n" 
	print("Got %d Hits:" % res['hits']['total']['value'])
	result_list = []
	for hit in res['hits']['hits']:
		print hit
		#print "ID: %s " % hit["_id"]
		print("ID: %s | Nome: %s | Sobrenome: %s | Cpf: %s | Email: %s | Sexo: %s | dtNasc: %s | Senha: %s " % \
			(hit["_id"], hit["_source"]["nome"],\
				hit["_source"]["sobrenome"],\
				hit["_source"]["cpf"],\
				hit["_source"]["email"],\
				hit["_source"]["sexo"],\
				hit["_source"]["dtNasc"],\
				hit["_source"]["senha"]))
		result_list.append("ID: %s | Nome: %s | Sobrenome: %s | Cpf: %s | Email: %s | Sexo: %s | dtNasc: %s | Senha: %s " % \
			(hit["_id"], hit["_source"]["nome"],\
				hit["_source"]["sobrenome"],\
				hit["_source"]["cpf"],\
				hit["_source"]["email"],\
				hit["_source"]["sexo"],\
				hit["_source"]["dtNasc"],\
				hit["_source"]["senha"]))
	return result_list

def elastic_update(id,nome,sobrenome,cpf,email,sexo,dtNasc,senha):
	#es = Elasticsearch([ElkIP])
	#es = Elasticsearch(['10.0.1.69'])

	doc = {
	    'nome': nome,
	    'sobrenome': sobrenome,
	    'cpf': cpf,
	    'email': email,
	    'sexo': sexo,
	    'dtNasc': dtNasc,
	    'senha': senha,
	}

	res = es.index(index="usuarios", id=id, body=doc)
	print(res['result'])

def elastic_delete(id,nome,sobrenome,cpf,email,sexo,dtNasc,senha):
	#es = Elasticsearch([ElkIP])
	#es = Elasticsearch(['10.0.1.69'])

	# doc = {
	#     'nome': nome,
	#     'sobrenome': sobrenome,
	#     'cpf': cpf,
	#     'email': email,
	#     'sexo': sexo,
	#     'dtNasc': dtNasc,
	#     'senha': senha,
	# }

	res = es.delete(index="usuarios", id=id)
	print(res['result'])


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
	# ipElk = request.form['ipElk']
	nome = request.form['nome']
	sobrenome = request.form['sobrenome']
	cpf = request.form['cpf']
	email = request.form['email']
	sexo = request.form['sexo']
	dtNasc = request.form['dtNasc']
	senha = request.form['senha']
	elastic_insert(nome,sobrenome,cpf,email,sexo,dtNasc,senha)
	#print request.form
	#print "\n\nBateu aqui!"
	return jsonify({'output' : 'Usuario '+request.form['nome']+' cadastrado!!'})

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
	# ipElk = request.form['ipElk']
	cpf = request.form['cpf']
	senha = request.form['senha']
	search_result = elastic_search(cpf,senha)
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

@app.route('/update',methods= ['POST'])
def update():
	#print request.form
	#ElkIP = request.form['ElkIP']
	id_user = request.form['id_user']
	nome_user = request.form['nome_user']
	sobrenome_user = request.form['sobrenome_user']
	cpf_user = request.form['cpf_user']
	email_user = request.form['email_user']
	sexo_user = request.form['sexo_user']
	dtNasc_user = request.form['dtNasc_user']
	senha_user = request.form['senha_user']
	#elastic_update(id_user,nome_user,sobrenome_user,ElkIP)
	elastic_update(id_user,nome_user,sobrenome_user,cpf_user,email_user,sexo_user,dtNasc_user,senha_user)
	return jsonify({'output' : 'Valor atualizado!'})

@app.route('/delete',methods= ['POST'])
def delete():
	#print "\n\nChamou o DELETE\n\n"
	#print request.form
	#ElkIP = request.form['ElkIP']
	id_user = request.form['id_user']
	nome_user = request.form['nome_user']
	sobrenome_user = request.form['sobrenome_user']
	cpf_user = request.form['cpf_user']
	email_user = request.form['email_user']
	sexo_user = request.form['sexo_user']
	dtNasc_user = request.form['dtNasc_user']
	senha_user = request.form['senha_user']
	#elastic_delete(id_user,nome_user,sobrenome_user,ElkIP)
	elastic_delete(id_user,nome_user,sobrenome_user,cpf_user,email_user,sexo_user,dtNasc_user,senha_user)
	return jsonify({'output' : 'Valor removido!'})

if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)