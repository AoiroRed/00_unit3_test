import os
import logging
import json
from colorama import Fore


MAX_DIFF = json.load(open('config.json', 'r'))['max_diff']


def cmp(files, case=-1):
    if len(files) <= 1:
        return True
    f = []
    for file in files:
        if not os.path.exists(file):
            raise FileNotFoundError(file)
        f.append(open(file, 'r'))
    diff_cnt = 0
    line_cnt = 0
    while True:
        try:
            lines = [file.readline().rstrip(' \n\r\t') for file in f]
            line_cnt += 1
            flag = 0
            for line in lines:
                if line != lines[0]:
                    flag = -1
                    break
                if line != '':
                    flag = 1
            if flag == 0 or diff_cnt == MAX_DIFF:
                if diff_cnt == 0:
                    print(Fore.GREEN, end='')
                    logging.info('Same!')
                    print(Fore.RESET, end='')
                    return True
                elif diff_cnt == MAX_DIFF:
                    print(Fore.YELLOW, end='')
                    logging.error('Too many different lines!')
                    print(Fore.RESET, end='')
                return False
            elif flag == -1:
                diff_cnt += 1
                if diff_cnt == 1:
                    errorLogger = logging.getLogger('error')
                    errorLogger.error('-' * 30)
                    errorLogger.error(f'TESTCASE #{case}')
                print(Fore.RED, end='')
                logging.error('Different on line %d:' % line_cnt)
                print(Fore.RESET, end='')
                for i in range(len(lines)):
                    logging.error('%-8s: ' %
                                  os.path.basename(files[i])[:-4] + lines[i])
                for i in range(len(lines)).__reversed__():
                    if lines[i] == '':
                        del f[i]
                        del files[i]

        except KeyboardInterrupt:
            print('Interrupted!')
            return


if __name__ == '__main__':
    cmp(['1.txt', '2.txt', '3.txt', '4.txt', '5.txt'])
