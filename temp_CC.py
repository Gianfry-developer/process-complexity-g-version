from cmath import log
import gc
import CC
import os
from pathlib import Path
from temp_Complexity import wait_for_memory

import sys
# Increase the limit to 5000 or 10000
sys.setrecursionlimit(20000)

import sys

class Tee(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # Necessario per la compatibilità con alcuni sistemi e per forzare la scrittura
        self.terminal.flush()
        self.log.flush()



if __name__ == "__main__":
     r_d = Path("datasets")
     scripts = list(r_d.rglob("*.xes"))
     scripts.sort()
     for elem in scripts:
            print(elem, "CC")
            # wait_for_memory(0.6, check_interval=10)
            log_path = "cc_log_" + os.path.basename(elem) + ".txt"

            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if any(["FINE" in line for line in lines]):
                        print(f"Skipping {elem} as it is already processed.")
                        continue


            sys.stdout = Tee(log_path)
            CC.main(str(elem), log_path)
            sys.stdout.log.close()
            sys.stdout = sys.__stdout__
            gc.collect()
            print("Finished", elem)