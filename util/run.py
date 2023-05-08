import subprocess
from subprocess import PIPE, STDOUT
import threading
from colorama import Fore
import os
import json


command = ['java', '-jar']
TIME_LIMIT = json.load(open('config.json', 'r'))['time_limit']


def execute_java(jar_path, stdin, timeout=TIME_LIMIT):
    cmd = command + [jar_path]
    with subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT) as proc:
        try:
            stdout, stderr = proc.communicate(stdin.encode(), timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            return 'Timeout'
    if stderr:
        print(Fore.RED)
        print(os.path.basename(jar_path)[:-4], 'Error:')
        print(stderr.decode())
        print(Fore.RESET)
    return stdout.decode().strip()


class jar_thread(threading.Thread):
    def __init__(self, name, jar, stdin, outpath=None):
        threading.Thread.__init__(self)
        self.name = name
        self.jar = jar
        self.stdin = stdin
        self.outpath = outpath

    def run(self):
        self.result = execute_java(self.jar, self.stdin).replace(
            '\r', '').replace('\n\n', '\n')
        if self.outpath:
            with open(self.outpath, 'w') as f:
                f.write(self.result)

    def get_result(self):
        return self.result

    def get_cpu_time(self):
        return self.cpu_time

    def get_name(self):
        return self.name
