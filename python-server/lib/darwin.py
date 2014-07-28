
from glob import glob

def possible_devices():
  return glob("/dev/tty.Mind*")
