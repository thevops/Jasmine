import socket
import platform
import signal
import requests
import json
import subprocess
import os
import sys
import time
import logging
import threading
import traceback

# ---------   LOGGING SETTINGS -------------
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('jasmine-agent.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s.%(funcName)s.%(lineno)d: %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# ------------------------------------------

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
CONFIG_FILE = "jasmine-agent.conf"
SYNCHRONIZATION_PERIOD = 0  # seconds

# ----------------------------------------

class ServerError(Exception):
    pass


class GetInformationAboutSystem:
    def __init__(self):
        pass

    def get_top_10_process(self, option):
        # option = 'mem' or 'cpu'
        command = ['ps -ax -o pid,user:20,%mem,%cpu,etime,cmd --sort=-%' + option + ' --no-headers| tr -s " " | head -10']
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        stdout = proc.stdout.read().decode('utf-8').split("\n")[:-1]  # from 0 to one before last, because of split

        result = {} # dict for results
        for i, row in enumerate(stdout):
            row = row.split() # split row by spaces
            result[i] = {"pid": row[0], "user": row[1], "mem": row[2], "cpu": row[3], "etime": row[4], "cmd": row[5]}
        return {"top_10_" + option: result}

    def get_uptime(self):
        proc = subprocess.Popen(['uptime | tr -s " "'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        stdout = proc.stdout.read().decode('utf-8').split("\n")[0].split()
        return {"uptime": ' '.join(stdout)}

    def get_ifconfig(self):
        proc = subprocess.Popen(['ifconfig -a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        stdout = proc.stdout.read()[:-2].decode('utf-8')  # [:-2] remove last newline = '\n'
        return {"ifconfig": stdout}

    def get_disk_size(self):
        proc = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        proc.wait()
        stdout = proc.stdout.read()[:-2].decode('utf-8')  # [:-2] remove last newline = '\n'
        return {"disk_size": stdout}

    def get_disk_model(self):
        command = ["lshw -short -C disk -quiet | grep 'disk' | tr -s ' ' | cut -d' ' -f2-"]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        stdout = proc.stdout.read()[:-2].decode('utf-8')  # [:-2] remove last newline = '\n'
        return {"disk_model": stdout}

    def get_meminfo(self):
        command = ["cat /proc/meminfo | grep 'Mem' | tr -s ' '"]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        stdout = proc.stdout.read()[:-2].decode('utf-8').split("\n")  # [:-2] remove last newline = '\n'

        result = dict()
        # divide to MB
        result["MemTotal"] = round(int(stdout[0].split()[1])/1024,2)
        result["MemFree"] = round(int(stdout[1].split()[1])/1024,2)
        result["MemAvailable"] = round(int(stdout[2].split()[1])/1024,2)

        return {"ram": result}

    def get_cpu_info(self):
        proc = subprocess.Popen(["cat /proc/cpuinfo"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        stdout = proc.stdout.read().decode('utf-8').split("\n")

        result = dict()
        # ---- CPU model ----
        processor_model = set()
        # ---- CPU cores number ----
        cores_number = 0
        # ---- CPU processors
        processors_number = 0
        tmp_processors_number = set()

        for line in stdout:
            if 'model name' in line:
                line = line.replace("\t", "").split()
                line = line[2:]
                processor_model.add(' '.join(line))
                continue
            if 'processor' in line:
                cores_number+=1
                continue
            if 'core id' in line:
                tmp_processors_number.add(line)
                continue

        processors_number = len(tmp_processors_number)

        result = {"model": list(processor_model), "cores": cores_number, "processors": processors_number}

        return {"cpu": result}

    def get_uname(self):
        proc = subprocess.Popen(['uname -a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        stdout = proc.stdout.read()[:-1].decode('utf-8')  # [:-2] remove last newline = '\n'
        return {"uname": stdout}

    def create_report(self, *args):
        data = {}
        for arg in args:
            data.update(arg)

        data_tmp = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
        return data_tmp

class Modules:
    def __init__(self):
        self.task = None
        self.module = None

    def run(self, task, module):
        self.task = task
        self.module = module

        module_name = self.module['name']

        if module_name == "Johny the Ripper Cracker":
            logger.debug("start task:%s module:%s" % (self.task['name'], module_name))
            return self.johny_the_ripper_cracker()
        elif module_name == "Reload configurations":
            return self.get_configurations()
        elif module_name == "Full report":
            return self.full_report()
        elif module_name == "Autoupdate":
            return self.autoupdate()
        elif module_name == "Run command":
            return self.run_command()
        else:
            status = "failed"
            results = "module not found"
            return status, results

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
        proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False).wait()

        # download hash file
        hash_url = configuration['hash_url']
        hash_filename = "hash.txt"
        command = ['wget', hash_url, '-O', hash_filename]
        proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False).wait()

        # extract lines
        try:
            parameters = json.loads(self.task['parameters'])
            local_id = parameters['local_id']
            number_of_workers = parameters['number_of_workers']
        except Exception as e:
            logger.critical("Error in json loads")
            return None

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
        proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True).wait()

        # run john
        command = ['john', hash_filename, '-w=%s' % part_dict_filename]
        proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False).wait()

        # get john results
        command = ['john', hash_filename, '--show']
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        proc.wait()
        stdout = proc.stdout.read().decode('utf-8')

        # clean
        subprocess.Popen(['rm', '%s' % dict_filename], shell=False).wait()
        subprocess.Popen(['rm', '%s' % part_dict_filename], shell=False).wait()
        subprocess.Popen(['rm', '%s' % hash_filename], shell=False).wait()

        # results
        results = os.linesep.join([s for s in stdout.splitlines() if s])
        if len(results.split("\n")) > 1:
            status = "victorious"
        elif len(results.split("\n")) == 1:
            status = "completed"
        else:
            status = "failed"

        logger.info("task:%s %s ->\n%s" % (self.task['name'], status, results))
        return status, results

    def get_configurations(self):
        global SYNCHRONIZATION_PERIOD
        url = API_URL + '/host/get_configurations/'
        data = {"token": TOKEN}
        try:
            r = requests.post(url, data=data)
            if r.status_code != 200:
                logger.critical("request status_code %s" % r.status_code)
                raise ServerError
        except Exception:
            raise ServerError

        tmp = r.json()  # dict
        SYNCHRONIZATION_PERIOD = tmp['synchronization_period'] * 60  # to seconds
        status = "completed"
        results = "ok"
        return status, results

    def full_report(self):
        GetInfo = GetInformationAboutSystem()
        top_proc_cpu = GetInfo.get_top_10_process('cpu')
        top_proc_mem = GetInfo.get_top_10_process('mem')
        uptime = GetInfo.get_uptime()
        ifconfig = GetInfo.get_ifconfig()
        disk_size = GetInfo.get_disk_size()
        disk_model = GetInfo.get_disk_model()
        mem_info = GetInfo.get_meminfo()
        cpu_info = GetInfo.get_cpu_info()
        uname = GetInfo.get_uname()

        results = GetInfo.create_report(top_proc_cpu, top_proc_mem, uptime, ifconfig, disk_size, disk_model,
            mem_info, cpu_info, uname, {"hostname": HOSTNAME}, {"python_version": PYTHON_VERSION},
            {"python_compiler": PYTHON_COMPILER}, {"linux_distribution": LINUX_DISTRIBUTION})

        status = "completed"
        return status, results

    def autoupdate(self):
        """
        module.configurations
        {
            "agent_url": "",
        }
        """
        configuration = json.loads(self.module['configuration'])
        agent_url = configuration['agent_url']
        command = ['bash autoupdate.sh %s' % agent_url]
        proc = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        resutls = "ok"
        status = "completed"
        return status, results

    def run_command(self):
        """
        module.configurations
        {
            "command": "",
        }
        """
        configuration = json.loads(self.module['configuration'])
        command = [configuration['command']]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        resutls = proc.stdout.read()[:-1].decode('utf-8')  # [:-2] remove last newline = '\n'
        status = "completed"
        return status, results


# ----------------------   PERIODIC REPORT    -----------------------------
def periodic_report(stop_event):
    while not stop_event.isSet():
        url = API_URL + '/host/periodic_report/'
        data = {"token": TOKEN}
        try:
            r = requests.post(url, data=data)
            if r.status_code != 200:
                logger.critical("request status_code %s" % r.status_code)
                raise ServerError
        except Exception:
            raise ServerError
        # check stop_event flag every 2 second
        for i in range(1, SYNCHRONIZATION_PERIOD, 2):
            time.sleep(2)
            if stop_event.isSet():
                return

# -------------------------------------------------------------------------

def set_results(task_id, status, results):
    url = API_URL + '/task/' + str(task_id) + '/result/'
    data = {"token": TOKEN, "status": status, "results": results}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            logger.critical("request status_code %s" % r.status_code)
            raise ServerError
    except Exception:
        raise ServerError

def get_task():
    # get all tasks
    url = API_URL + '/task/list/'
    data = {"token": TOKEN}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            logger.critical("request status_code %s" % r.status_code)
            raise ServerError
    except Exception:
        raise ServerError

    all_tasks = r.json()
    if len(all_tasks) <= 0:
        # there are no tasks
        return None

    # sort task by timestamp
    sorted_tasks = sorted(all_tasks, key=lambda x: x['timestamp'])

    # get first task
    url = API_URL + '/task/' + str(sorted_tasks[0]['id']) + '/'
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            logger.critical("request status_code %s" % r.status_code)
            raise ServerError
    except Exception:
        raise ServerError

    selected_task = r.json()

    return selected_task

def get_module(task):
    url = API_URL + '/module/' + str(task['module']) + '/'
    data = {"token": TOKEN}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            logger.critical("request status_code %s" % r.status_code)
            raise ServerError
    except Exception:
        raise ServerError

    module = r.json()
    if len(module) <= 0:
        logger.critical("task:%s module:%s not found" % (task['name'], task['module']))
        return None

    return module

def load_configuration():
    global SERVER_IP, SERVER_PORT, API_URL, TOKEN
    try:
        data = json.load(open(CONFIG_FILE))
    except Exception as e:
        return

    SERVER_IP = data['server ip']
    SERVER_PORT = data['server port']
    API_URL = HTTP + SERVER_IP + ":" + SERVER_PORT + data['api']
    TOKEN = data['token']

def sigterm_handler(signum, frame):
    # for systemd stop
    stop_event.set()
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    try:
        load_configuration()
        modules_worker = Modules()
        modules_worker.get_configurations()
    except Exception as e:
        logger.critical("Server not responding from: %s:%s" % (SERVER_IP, SERVER_PORT))
        exit()

    # run periodic report
    stop_event = threading.Event()
    thr1 = threading.Thread(target=periodic_report, args=(stop_event,))
    thr1.start()

    # -----------------    MAIN LOOP    -----------------------
    try:
        while True:
            print(" ", time.asctime(time.localtime(time.time())))
            task = get_task()
            if task:
                module = get_module(task)
                if module:
                    status, results = modules_worker.run(task, module)
                    set_results(task['id'], status, results)

            for i in range(1, SYNCHRONIZATION_PERIOD):
                time.sleep(1)
                sys.stdout.write("\r%s z %s" % (i, SYNCHRONIZATION_PERIOD))
    except KeyboardInterrupt:
        print("\nControl+C")
    except ServerError:
        logger.critical("ServerError - exit")
    except Exception as e:
        #print(e)
        traceback.print_exc()
    finally:
        stop_event.set()
        exit()


