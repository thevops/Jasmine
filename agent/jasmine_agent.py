import socket
import platform
import signal
import requests
import json
import dateutil.parser  # pip install python-dateutil
import subprocess
import os

# -------- SERVER GLOBAL VARIABLES -------
HTTP = "http://"
SERVER_IP = ""
SERVER_PORT = ""
API_URL = ""
TOKEN = ""

# ----------------------------------------
# -------- HOST GLOBAL VARIABLES ---------
HOSTNAME = socket.gethostname()
PYTHON_VERSION = platform.python_version()
PYTHON_COMPILER = platform.python_compiler()
LINUX_DISTRIBUTION = ' '.join(platform.linux_distribution())

# ----------------------------------------
# ------------ CONFIGURATION -------------
CONFIG_FILE = "jasmine.conf"
COMMUNICATION_INTERVAL = ""

# ----------------------------------------


class Modules:
    def __init__(self):
        pass

    def run(self, task, module):
        self.task = task
        self.module = module

        module_name = self.module['name']

        if module_name == "Johny the Ripper Cracker":
            return self.johny_the_ripper_cracker()
        elif module_name == "costam":
            pass
        else:
            pass

    def johny_the_ripper_cracker(self):
        """
        module.configurations
        {
            "dict_url": "",
            "hash_url": "",
        }
        task.parameters
        {
            "local_id": "",
            "number_of_workers": ""
        }
        """
        # download password dictionary
        configuration = json.loads(self.module['configuration'])
        dict_url = configuration['dict_url']
        dict_filename = "dict.txt"
        command = ['wget', dict_url, '-O', dict_filename]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        proc.wait()
        return_code = proc.returncode
        stdout = proc.stdout.read().decode('utf-8')
        stderr = proc.stderr.read().decode('utf-8')

        #print("Return code %s" % return_code)
        #print("Output:\n %s " % stdout)
        #print("Error\n %s " % stderr)
        #print("PID: %s" % proc.pid)

        # download hash file
        hash_url = configuration['hash_url']
        hash_filename = "hash.txt"
        command = ['wget', hash_url, '-O', hash_filename]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        proc.wait()
        return_code = proc.returncode
        stdout = proc.stdout.read().decode('utf-8')
        stderr = proc.stderr.read().decode('utf-8')

        #print("Return code %s" % return_code)
        #print("Output:\n %s " % stdout)
        #print("Error\n %s " % stderr)
        #print("PID: %s" % proc.pid)

        # extract lines
        try:
            parameters = json.loads(self.task['parameters'])
            local_id = parameters['local_id']
            number_of_workers = parameters['number_of_workers']
        except Exception as e:
            print(e)
            return -1
        
        # count number of file lines
        num_of_lines = sum(1 for line in open(dict_filename, errors='replace'))

        my_part = round(num_of_lines / number_of_workers)
        if local_id+1 == number_of_workers:  # if parts are not equal, the last has to be a little more lines
            tmp = num_of_lines - (my_part * number_of_workers)
            my_part += tmp

        start = (local_id * my_part) + 1
        stop = start + my_part - 1
        part_dict_filename = "part_dict.txt"
        command = ['sed -n %d,%dp %s > %s' % (start, stop, dict_filename, part_dict_filename)]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        return_code = proc.returncode
        stdout = proc.stdout.read().decode('utf-8')
        stderr = proc.stderr.read().decode('utf-8')

        #print("Return code %s" % return_code)
        #print("Output:\n %s " % stdout)
        #print("Error\n %s " % stderr)
        #print("PID: %s" % proc.pid)

        # run john
        command = ['john', hash_filename, '-w=%s' % part_dict_filename]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        proc.wait()
        return_code = proc.returncode
        stdout = proc.stdout.read().decode('utf-8')
        stderr = proc.stderr.read().decode('utf-8')

        #print("Return code %s" % return_code)
        #print("Output:\n %s " % stdout)
        #print("Error\n %s " % stderr)
        #print("PID: %s" % proc.pid)

        # get john results
        command = ['john', hash_filename, '--show']
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        proc.wait()
        return_code = proc.returncode
        stdout = proc.stdout.read().decode('utf-8')
        stderr = proc.stderr.read().decode('utf-8')

        #print("Return code %s" % return_code)
        #print("Output:\n %s " % stdout)
        #print("Error\n %s " % stderr)
        #print("PID: %s" % proc.pid)

        # clean
        os.system('rm %s' % dict_filename)
        os.system('rm %s' % part_dict_filename)
        os.system('rm %s' % hash_filename)

        # results
        results = os.linesep.join([s for s in stdout.splitlines() if s])
        if len(results.split("\n")) > 1:
            status = "victorious"
        elif len(results.split("\n")) == 1:
            status = "completed"
        else:
            status = "failed"

        return status, results


def set_results(task_id, status, results):
    url = API_URL + '/task/' + str(task_id) + '/result/'
    data = {"token": TOKEN, "status": status, "results": results}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print("server nie dziala?")
            return None
    except Exception as e:
        print("cant connect to server")

    response = r.json()
    print(r)

def get_task():
    # get all tasks
    url = API_URL + '/task/list/'
    data = {"token": TOKEN}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print("server nie dziala?")
            return None
    except Exception as e:
        print("cant connect to server")

    all_tasks = r.json()
    if len(all_tasks) <= 0:
        print("nie ma zadan")
        return None

    # sort task by timestamp
    sorted_tasks = sorted(all_tasks, key=lambda x: x['timestamp'])
    
    # get first task
    url = API_URL + '/task/' + str(sorted_tasks[0]['id']) + '/'
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print("server nie dziala?")
            return None
    except Exception as e:
        print("cant connect to server")

    selected_task = r.json()

    return selected_task

def get_module(task):
    url = API_URL + '/module/' + str(task['module']) + '/'
    data = {"token": TOKEN}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print("server nie dziala?")
            return None
    except Exception as e:
        print("cant connect to server")

    module = r.json()
    if len(module) <= 0:
        print("nie ma modulow")
        return None

    return module


def load_configuration():
    global SERVER_IP, SERVER_PORT, API_URL, TOKEN
    try:
        data = json.load(open(CONFIG_FILE))
    except Exception as e:
        print(e)
        exit()

    SERVER_IP = data['server ip']
    SERVER_PORT = data['server port']
    API_URL = HTTP + SERVER_IP + ":" + SERVER_PORT + data['api']
    TOKEN = data['token']

def sigterm_handler(signum, frame):
    # for systemd stop
    raise Exception


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    load_configuration()

    t = get_task()
    m = get_module(t)

    mod = Modules()
    status, results = mod.run(t,m)
    q = set_results(t['id'], status, results)
