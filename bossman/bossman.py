#!/usr/bin/env python
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/account', methods=['POST'])
def index():
    if not request.json:
        return "need json", 400

    try:
        uid = request.json['uid']
        cn = request.json['cn']
        password = request.json['password']
        mail = request.json['mail']
        calnet_uid = request.json['calnetUid']
        login_shell = request.json.get('loginShell', '/bin/bash')
    except KeyError as e:
        return "missing key: {}".format(e), 400

    return "helo, world!"


if __name__ == '__main__':
    app.run(debug=True)
