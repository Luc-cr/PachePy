from commands import commands
from network import *
import threading
import json
import sys

# Load Config file
file = open("config.json", "r")
file = json.loads(file.read())

servers = {}
runing = {}

if file['start']['autorun']:
  servers['autorun'] = server(file['start']['host'], file['start']['port'], file['start']['dir'], file['file']['autoread'])
  pro = threading.Thread(target=servers['autorun'].start)
  pro.start()
  runing['autorun'] = pro


# Create commands
cmd = commands()

@cmd.addCommand("help", "(Display all commands)", "")
def help(args):
  commands = "Commands available: \n"
  for i in cmd.events.values():
    commands = commands + i[1]
  return commands 

@cmd.addCommand("exit", "(Exit the comand prompt)", "")
def exit(args):
  for i in runing.values():
    pass
  return sys.exit(0)

@cmd.addCommand("services", "(Display all servers runing)", "")
def services(args):
  s = ""
  for i in runing.keys():
    s += "\n" + i  
  return f"Servers runing: {s}"

@cmd.addCommand("init", "(init the server)", "'name' 'host' 'port' 'dir' 'doc'")
def start(args):
  if len(args) < 2:
    servers[args[0]] = server(args[1], int(args[2]), args[3], args[4])  
  servers[args[0]] = server(args[1], int(args[2]))
  return "Server initialized"

@cmd.addCommand("run", "(Run the server)", "'name'")
def run(args):
  if args[0] not in servers.keys():
    return "Server not found, check the servers"
  pro = threading.Thread(target=servers[args[0]].start)
  pro.start()
  runing[args[0]] = pro
  return "Running " + args[0]

@cmd.addCommand("status", "(Get the status of a server)", "'name'")
def status(args):
  if args[0] not in servers.keys():
    return "Server not found, check the servers"
  serv = servers[args[0]]
  data = f"Status: \n Running: {serv.status}\n Host: {serv.host} \n Port: {serv.port}"
  return data

@cmd.addCommand("stop", "(Stop server)", "'name'")
def stop(args):
  if args[0] not in servers.keys():
    return "Server not found, check the servers"
  runing[args[0]]._stop
  runing.__delitem__(args[0])
  return ""
  
@cmd.addCommand("save", "(Save server config)", "'name'")
def save(args):
  if args[0] not in servers.keys():
    return "Server not found, check the servers"
  serv = servers[args[0]]
  return serv.getConfig()