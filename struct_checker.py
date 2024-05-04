import os

cur_dir = os.curdir + '/'

def check_paths(paths = []):
    for path in paths:
        dir = cur_dir + path
        if not os.path.exists(dir):
            os.mkdir(dir)
            print('[*] Creating directory:  ' + dir)

