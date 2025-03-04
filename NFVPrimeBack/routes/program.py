from flask import Blueprint, request, jsonify, abort
import lib.handleLibs as hl
import lib.interfaceLibs as il
import lib.loginLibs as ll
import lib.programLibs as pl
from lib.threadingLibs import ThreadWithReturnValue
from lib.connection import conn
import time
import os
import sys

program_blueprint = Blueprint('program', __name__)

@program_blueprint.route('/postProgram', methods=['POST'])
def postClientProgram():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        path = '../Arquivos/' + req_data["username"]
        if not os.path.isdir(path):
            os.mkdir(path)
        received_file = open(path + '/program.py', 'w')
        output_file = open(path + '/output.txt', 'w+')
        userId = ll.getUserIdByUsername(conn, req_data)
        interfaces = il.getUserInterfaces(conn, userId)
        if (len(interfaces) > 0):
            program = hl.nfvHeaderWrite(req_data["code"], list(interfaces.values()))
            received_file.write(program)
            received_file.close()
            comando = "sudo python3 /python-docker/Arquivos/"+ req_data["username"]+ "/program.py"

            processName = req_data["processName"]
            thread = ThreadWithReturnValue(target=hl.executeProgramArmazenaPidPython, args=(conn, userId, comando, output_file, "program", processName))
            thread.start()
            processPid = thread.join()

            comando = "sudo python3 /python-docker/Arquivos/addProcessSniffer.py " + str(processPid)
            thread = ThreadWithReturnValue(target=hl.executeProgramArmazenaPidPython, args=(conn, userId, comando, output_file, "process_sniffer", processName))
            thread.start()

            programs = pl.getPrograms(conn, userId)

            return jsonify(programs)    
        else:
            abort(404, description="None interfaces")   
    else:
        return jsonify(error="Erro ao gerar arquivo Python")
    
@program_blueprint.route('/stopProgram', methods=['POST'])
def stopProgram():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        pid = hl.getPidByProcessType(conn, userId, "program")
        hl.killProcess(pid)
        hl.deletePid(conn, userId, pid)
        
        programs = pl.getPrograms(conn, userId)

        return jsonify(programs)
    else:
        return jsonify(error="Erro ao parar os processos!")
    
@program_blueprint.route('/getProgramsSamples', methods=['POST'])
def programSamples():
    req_data = request.get_json()
    if ((req_data != None) and (req_data != "")):
        userId = ll.getUserIdByUsername(conn, req_data)
        
        programs = pl.getSamples(conn, userId)

        return jsonify(programs)
    else:
        return jsonify(error="Erro ao parar os processos!")