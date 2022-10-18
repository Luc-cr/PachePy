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
  servers['autorun'] = server(file['start']['host'], file['start']['port'], file['start']['dir'], file['start']['read'])
  pro = threading.Thread(target=servers['autorun'].start, args=())
  runing['autorun'] = pro
  pro.start()


# Create commands
cmd = commands()

@cmd.addCommand()
def help():
  """(Display all commands)"""
  commands = "Commands available: \n"
  for i in cmd.events.values():
    commands = commands + i[1]
  return commands 

@cmd.addCommand()
def exit():
  """(Exit the comand prompt)"""
  for i in runing.values():
    i.status = False
  return sys.exit(0)

@cmd.addCommand()
def services():
  """(Display all servers runing)"""
  s = ""
  for i in runing.keys():
    s += "\n" + i  
  return f"Servers runing: {s}"

@cmd.addCommand()
def init(name = "default", host = file['default']["host"], port = file['default']["port"], directory = file['default']["dir"], doc = file['default']["read"]):
  """(init the server)"""

  servers[name] = server(host, int(port), directory, doc)
  return "Server initialized"

@cmd.addCommand()
def run(name):
  """(Run the server)"""
  if name not in servers.keys():
    return "Server not found, check the servers"
  pro = threading.Thread(target=servers[name].start, args=())
  runing[name] = pro
  pro.start()
  return "Running " + name

@cmd.addCommand()
def status(name):
  """(Get the status of a server)"""
  if name not in servers.keys():
    return "Server not found, check the servers"
  serv = servers[name]
  data = f"Status: \n Running: {serv.status}\n Host: {serv.host} \n Port: {serv.port}"
  return data

@cmd.addCommand()
def stop(name):
  """(Stop server)"""
  if name not in servers.keys():
    return "Server not found, check the servers"
  servers[name].status = False
  runing.__delitem__(name)
  servers.__delitem__(name)
  return "Server stoped"

@cmd.addCommand()
def reload(name):
  """(Reload server)"""
  if name not in servers.keys():
    return "Server not found, check the servers"
  servers[name].status = False
  runing.__delitem__(name)
  pro = threading.Thread(target=servers[name].start, args=())
  runing[name] = pro
  pro.start()
  return "Server reloaded"
