# Starts the node with the box named in config.py. The same file on every box.
import config
from node import Node

box = __import__("boxes." + config.BOX, None, None, ["setup", "loop"])
Node(config).run(box)
