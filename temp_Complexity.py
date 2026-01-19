import gc

import psutil
from Complexity import *
import os
from pathlib import Path


def wait_for_memory(threshold=0.5, check_interval=5): 
    """ Attende finché la RAM libera non supera la soglia indicata. threshold = 0.5 significa 50% di RAM libera. """ 
    time.sleep(check_interval * 2)  # Attesa iniziale per evitare controlli troppo frequenti
    while True: 
        mem = psutil.virtual_memory()
        free_ratio = mem.available / mem.total 
        if free_ratio >= threshold: 
            print(f"RAM libera sufficiente ({free_ratio:.2%}). Procedo.") 
            return 
        else: 
            print(f"RAM libera insufficiente ({free_ratio:.2%}). Aspetto {check_interval}s...")
            time.sleep(check_interval)

def trova_riga_total(file_path):
    riga_trovata = None
    
    # Usiamo utf-8-sig per massima compatibilità e errors='replace' per evitare crash
    with open(file_path, "r", encoding="utf-8-sig", errors="replace") as f:
        for riga in f:
            # .strip() rimuove spazi e a capo bianchi
            if "Total:" in riga:
                riga_trovata = True
                # Se ti serve solo il PRIMO "Total:", aggiungi 'break' qui
                # Se ti serve l'ULTIMO (comune nei log), non mettere il break
    
    return riga_trovata

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
     root_main = Path()
     scripts = list(r_d.rglob("*.xes"))
     logs = list(root_main.rglob("log_*.txt"))
     scripts.sort()
     for elem in scripts:
          for log in logs:
               if elem.stem in log.stem:
                    print(elem)
                    # # Verifica se l'ultima riga contiene "Total:"
                    # # last_line = None
                    # # with open(log, "r") as f:
                    # #      last_line = f.read().split("\n")[-2]
                    # # Sostituisci la tua apertura file con questa:
                    # # with open(log, "r", encoding="utf-8-sig", errors="replace") as f:
                    # #      linee = f.readlines()
                    # #      if len(linee) >= 2:
                    # #           last_line = linee[-2]
                    # # Verifica se l'ultima riga contiene "Total:" Vuol dire che non serve rifare i calcoli
                    if trova_riga_total(log):
                         print(elem , "Ended")
                    else:
                         times = {}
                         measure_times = {}
                         wait_for_memory(0.5, check_interval=10)
                         # Read and prepare event log
                         # Da qui in poi, tutto ciò che stampi va sia in console che nel file
                         sys.stdout = Tee(log)
                         
                         print("Reading and preparing event log", elem)
                         base_filename = extract_base_filename(str(elem))
                         pm4py_log = generate_pm4py_log(str(elem), verbose=False)
                         
                         gc.collect()
                         # This log is a list of lists of Event objects defined here
                         log = generate_log(pm4py_log, verbose=False)
                         gc.collect()
                         pa = build_graph(log, verbose=False, accepting=False)
                         
                         if(False):
                              print("DOT specification:")
                              print(pa.draw(args.subg))
                         
                         if(False):
                              draw_graph(pa, base_filename, args.subg, args.png, args.accepting)
                         if("all"):
                              print("Starting performing measurements", elem)
                              measurements = perform_measurements(["all"], log, pm4py_log, pa, quiet=False, verbose=False)
                         
                         print("---Entropy measures---")
                         var_ent = graph_complexity(pa)
                         print("Variant entropy: "+str(var_ent[0]))
                         print("Normalized variant entropy: "+str(var_ent[1]))
                         
                         seq_ent = log_complexity(pa)
                         print("Sequence entropy: "+str(seq_ent[0]))
                         print("Normalized equence entropy: "+str(seq_ent[1]))
                         
                         seq_ent_lin = log_complexity(pa, "linear")
                         print("Sequence entropy with linear forgetting: "+str(seq_ent_lin[0]))
                         print("Normalized sequence entropy with linear forgetting: "+str(seq_ent_lin[1]))
                         
                         seq_ent_exp = log_complexity(pa, "exp",float(1))
                         print("Sequence entropy with exponential forgetting (k="+str(1)+"): "+str(seq_ent_exp[0]))
                         print("Normalized sequence entropy with exponential forgetting (k="+str(1)+"): "+str(seq_ent_exp[1]))
                         
                         # Change over time

                         if(False):
                              def show(df): # For backward compatibility
                                   cols = [col for col in df.columns if col != "Date"]
                                   for i in range(len(df)):
                                        dt = df["Date"][i]
                                        print(str(calendar.month_name[dt.month])+" "+str(dt.year))
                                        for col in cols:
                                             print(col+": "+str(df[col][i]))
                         
                              variant_entropy_change = calculate_variant_entropy(pa,log[0].timestamp,log[-1].timestamp, figure=True, base_filename=base_filename, verbose=args.verbose)
                              show(variant_entropy_change)
                              sequence_entropy_change = calculate_sequence_entropy(pa,log[0].timestamp,log[-1].timestamp, figure=True, base_filename=base_filename, verbose=args.verbose)
                              show(sequence_entropy_change)
                              sequence_entropy_change_linear = calculate_sequence_entropy(pa,log[0].timestamp,log[-1].timestamp, forgetting="linear", figure=True, base_filename=base_filename, verbose=args.verbose)
                              show(sequence_entropy_change_linear)
                              sequence_entropy_change_exponential = calculate_sequence_entropy(pa,log[0].timestamp,log[-1].timestamp, forgetting="exp", k=float(args.ex_k), figure=True, base_filename=base_filename, verbose=args.verbose)
                              show(sequence_entropy_change_exponential)
                         
                         # Show prefixes of each state
                         if(False):
                              print("Prefixes:")
                              for node in pa.nodes:
                                   if node != pa.root:
                                        print ("s"+"^"+str(node.c)+"_"+str(node.j) + ":" + node.getPrefix())
                         
                         #TODO:
                         #Text wrap for event nodes
                         #Automatically set font size
                         # Add args.verbose to all addNode calls

                         

                         # count time
                         s = time.perf_counter()
                         times['Defining predecessors'] = time.perf_counter()-s
                         times["Building prefix automaton"] = time.perf_counter()-s
                         times["Drawing the graph"] = time.perf_counter()-s
                         times["Calculating log complexity measures"] = time.perf_counter()-s
                         times["Calculating variant entropy"] = time.perf_counter()-s
                         times["Calculating sequence entropy"] = time.perf_counter()-s
                         times["Calculating sequence entropy with linear forgetting"] = time.perf_counter()-s
                         times["Calculating sequence entropy with exponential forgetting"] = time.perf_counter()-s
                         
                         print("Time measurements:")
                         for k,v in times.items():
                              if(k=="Calculating log complexity measures"):
                                   for p,m in measure_times.items():
                                        if p not in ["event_classes", "hashmap", "var"]:
                                             print(p+": "+str(m)+" seconds")
                              print(k+": "+str(v)+" seconds")
                         print("Total: "+str(sum(times.values())))
