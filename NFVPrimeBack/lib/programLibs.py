def getPrograms(conn, userId):
    id = 0
    name = 1

    curs_obj = conn.cursor()
    curs_obj.execute("SELECT pid_id_by_type, process_name FROM pids WHERE user_id = {} AND process_type = '{}'".format(userId, "program"))
    rows = curs_obj.fetchall()
    curs_obj.close()

    programs = {}

    i = 1
    for row in rows:
        program = {
            "pid": row[id],
            "processName": row[name]
        }
        programs["program"+ str(i)] = program
        i += 1

    return programs

def getSamples(conn, userId):
    filename = 0
    file = 1

    curs_obj = conn.cursor()
    curs_obj.execute("SELECT filename, file FROM user_files WHERE user_id = {}".format(userId))
    rows = curs_obj.fetchall()
    curs_obj.close()

    programs = []

    i = 1
    for row in rows:
        program = {
            "title": row[filename],
            "value": row[file].tobytes()
        }
        programs.append(program)
        i += 1

    return programs
