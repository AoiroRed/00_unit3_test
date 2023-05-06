import subprocess
from subprocess import PIPE, STDOUT
import threading
from colorama import Fore

command = ['java', '-jar']


def execute_java(jar_path, stdin, timeout=5):
    cmd = command + [jar_path]
    with subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT) as proc:
        try:
            stdout, stderr = proc.communicate(stdin.encode(), timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            return 'Timeout'
    if stderr:
        print(Fore.RED)
        print(jar_path.split('/')[-1], 'Error:')
        print(stderr.decode())
        print(Fore.RESET)
    return stdout.decode().strip()


class jar_thread(threading.Thread):
    def __init__(self, jar, stdin, outpath=None):
        threading.Thread.__init__(self)
        self.jar = jar
        self.stdin = stdin
        self.outpath = outpath

    def run(self):
        self.result = execute_java(self.jar, self.stdin).replace('\r', '').replace('\n\n', '\n')
        if self.outpath:
            with open(self.outpath, 'w') as f:
                f.write(self.result)
    def get_result(self):
        return self.result
