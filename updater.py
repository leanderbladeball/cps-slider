import sys
import os
import time
import shutil
import subprocess

def run():
    new_file = sys.argv[1]
    old_file = sys.argv[2]

    time.sleep(1)

    try:
        os.remove(old_file)
    except:
        pass

    shutil.move(new_file, old_file)

    subprocess.Popen([old_file, "--updated"])


if __name__ == "__main__":
    run()
    