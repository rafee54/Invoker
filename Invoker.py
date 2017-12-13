#!twitch-project/bin/python

import sqlite3
import argparse
import time
import numpy as np
from twitchstream.chat import TwitchChatStream
from json import dumps
from flask import Flask, url_for, g, render_template
from sqlalchemy import create_engine #modified
from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///spell.db')

def make_public_question(question):
    new_question = {}
    for field in question:
        if field == 'id':
            new_question['uri'] = url_for('get_question',question_id=question['id'], _external=True)
        else:
            new_question[field] = question[field]
    return new_question

app = Flask(__name__)

@app.route('/spells', methods=['GET'])
def get_questions():
    conn = db_connect.connect()
    query = conn.execute("select * from spells")
    spell_list = {'id': [i[0] for i in query.cursor.fetchall()]}
    return jsonify(spell_list)

@app.route('/spells/<number>', methods=['GET'])
def get_thequestions(number):
    conn = db_connect.connect()
    query = conn.execute("select * from spells where id = %d" %int(number))
    result = {'id': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return jsonify(result)

@app.route('/getorb', methods=['GET'])
def voting():
    Quas = 0;
    Wex = 0;
    Exort = 0;
    with TwitchChatStream(username='TwitchPlaysInvoker',oauth='',verbose=False) as chatstream:
	chatstream.send_chat_message('Voting for action has begun.')
	timer = 60
	while timer > 0:
	    time.sleep(1)
            received = chatstream.twitch_receive_messages()
            if received:
		    if chat_message['message'].lower() == 'q': Quas += 1;
		    if chat_message['message'].lower() == 'w': Wex += 1;
            if chat_message['message'].lower() == 'e': Exort += 1;
	    timer-=1;
    result = {"Quas":Quas, "Wex":Wex, "Exort":Exort}
    return jsonify(result)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='192.168.0.8')
