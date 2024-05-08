import os
import logging
import variables

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(variables.LOG_FILE)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

debug = logger.debug
info = logger.info

logger.info('------------START SONOSC------------')
logger.info('cwd: %s', os.getcwd())

logger.info('COVERS_DIR: %s', variables.COVERS_DIR)
logger.info('LOG_FILE: %s', variables.LOG_FILE)
