import os

WORKING_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
COVERS_DIR = WORKING_DIR + "covers/"
LOG_FILE = WORKING_DIR + "log.txt"

# Change working directory to init.py folder.
# Needed when we run under systemd because its cwd is "/".
os.chdir(WORKING_DIR)
