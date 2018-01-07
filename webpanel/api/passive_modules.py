import subprocess
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
# create a file handler
handler = logging.FileHandler('jasmine-api.log')
handler.setLevel(logging.DEBUG)
# create a logging format
formatter = logging.Formatter('%(asctime)s %(name)s.%(funcName)s.%(lineno)d: %(levelname)s %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)


def ping(target):
    command = ['ping -w 7 -c 3 -s 0 -q %s | grep "packets"' % target]
    ping_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ping_process.wait()
    return_code = ping_process.returncode
    stdout = ping_process.stdout.read().decode('utf-8').split()
    stderr = ping_process.stderr.read().decode('utf-8')

    if return_code != 0:
        logger.debug("ping %s error %s" % (target, stderr))
        return 1
    # packet loss ratio
    if stdout[5] == "0%":
        logger.debug("ping %s success" % target)
        return 0
    elif stdout[5] == "100%":
        logger.debug("ping %s fail" % target)
        return 1
    else:
        logger.debug("ping %s connection problem" % target)
        return 2
