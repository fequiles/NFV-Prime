import os
import signal

def npingComand(data, interfaceHost):
    # path = 'sudo docker exec -it generator sh -c "nping --udp'
    path = 'sudo ip netns exec NFV-client nping --udp'
    if (data["lenght"] != 0):
        path += " --data-len " + str(data["lenght"])
    if (data["rate"] != 0):
        path += " --rate " + str(data["rate"])
    if (data["delay"] != 0):
        path += " --delay " + str(data["delay"]) + "ms"
    if (data["port"] != 0):
        path += " -p " + str(data["port"])
    else: 
        path += " -p 8001"
    path += " -c " + str(data["count"]) + " "
    
    path += interfaceHost

    return path

def getMaxTrafficsGenerator(conn, userId):
    id = 0

    curs_obj = conn.cursor()
    curs_obj.execute("SELECT max(pid_id_by_type) FROM pids WHERE user_id = {} AND process_type = '{}'".format(userId, "traffic_p"))
    rows = curs_obj.fetchall()
    trafficGeneratorId = rows[0][id] if rows[0] != None else 0
    curs_obj.close()

    return trafficGeneratorId

def getTraffics(conn, userId):
    id = 0
    name = 1

    curs_obj = conn.cursor()
    curs_obj.execute("SELECT pid_id_by_type, process_name FROM pids WHERE user_id = {} AND process_type = '{}'".format(userId, "traffic"))
    rows = curs_obj.fetchall()
    curs_obj.close()

    traffics = {}

    i = 1
    for row in rows:
        traffic = {
            "pid": row[id],
            "processName": row[name]
        }
        traffics["traffic_"+ str(i)] = traffic
        i += 1

    return traffics

def getTrafficsProfiles(conn, userId):
    profile_name = 0	
    rate = 1
    packet_lenght = 2
    packet_counter = 3
    delay = 4
    port = 5
    traffic_trigger = 6

    curs_obj = conn.cursor()
    curs_obj.execute("SELECT profile_name, rate, packet_lenght, packet_counter, delay, port, traffic_trigger FROM user_traffic_profiles WHERE (user_id = {} or user_id = 0)".format(userId))
    rows = curs_obj.fetchall()
    curs_obj.close()

    traffics = []

    i = 1
    for row in rows:
        program = {
            "title": row[profile_name],
            "value": '{},{},{},{},{},{},{}'.format(row[profile_name],row[rate],row[packet_lenght],row[packet_counter],row[delay],row[port],row[traffic_trigger])
        }
        traffics.append(program)
        i += 1

    return traffics

def trafficConfigsValidator(data):
    if data["lenght"] == 0:
        return 404
    else:
        return 200
    
def killTrafficProcess(processPid):
    try:
        os.kill(processPid, signal.SIGKILL)
    except:
        print("Pid doesn't exist")