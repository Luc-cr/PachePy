from network import server
from cmd import *
import sys

version = "0.0.1"
print(f"PyPache\nVersion: {version} \nAuthor: Luc")

while True:
  try:
    prompt = input("PyPache >> ").split(" ")
    if prompt[0] not in list(cmd.events.keys()):
      print("[Console] Command not found!!")
    else:
      print(f"[Console] {cmd.events[prompt[0]][0](prompt[1:])}")
  except KeyboardInterrupt:
    print("\n[Console] Bye!")
    sys.exit(0)