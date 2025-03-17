from flask import Blueprint, request, jsonify
import lib.handleLibs as hl
import lib.loginLibs as ll
import lib.interfaceLibs as il
import lib.trafficLibs as tl
import os
from lib.threadingLibs import ThreadWithReturnValue
from lib.connection import conn
from dotenv import load_dotenv

load_dotenv()     # this loads in the environment variables from the .env file

traffic_blueprint = Blueprint('traffic', __name__)

wdir = os.getenv("NFVPRIME_PATH")

@traffic_blueprint.route('/postTrafficMode', methods=['POST'])
def postTrafficMode():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        path = wdir + '/Arquivos/' + req_data["username"]
        if not os.path.isdir(path):
            os.mkdir(path)
        output_file = open(path + '/nping_output.txt', 'w+')

        userId = ll.getUserIdByUsername(conn, req_data)
        trafficType = req_data["type"]
        processName = req_data["name"]

        print(trafficType)

        if trafficType == 'Automatic':
            if (tl.trafficConfigsValidator(req_data) != 200):
                return jsonify(error="Erro ao configurar trafego!")
            interfaceHost = il.getInterfaceHostIpById(conn, req_data, userId)
            comando = tl.npingComand(req_data, interfaceHost)
            thread = ThreadWithReturnValue(target=hl.executeProgramArmazenaPid, args=(conn, userId, comando, output_file, "traffic", processName))
            thread.start()
            
            thread.join()
        else:
            tgid = tl.getMaxTrafficsGenerator(conn, userId)
            path = wdir + '/Arquivos/' + req_data["username"] + '/Traffics'
            if not os.path.isdir(path):
                os.mkdir(path)
            output_file = open(path + '/trafficslogs.txt', 'w+')
            filename = 'traffic_generator_{}.py'.format(tgid)
            received_file = open('{}/{}'.format(path, filename), 'w+')
            received_file.write(req_data['code'])
            received_file.close()

            comando = "sudo ip netns exec NFV-client python3 " + wdir + "/Arquivos/"+ req_data["username"]+ "/Traffics/{}".format(filename)

            processName = '{}_{}'.format(req_data["name"], tgid)
            thread = ThreadWithReturnValue(target=hl.executeProgramArmazenaPidPython, args=(conn, userId, comando, output_file, "traffic_p", processName))
            thread.start()

        traffics = tl.getTraffics(conn, userId)

        return jsonify(traffics)
    else:
        return jsonify(error="Erro ao gerar trafego!")
    
@traffic_blueprint.route('/stopTraffic/<id>', methods=['DELETE'])
def stopTraffic(id):
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        pid = hl.getPidByIdPerType(conn, userId, id, "traffic")
        tl.killTrafficProcess(pid)
        hl.deletePid(conn, userId, pid)
        
        traffics = tl.getTraffics(conn, userId)

        return jsonify(traffics)
    else:
        return jsonify("Erro ao parar os processos!")
    
@traffic_blueprint.route('/searchTraffics', methods=['POST'])
def searchTraffics():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        traffics = tl.getTraffics(conn, userId)

        return jsonify(traffics)
    else:
        return jsonify(error="Erro ao buscar interfaces!")
    
@traffic_blueprint.route('/searchTrafficsProfiles', methods=['POST'])
def searchTrafficsProfiles():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        traffics = tl.getTrafficsProfiles(conn, userId)

        return jsonify(traffics)
    else:
        return jsonify(error="Erro ao buscar interfaces!")