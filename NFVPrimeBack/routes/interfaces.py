from flask import Blueprint, request, jsonify
import lib.handleLibs as hl
import lib.interfaceLibs as il
import lib.loginLibs as ll
from lib.threadingLibs import ThreadWithReturnValue
from lib.connection import conn
import time
import os
import sys
from dotenv import load_dotenv

load_dotenv()     # this loads in the environment variables from the .env file

interfaces_blueprint = Blueprint('interface', __name__)

wdir = os.getenv("NFVPRIME_PATH")

@interfaces_blueprint.route('/createInterface', methods=['POST'])
def createInterface():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        path = wdir + '/Arquivos/' + req_data["username"]
        if not os.path.isdir(path):
            os.mkdir(path)
        output_file = open(path + '/errorCriaDummy.txt', 'w+')
        userId = ll.getUserIdByUsername(conn, req_data)
        newInterfaceId = il.getMaxInterfaceId(conn, userId)
        interfaceHostNumber, newHostEthernet, newNamespaceEthernet = il.getInterfaceMaxValues(conn)
        newInterfaceHostIp = "10.0.1." + str(interfaceHostNumber)
        newInterfaceNamespaceIp = "10.0.2." + str(interfaceHostNumber)
        newInterfaceName = "dummy_" + str(userId) + "_" + str(newInterfaceId)
        newInterfaceHostName = "veth-h{}".format(newInterfaceId)
        newInterfaceNamespaceName = "veth-n{}".format(newInterfaceId)
        comando = il.dummyInterface(newInterfaceId, newInterfaceHostIp, newInterfaceNamespaceIp, newHostEthernet, newNamespaceEthernet)

        thread = ThreadWithReturnValue(target=hl.executeProgramOutput, args=(comando, output_file))
        thread.start()
        thread.join()
        il.insertUserInterface(conn, userId, newInterfaceId, newInterfaceName, newInterfaceHostName, newInterfaceHostIp, newInterfaceNamespaceName, newInterfaceNamespaceIp, newHostEthernet, newNamespaceEthernet)

        time.sleep(0.03)

        dummySnifferHost, dummySnifferNamespace = hl.dummySnifferProgram(newInterfaceHostName, newInterfaceHostIp, newInterfaceNamespaceName, newInterfaceNamespaceIp)
        path = wdir + '/Arquivos/' + req_data["username"] + '/Sniffers'
        if not os.path.isdir(path):
            os.mkdir(path)
    
        snifferProgram = open(path + '/sniffer_' + newInterfaceName + '_namespace.py', 'w+')
        snifferProgram.write(dummySnifferNamespace)
        snifferProgram.close()

        comando = "sudo ip netns exec NFVPrime python3 " + wdir + "/Arquivos/"+ req_data["username"]+ "/Sniffers/sniffer_" + newInterfaceName + "_namespace.py"
        output_file = open(path + '/errorNamespaceSniffers.txt', 'w+')

        thread = ThreadWithReturnValue(target=hl.executeProgramArmazenaPidPython, args=(conn, userId, comando, output_file, "sniffer", "snif_" + newInterfaceName + "_ns"))
        thread.start()

        interfaces = il.getUserInterfaces(conn, userId)

        return jsonify(interfaces)
    else:
        return jsonify(error="Erro ao criar nova interface!")
    
@interfaces_blueprint.route('/searchInterfaces', methods=['POST'])
def buscaInterfaces():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        interfaces = il.getUserInterfaces(conn, userId)

        return jsonify(interfaces)
    else:
        return jsonify(error="Erro ao buscar interfaces!")
    
@interfaces_blueprint.route('/deleteInterface/<id>', methods=['DELETE'])
def deleteInterface(id):
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        il.deleteInterface(conn, userId, id)
        interfaces = il.getUserInterfaces(conn, userId)

        return jsonify(interfaces)
    else:
        return jsonify(error="Erro ao deletar interface!")
    
@interfaces_blueprint.route('/deleteAllUserInterfaces', methods=['POST'])
def deleteAllUserInterfaces():
    req_data = request.get_json()
    print(req_data)
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        il.deleteAllInterfaces(conn, userId)
        return jsonify(msg="Ok")
    else:
        return jsonify(error="Erro ao parar os processos!")