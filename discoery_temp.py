# import pandas as pd


# df = pd.read_csv("event_log_covid.csv")

# df["concept:name"] = df["activity"].apply(lambda x: "_".join(x.split("_")[0:-1]) if not x in ["ICU_TRANSFER", "ER_ADMISSION", "VITAL_MEASUREMENT"] else x)
# df["concept:attribute"] = df["activity"].apply(lambda x: x.split("_")[-1] if not x in ["ICU_TRANSFER", "ER_ADMISSION", "VITAL_MEASUREMENT"] else "")

# df = df.rename(columns={
#     "case_id": "case:concept:name",
#     "activity": "concept:name",
#     "timestamp": "time:timestamp"
# })

# df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], format="%Y-%m-%d %H:%M:%S", errors='coerce')
# df["case:concept:name"] = df["case:concept:name"].astype(str)
# df["concept:name"] = df["concept:name"].astype(str)

# df.to_csv("simpler_event_log_covid.csv")

# import pandas as pd
# import pm4py

# df = pd.read_csv("event_log_covid.csv")

# df = df.rename(columns={
#     "case_id": "case:concept:name",
#     "activity": "concept:name",
#     "timestamp": "time:timestamp"
# })

# df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], format="%Y-%m-%d %H:%M:%S", errors='coerce')
# df["case:concept:name"] = df["case:concept:name"].astype(str)
# df["concept:name"] = df["concept:name"].astype(str)

# petri_net, initial_marking, final_marking = pm4py.algo.discovery.heuristics.algorithm.apply(df)

# pm4py.visualization.petri_net.visualizer.apply(petri_net, initial_marking, final_marking).render("petri_net_completa",cleanup=True, format="svg")


import pandas as pd
import pm4py

import os
import pickle
from concurrent.futures import ThreadPoolExecutor




print("Carico Log")
df_orig = pd.read_csv("event_log_covid.csv")
df_orig = df_orig.rename(columns={
    "case_id": "case:concept:name",
    "activity": "concept:name",
    "timestamp": "time:timestamp"
})
print("Conversioni necessarie")
df_orig["time:timestamp"] = pd.to_datetime(df_orig["time:timestamp"], format="%Y-%m-%d %H:%M:%S", errors='coerce')
df_orig["case:concept:name"] = df_orig["case:concept:name"].astype(str)
df_orig["concept:name"] = df_orig["concept:name"].astype(str)

df_simpl = pd.read_csv("simpler_event_log_covid.csv")
df_simpl["time:timestamp"] = pd.to_datetime(df_simpl["time:timestamp"], format="%Y-%m-%d %H:%M:%S", errors='coerce')
df_simpl["case:concept:name"] = df_simpl["case:concept:name"].astype(str)
df_simpl["concept:name"] = df_simpl["concept:name"].astype(str)

print("Start Discovery")
# petri_nets = {
#     "inductive_orig": pm4py.discover_petri_net_inductive(df_orig),
#     "inductive_simpl": pm4py.discover_petri_net_inductive(df_simpl),

#     "heuristics_orig": pm4py.discover_petri_net_heuristics(df_orig),
#     "heuristics_simpl": pm4py.discover_petri_net_heuristics(df_simpl),

#     "alpha_orig": pm4py.discover_petri_net_alpha(df_orig),
#     "alpha_simpl": pm4py.discover_petri_net_alpha(df_simpl),

#     "alpha_plus_orig": pm4py.discover_petri_net_alpha_plus(df_orig),
#     "alpha_plus_simpl": pm4py.discover_petri_net_alpha_plus(df_simpl),

#     "ilp_orig": pm4py.discover_petri_net_ilp(df_orig),
#     "ilp_simpl": pm4py.discover_petri_net_ilp(df_simpl)
# }


output_dir = "discovery"
os.makedirs(output_dir, exist_ok=True)

def discover_and_save_petri_net(method_name, log_data, log_type):
    """
    Function to discover a Petri net using a specified method and save it.
    """
    print(f"Discovering {method_name} for {log_type}...")
    try:
        if method_name == "inductive":
            net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log_data)
        elif method_name == "heuristics":
            net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(log_data)
        elif method_name == "alpha":
            net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log_data)
        elif method_name == "alpha_plus":
            net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(log_data)
        elif method_name == "ilp":
            net, initial_marking, final_marking = pm4py.discover_petri_net_ilp(log_data)
        else:
            raise ValueError(f"Unknown discovery method: {method_name}")

        file_name = f"{method_name}_{log_type}.pkl"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, 'wb') as f:
            pickle.dump((net, initial_marking, final_marking), f)
        print(f"Successfully discovered and saved {method_name} for {log_type} to {file_path}")
        return {f"{method_name}_{log_type}": (net, initial_marking, final_marking)}
    except Exception as e:
        print(f"Error discovering {method_name} for {log_type}: {e}")
        return {f"{method_name}_{log_type}": None}


# Define the tasks for the thread pool
tasks = []
discovery_methods = ["inductive", "heuristics", "alpha", "alpha_plus", "ilp"]

for method in discovery_methods:
    tasks.append((method, df_orig, "orig"))
    tasks.append((method, df_simpl, "simpl"))

petri_nets = {}

# Use ThreadPoolExecutor for concurrent execution
# You can adjust max_workers based on your system's capabilities
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    # Submit tasks to the executor
    futures = [executor.submit(discover_and_save_petri_net, method, log_data, log_type) for method, log_data, log_type in tasks]

    # Collect results as they complete
    for future in futures:
        result = future.result()
        if result:
            petri_nets.update(result)

print("\nAll Petri net discoveries attempted.")





count = 1
metrics_data = []
for name, (net, initial_marking, final_marking) in petri_nets.items():
    print(f"\n--- Elaborazione della Petri Net: {name} {count}/10---")

    # Determina il log da utilizzare per il calcolo delle metriche
    # In base al nome della chiave, usiamo df_orig o df_simpl
    if "_orig" in name:
        log = df_orig
    elif "_simpl" in name:
        log = df_simpl
    else:
        print(f"ATTENZIONE: Impossibile determinare il log per {name}. Le metriche non verranno calcolate.")
        log = None

    if log is not None:
        # 1. Stampa il SVG della Petri Net
        gviz = pm4py.view_petri_net(net, initial_marking, final_marking)
        output_file_path = f"{name}.svg"
        pm4py.save_vis_petri_net(net, initial_marking, final_marking,output_file_path)
  
        print(f"SVG salvato come: {output_file_path}")

        # 2. Calcola e stampa la Fitness
        # pm4py.evaluate_replay_fitness è un wrapper per fitness_evaluator.apply
        fitness_results = pm4py.fitness_alignments(log, net, initial_marking, final_marking, multi_processing= True)
        print(f"Fitness: {fitness_results['log_fitness']:.4f}")

        # 3. Calcola e stampa la Precisione
        # pm4py.evaluate_precision è un wrapper per precision_evaluator.apply
        precision = pm4py.precision_alignments(log, net, initial_marking, final_marking,  multi_processing= True)
        print(f"Precision: {precision:.4f}")

        
        metrics_data.append({
                    "PetriNet_Name": name,
                    "Fitness": fitness_results,
                    "Precision": precision
                })

    else:
        print(f"Skipping metrics for {name} due to missing log.")
    count +=1
metrics_df = pd.DataFrame(metrics_data)
print("\n--- Riepilogo delle Metriche ---")
print(metrics_df)
output_csv_path = "petrinet_metrics_summary.csv"
metrics_df.to_csv(output_csv_path, index=False)
print(f"\nMetriche salvate in: {output_csv_path}")

