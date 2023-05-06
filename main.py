from util.run import jar_thread
from util.cmp import cmp
from util.gen import gen
import logging
import logging.config
from colorama import Fore
import os
import json


config = json.load(open('config.json', 'r'))

JAR_FOLDER_PATH = config['jar_folder_path']
MODE = config['mode']
CASES = config['cases']
MAX_INPUT = config['max_input']
CLEAN = config['clean']

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
        t = jar_thread(jar, inst, path)
        tasks.append(t)
        t.start()

    for t in tasks:
        t.join()

    r = cmp(paths, i)

    if r and CLEAN and i > 0:
        for path in paths:
            os.remove(path)

    print()
    return r


if __name__ == '__main__':

    logging.config.fileConfig('logging.conf')

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
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        for jar in jars:
            if not os.path.exists(os.path.join(output_path, os.path.basename(jar)[:-4])):
                os.mkdir(os.path.join(output_path, os.path.basename(jar)[:-4]))

        for i in range(1, 1+CASES):
            if MODE == 'rand':
                inst = gen(MAX_INPUT)
                with open(os.path.join(input_path, f'{i}.txt'), 'w') as f:
                    f.write(inst)
            logging.info(f'TESTCASE #{i}')
            if check(inst, i, jars) and CLEAN:
                os.remove(os.path.join(input_path, f'{i}.txt'))

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
            check(inst, -1, jars)