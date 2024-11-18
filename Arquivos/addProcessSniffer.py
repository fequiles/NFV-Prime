import sys
import threading #thread module imported
import subprocess
import time
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres",
    port="5432")

def updateProcessMemCpu(mem, cpu):
    curs_obj = conn.cursor()

    curs_obj.execute("UPDATE pids SET mem = {}, cpu = {} WHERE pid = {}".format(mem, cpu, sys.argv[1]))
    conn.commit()
    curs_obj.close()

def handleOutput(output):
    string = output.decode('utf-8')
    values = string.split('\n')[1] if len(string.split('\n')) > 1 else ''
    if (values != ''):
      cpu = values.split(' ')[1]
      mem = values.split(' ')[3]
    else:
      cpu = 0
      mem = 0
    return cpu, mem

def handleChildPid(output):
    string = output.decode('utf-8')
    values = string.split('\n')[1] if len(string.split('\n')) > 1 else ''

    return values.split(' ')[2]

def thread_Time(thread_name, interval, pid):
    while 1:
        semaphore.acquire()
        command = 'ps -p {} -o %cpu,%mem'.format(pid)
        print(command)
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            out, err = process.communicate()
        except:
            exit()
        cpu, mem = handleOutput(out)
        updateProcessMemCpu(mem, cpu)
        semaphore.release()  
        time.sleep(interval)

if (len(sys.argv) != 2):
    print('Usage: python3 addProcessSnifer.py pid')
    exit()

pidArg = sys.argv[1]
command = 'ps --ppid {}'.format(pidArg)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
out, err = process.communicate()
childPid = handleChildPid(out)

semaphore = threading.Semaphore(1)
timer = threading.Thread(target=thread_Time, args=('timer', 0.5, childPid))
timer.start()
