def cleanDbInterfacesRxTx(conn, userId):
  curs_obj = conn.cursor()

  curs_obj.execute("UPDATE user_interfaces SET interface_tx = {}, interface_rx = {} WHERE user_id = {} or user_id = 0".format(0, 0, userId))
  conn.commit()
  curs_obj.close()

def getInterfacesRxTx(conn, userId):
    name = 0
    rx = 1
    tx = 2
    dict = {}
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT interface_id, coalesce(interface_rx, 0) as rx, coalesce(interface_tx, 0) as tx FROM user_interfaces WHERE user_id = {} or user_id = 0".format(userId))
    rows = curs_obj.fetchall()
    for row in rows:
      iId = row[name] if row[name] != None else 0
      iRx = row[rx] if row[rx] != None else 0
      iTx = row[tx] if row[tx] != None else 0
      interfaceRxTx = {iId: {'rx': iRx, 'tx': iTx}}
      dict.update(interfaceRxTx)
    
    curs_obj.close()

    cleanDbInterfacesRxTx(conn, userId)
    return dict

def getProgramMemCpu(conn, userId):
    name = 0
    mem = 1
    cpu = 2
    dict = {}
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT process_name, coalesce(mem, 0) as mem, coalesce(cpu, 0) as cpu FROM pids WHERE user_id = {} and process_type=\'program\'".format(userId))
    rows = curs_obj.fetchall()
    for row in rows:
      iId = row[name] if row[name] != None else 0
      iMem = row[mem] if row[mem] != None else 0
      iCpu = row[cpu] if row[cpu] != None else 0
      programMemCpu = {iId: {'mem': iMem, 'cpu': iCpu}}
      dict.update(programMemCpu)
    
    curs_obj.close()

    return dict