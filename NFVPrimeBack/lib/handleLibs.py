import subprocess
import os
import signal
import lib.interfaceLibs as il
from dotenv import load_dotenv

load_dotenv()     # this loads in the environment variables from the .env file

wdir = os.getenv("NFVPRIME_PATH")

def interfaceReplace(program_txt, dummies):
    print(dummies)
    for i in range(0, len(dummies)):
        replacing = ":{}".format(dummies[i]["name"])
        print(replacing)
        program_txt = program_txt.replace(replacing, "\""+dummies[i]["hostip"]+"\"")
    return program_txt

def nfvHeaderWrite(program_txt, dummies):
    header = open(wdir + "/Arquivos/lib/header.txt", "r")
    header_content = header.read()
    new_program = header_content + program_txt
    new_program = interfaceReplace(new_program, dummies)
    return new_program

def dummySnifferProgram(hostName, hostIp, namespaceName, namespaceIp):
    # snifferDummyFile = open("../Arquivos/dummySnifferMask.py", "r")
    # snifferDummyProgram = snifferDummyFile.read()
    # snifferDummyProgram = snifferDummyProgram.replace(":dummyIp", "\"" + ip + "\"")

    snifferDummyHostFile = open(wdir + "/Arquivos/dummySnifferMaskHost.py", "r")
    snifferDummyNamespaceFile = open(wdir + "/Arquivos/dummySnifferMaskNamespace.py", "r")

    snifferDummyHostProgram = snifferDummyHostFile.read()
    snifferDummyHostProgram = snifferDummyHostProgram.replace(":dummyHostName", "\"" + hostName + "\"")
    snifferDummyHostProgram = snifferDummyHostProgram.replace(":dummyNamespaceName", "\"" + namespaceName + "\"")
    snifferDummyHostProgram = snifferDummyHostProgram.replace(":dummyHostIp", "\"" + hostIp + "\"")
    snifferDummyHostProgram = snifferDummyHostProgram.replace(":dummyNamespaceIp", "\"" + namespaceIp + "\"")

    snifferDummyNamespaceProgram = snifferDummyNamespaceFile.read()
    snifferDummyNamespaceProgram = snifferDummyNamespaceProgram.replace(":dummyHostName", "\"" + hostName + "\"")
    snifferDummyNamespaceProgram = snifferDummyNamespaceProgram.replace(":dummyNamespaceName", "\"" + namespaceName + "\"")
    snifferDummyNamespaceProgram = snifferDummyNamespaceProgram.replace(":dummyHostIp", "\"" + hostIp + "\"")
    snifferDummyNamespaceProgram = snifferDummyNamespaceProgram.replace(":dummyNamespaceIp", "\"" + namespaceIp + "\"")
    
    return snifferDummyHostProgram, snifferDummyNamespaceProgram

def netstatComand():
    path = "netstat -i"
    return path

def executeProgramArmazenaPidPython(conn, userId, path, outputFile, processType, processName):
    processo = subprocess.Popen("exec " + path, stdout=outputFile, shell=True, preexec_fn=os.setsid)
    processId = getNewPidIdByType(conn, userId, processType)
    savePid(conn, userId, processo.pid, processId, processType, processName)
    return processo.pid

def executeProgramArmazenaPid(conn, userId, path, outputFile, processType, processName):
    process = subprocess.Popen("exec " + path, stdout=outputFile, shell=True)
    processId = getNewPidIdByType(conn, userId, processType)
    savePid(conn, userId, process.pid, processId, processType, processName)

def executeProgramOutput(path, outputFile):
    processo = subprocess.Popen(path, stdout=outputFile, shell=True)

def executeProgram(path):
    processo = subprocess.Popen(path, shell=True)
    return processo

def killAllProcess(conn, userId, data):
    pid = 0
    processType = 1

    processTypeList = data["typeList"]
    curs_obj = conn.cursor()
    curs_obj.execute("SELECT pid, process_type FROM pids WHERE user_id = {} AND process_type in({})".format(userId, processTypeList))
    rows = curs_obj.fetchall()
    curs_obj.close()

    trafficKilled = False
    for row in rows:
        if (row[processType] != "traffic"):
            try: 
                os.killpg(os.getpgid(row[pid]), signal.SIGTERM)
            except:
                print("Pid doesn't exist")
        else:
            if (not trafficKilled):
                process = executeProgram('sudo ip netns exec NFV-client pkill -9 -f nping')
                process.wait()

    curs_obj = conn.cursor()
    curs_obj.execute("DELETE FROM pids WHERE user_id = {} AND process_type in({})".format(userId, processTypeList))
    conn.commit()
    curs_obj.close()


def killProgramProcess(listProcess):
    os.killpg(os.getpgid(listProcess["program"]["PID"]), signal.SIGTERM)
    listProcess.pop("program")

def savePid(conn, userId, pid, processId, processType, processName):
    curs_obj = conn.cursor()
    curs_obj.execute("INSERT INTO pids(user_id, pid, pid_id_by_type, process_type, process_name) VALUES({}, {}, {}, '{}', '{}')".format(userId, str(pid), processId, processType, processName))
    conn.commit()
    curs_obj.close()

def getNewPidIdByType(conn, userId, processType):
    id = 0
    curs_obj = conn.cursor()
    curs_obj.execute("SELECT max(pid_id_by_type) FROM pids WHERE user_id = {} AND process_type = '{}'".format(userId, processType))
    rows = curs_obj.fetchall()
    curs_obj.close()

    pidIdByType = rows[0][id] if rows[0][id] != None else 0

    return pidIdByType + 1

def getPidByProcessName(conn, userId, processName):
    curs_obj = conn.cursor()

    print("SELECT pid FROM pids WHERE user_id = '{}' AND process_name = '{}'".format(userId, processName))
    curs_obj.execute("SELECT pid FROM pids WHERE user_id = '{}' AND process_name = '{}'".format(userId, processName))
    rows = curs_obj.fetchall()
    pid = rows[0][0] if rows[0][0] != None else 0
    curs_obj.close()
    return pid

def getPidByIdPerType(conn, userId, id, processType):
    pid = 0
    curs_obj = conn.cursor()
    curs_obj.execute("SELECT pid FROM pids WHERE user_id = {} AND process_type = '{}' AND pid_id_by_type = {}".format(userId, processType, id))
    rows = curs_obj.fetchall()
    curs_obj.close()

    processPid = rows[0][pid] if rows[0][pid] != None else 0
    return processPid

def getPidByProcessType(conn, userId, processType):
    pid = 0
    curs_obj = conn.cursor()
    curs_obj.execute("SELECT pid FROM pids WHERE user_id = {} AND process_type = '{}' LIMIT 1".format(userId, processType))
    rows = curs_obj.fetchall()
    curs_obj.close()

    processPid = rows[0][pid] if rows[0][pid] != None else 0
    return processPid

def deletePid(conn, userId, pid):
    curs_obj = conn.cursor()
    curs_obj.execute("DELETE FROM pids WHERE user_id = {} AND pid = {}".format(userId, pid))
    conn.commit()
    curs_obj.close()

def killProcess(processPid):
    os.kill(processPid, signal.SIGKILL)