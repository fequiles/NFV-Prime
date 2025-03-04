#!/usr/bin/python3

from distutils.log import debug
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import os
import sys
import subprocess
sys.path.append( '/lib' )
import lib.handleLibs as hl
import lib.loginLibs as ll
import lib.graphicsLibs as gl
import lib.interfaceLibs as il
from lib.threadingLibs import ThreadWithReturnValue
from lib.connection import conn
from routes.traffic import traffic_blueprint
from routes.interfaces import interfaces_blueprint
from routes.program import program_blueprint

#Global vars
listProcess = {}

process = subprocess.Popen('sh /home/felipe/Desktop/NFV-Prime/config.sh', shell=True)
process.wait()
clientSniffer = 'sudo ip netns exec NFV-client python3 /home/felipe/Desktop/NFV-Prime/Arquivos/dummySnifferClient.py'
path = '/home/felipe/Desktop/NFV-Prime/Arquivos/sniffers'
output_file = open(path + '/errorClientSniffers.txt', 'w+')
thread = ThreadWithReturnValue(target=hl.executeProgramArmazenaPid, args=(conn, 0, clientSniffer, output_file, "sniffer_client", "snif_client"))
thread.start()

app = Flask(__name__)
CORS(app)

app.register_blueprint(traffic_blueprint, url_prefix="/traffic")
app.register_blueprint(interfaces_blueprint, url_prefix="/interface")
app.register_blueprint(program_blueprint, url_prefix="/program")

@app.route('/')

@app.route('/nfvprime/getTrafficInfos', methods=['POST'])
def getTrafficInfos():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        interfaces = gl.getInterfacesRxTx(conn, userId)

        return jsonify(interfaces)
    else:
        return jsonify("Erro ao gerar trafego!")
    
@app.route('/nfvprime/getProcessInfos', methods=['POST'])
def getProcessInfos():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        processInfos = gl.getProgramMemCpu(conn, userId)

        return jsonify(processInfos)
    else:
        return jsonify("Erro ao gerar trafego!")

@app.route('/nfvprime/stopAll', methods=['POST'])
def stopAll():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        il.deleteAllInterfaces(conn, userId)
        hl.killAllProcess(conn, userId, req_data)
        return jsonify(msg="Ok")
    else:
        return jsonify(error="Erro ao parar os processos!")
    
@app.route('/nfvprime/stopAllProcesses', methods=['POST'])
def stopAllProcesses():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        hl.killAllProcess(conn, userId, req_data)
        return jsonify(msg="Ok")
    else:
        return jsonify(error="Erro ao parar os processos!")

@app.route('/nfvprime/startGraficos', methods=['POST'])
def iniciaGraficos():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        path = '../Arquivos/' + req_data["username"]
        if not os.path.isdir(path):
            os.mkdir(path)
        userId = ll.getUserIdByUsername(conn, req_data)
        output_file = open(path + '/output.txt', 'w+')
        comando = "sudo python3 /home/felipe/Desktop/NFV-Prime/Arquivos/networkSniffer.py"

        thread = ThreadWithReturnValue(target=hl.executeProgramArmazenaPidPython, args=(conn, userId, comando, output_file, "graphics", "sniffer_graphics"))
        thread.start()

        return jsonify(msg="Ok")
    else:
        return jsonify(error="Erro iniciar os Graficos!")
    
@app.route('/createUser', methods=['POST'])
def createUser():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        ll.createUser(conn, req_data['data'])
        return jsonify("Ok")
    else:
        return jsonify(error="Erro criar Usuário")

@app.route('/getUserIdByUsername', methods=['POST'])
def getUserIdByUsername():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        id = ll.getUserIdByUsername(conn, req_data['data'])
        return jsonify(
            userId=id
        )
    else:
        return jsonify(error="Erro criar Usuário")

if __name__ == "__main__":
    app.run(debug=False)