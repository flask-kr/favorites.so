#!/usr/bin/env python
# coding: utf8

from flask import Flask, request, send_file, jsonify
import pymongo
import logging
import os
import traceback

app = Flask(__name__)
app.debug =True
# XXX: Bad. but who cares? -_-
app.config['INDEX'] = open('teaser/index.html').read()

mongo = pymongo.MongoClient('mongodb://localhost:27017')
sub = mongo.fvso_teaser.subscriber
sub.ensure_index([('email', pymongo.ASCENDING)], unique=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return app.config['INDEX']
    elif request.method == 'POST':
        email = request.form['email']
        print email
        try:
            sub.insert({'email':email})
            return jsonify({'valid':1, 'message':u'Thanks for your interest!'})
        except:
            #print traceback.format_exc()
            return jsonify({'valid':0, 'message':u'Seems you have already subscribed!'})
    else:
        raise NotImplemented

@app.route('/assets/<path:filename>')
def assets(filename):
    #print 'assets {}'.format(os.path.join('teaser', 'assets', filename))
    return send_file(os.path.join('teaser', 'assets', filename))

def run():
    app.run(host='0.0.0.0', port=57444)

if __name__ == "__main__":
    run()
