from util.run import jar_thread
from util.cmp import cmp
from util.gen import gen
import logging
import logging.config
from colorama import Fore
import os
import json
import time


config = json.load(open('config.json', 'r'))

JAR_FOLDER_PATH = config['jar_folder_path']
MODE = config['mode']
CASES = config['cases']
CLEAN = config['clean']
CPU_TIME = config['cpu_time']
STOP = config['stop']

input_path = os.path.join('data', 'input')
output_path = os.path.join('data', 'output')


def check(inst, i, jars):
    paths = []
    tasks = []
    for jar in jars:
        name = os.path.basename(jar)[:-4]
        path = os.path.join(output_path, name, f'{name}_{i}.txt') if i > 0 else os.path.join(
            'output', os.path.basename(jar)[:-4] + '_out.txt')
        paths.append(path)
        t = jar_thread(name, jar, inst, path)
        tasks.append(t)
        t.start()

    for t in tasks:
        t.join()

    r = cmp(paths, i, inst.splitlines())

    # if CPU_TIME:
    #     for t in tasks:
    #         print(Fore.GREEN, end='')
    #         print(f'{t.get_name()} CPU Time:', end=' ')
    #         print(Fore.RESET, end='')
    #         print(f'{t.get_cpu_time()}s')

    if r and CLEAN and i > 0:
        for path in paths:
            os.remove(path)

    print()
    return r


if __name__ == '__main__':

    logging.config.fileConfig('logging.conf')

    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    print(Fore.GREEN, end='')
    print(f'[{t}]', end=' ')
    print(Fore.RESET, end='')
    print('Start testing...')
    
    log_path = os.path.join('log', 'err_data', t)
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    handler = logging.FileHandler(os.path.join(log_path, 'error.log'), encoding='utf-8')
    handler.setLevel(logging.ERROR)
    logging.getLogger('error').addHandler(handler)
    logging.getLogger().addHandler(handler)

    if not os.path.exists(JAR_FOLDER_PATH):
        print(Fore.RED, end='')
        logging.info('No jar folder!')
        print(Fore.RESET)
        exit(0)

    jars = []
    for file in os.listdir(JAR_FOLDER_PATH):
        if file.endswith('.jar'):
            jars.append(os.path.join(JAR_FOLDER_PATH, file))

    if MODE == 'rand' or MODE == 'retest':
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists(input_path):
            os.mkdir(input_path)
        elif CLEAN:
            for file in os.listdir(input_path):
                os.remove(os.path.join(input_path, file))
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        for jar in jars:
            if not os.path.exists(os.path.join(output_path, os.path.basename(jar)[:-4])):
                os.mkdir(os.path.join(output_path, os.path.basename(jar)[:-4]))

        for i in range(1, 1+CASES):
            if MODE == 'rand':
                inst = gen()
                if not CLEAN:
                    with open(os.path.join(input_path, f'{i}.txt'), 'w') as f:
                        f.write(inst)
            else:
                with open(os.path.join(input_path, f'{i}.txt'), 'r') as f:
                    inst = f.read()
            logging.info(f'TESTCASE #{i}')
            if not check(inst, i, jars):
                with open(os.path.join(log_path, f'{i}.txt'), 'w') as f:
                    f.write(inst)
                if CLEAN:
                    with open(os.path.join(input_path, f'{i}.txt'), 'w') as f:
                        f.write(inst)
                if STOP == 'first':
                    print(Fore.RED, end='')
                    logging.info(f'Failed at #{i}!')
                    print(Fore.RESET)
                    exit(0)

    elif MODE == 'input':
        input_file = 'input.txt'
        if not os.path.exists(input_file):
            input_file = input('Input file name: ')
            if not os.path.exists(input_file):
                print(Fore.RED, end='')
                logging.info('No input file!')
                print(Fore.RESET)
                exit(0)
        if not os.path.exists('output'):
            os.mkdir('output')
        with open(input_file, 'r') as f:
            inst = f.read()
            if not check(inst, -1, jars):
                with open(os.path.join(log_path, f'input.txt'), 'w') as f:
                    f.write(inst)
