import os
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner # solo uno perchè da modelli sound
from pm4py.algo.evaluation.replay_fitness.variants import token_replay as fitness_token_based
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.conformance import fitness_token_based_replay, precision_token_based_replay, generalization_tbr
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py import convert
import numpy as np
from sklearn.model_selection import ShuffleSplit
from argparse import ArgumentParser
from pm4py.objects.log.obj import EventLog, Trace, Event

import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import pm4py

def normalize_columns(df):
    mapping = {
        "case_id": "case:concept:name",
        "Incident ID": "case:concept:name",
        "SessionID": "case:concept:name",
        "stay_id": "case:concept:name",
        
        "URL_FILE": "concept:name",
        "activity":"concept:name",
        "IncidentActivity_Type":"concept:name",
        
        "timestamp": "time:timestamp",
        "timestamps": "time:timestamp",
        "TIMESTAMP": "time:timestamp",
        "DateStamp": "time:timestamp",
    }
    df = df.rename(columns=mapping)
    return df




def  carica_log(file_path):
    """Carica un file .xes e restituisce l'oggetto log."""

    import gc
    # log = xes_importer.apply(file_path)
    # log  = pm4py.read_xes(file_path)

    file_path_csv = file_path.replace("xes", "csv")
    
    log = None

    if os.path.exists(file_path_csv):
        print("carico da csv")


        # log = pd.read_csv(file_path_csv, sep = ";", encoding =  "latin1")
        
        encodings_to_try = ['utf-8', 'ISO-8859-1', 'cp1252', 'latin1']
        for encoding in encodings_to_try:
            try:
                print(f"Tentativo lettura con encoding='{encoding}'...")
                # engine='python' e sep=None rilevano il separatore automaticamente
                log_csv = pd.read_csv(file_path_csv, sep=None, engine='python', encoding=encoding)
                
                print(f"Successo! File letto con encoding: {encoding}")
                break  # Interrompe il ciclo se la lettura ha successo
                
            except (UnicodeDecodeError, pd.errors.ParserError):
                # Se fallisce, continua col prossimo encoding nel ciclo
                continue

        # Se dopo tutti i tentativi log_csv è ancora vuoto, solleva un errore
        if log_csv is None:
            raise ValueError(f"Impossibile leggere il file {file_path_csv}. Controlla che non sia corrotto.")
        
        
        
        
        log = log_csv
        
        # print(log.columns)
        log = normalize_columns(log)

        # Riduzione del log mantenendo solo gli attributi necessari per il calcolo delle metriche
        log = log[['case:concept:name', 'concept:name', 'time:timestamp']]

        log["time:timestamp"] = pd.to_datetime(log["time:timestamp"].apply(lambda x : x if "." in x else x + ".000"), infer_datetime_format = True )
        log[['case:concept:name', 'concept:name']] = log[['case:concept:name', 'concept:name']].astype(str)


    else:
        log = pm4py.read_xes(file_path, return_legacy_log_object=False) #Ritorna solo la tabella e non la struttura ad albero
        print(f"Tipo di oggetto caricato: {type(log)}")
        # log = pm4py.convert_to_dataframe(log)
        log = pm4py.format_dataframe(log, case_id='case:concept:name', activity_key='concept:name',
                                    timestamp_key='time:timestamp')

        # log = pd.read_csv(file_path, sep = ";", encoding =  "latin1")
        # print(log.columns)
        # log.rename(columns={'TIMESTAMP': 'time:timestamp', 'SessionID': 'case:concept:name', "URL_FILE":"concept:name"}, inplace= True)

        # Riduzione del log mantenendo solo gli attributi necessari per il calcolo delle metriche
        log = log[['case:concept:name', 'concept:name', 'time:timestamp']]

        # log["time:timestamp"] = pd.to_datetime(log["time:timestamp"].apply(lambda x : x if "." in x else x + ".000"), infer_datetime_format = True )
        # log[['case:concept:name', 'concept:name']] = log[['case:concept:name', 'concept:name']].astype(str)

    gc.collect()
    return log


def scopri_modello(log):
    """Utilizza l'Inductive Miner per ottenere Rete di Petri, Marcatura Iniziale e Finale. Così ho modelli con proprietà sound"""
    print("Modello")
    net, initial_marking, final_marking =  convert.convert_to_petri_net(inductive_miner.apply(log, variant=inductive_miner.Variants.IMd))
    return net, initial_marking, final_marking

def calcola_aderenza_e_precisione(log, net, im, fm):
    """Calcola Token-based Fitness e precision ed Escaping Edges Precision disponibili in pm4py."""
    print("fitness e precisison Token-based ")

    fitness = fitness_token_based_replay(log, net, im, fm)

    precision_escaping_edges = precision_evaluator.apply(log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    precision = precision_token_based_replay(log, net, im, fm)

    return fitness, precision, precision_escaping_edges

def calcola_generalizzazione(log, net, im, fm):
    """Calcola le metriche di generalizzazione disponibili in pm4py."""
    print("generalizzazione token based")

    gen = generalization_tbr(log, net, im, fm)
    return gen

def calcola_semplicita(net):
    """Calcola metriche di semplicità strutturale disponibili in pm4py."""
    print("simplicity")
    print("Arc degree")
    simplicity_arc_degree = simplicity_evaluator.apply(net, variant= simplicity_evaluator.Variants.SIMPLICITY_ARC_DEGREE)
    print("Extended cardoso")

    simplicity_extende_cardos= simplicity_evaluator.apply(net, variant= simplicity_evaluator.Variants.EXTENDED_CARDOSO)
    print("cyclomatic")

    simplicity_cyclomatic= simplicity_evaluator.apply(net, variant=simplicity_evaluator.Variants.EXTENDED_CYCLOMATIC)

    return [simplicity_arc_degree,simplicity_extende_cardos,simplicity_cyclomatic]



def ottimizza_tipi_dato(df):
    """Riduce l'uso della RAM convertendo stringhe in categorie."""
    for col in ['concept:name', 'case:concept:name']:
        if col in df.columns:
            df[col] = df[col].astype('category')
    return df



def k_fold_cross_validation(log, k=5):
    """Esegue il k-fold cross-validation per calcolare la generalizzazione."""

    case_ids = log['case:concept:name'].unique()
    from sklearn.model_selection import KFold
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    
    risultati = []
    for train_idx, test_idx in kf.split(case_ids):
        train_log = log[log['case:concept:name'].isin(case_ids[train_idx])]
        test_log = log[log['case:concept:name'].isin(case_ids[test_idx])]
        
        # Scoperta e calcolo fitness
        net, im, fm = scopri_modello(train_log)
        fit = pm4py.algo.evaluation.replay_fitness.algorithm.apply(
            test_log, net, im, fm, 
            variant=pm4py.algo.evaluation.replay_fitness.algorithm.Variants.TOKEN_BASED
        )
        risultati.append(fit['log_fitness'])

    return sum(risultati) / len(risultati)




def main(path_file, log_path):

    print(path_file)
    log = carica_log(path_file)
    net, im, fm = scopri_modello(log)

    # Calcolo metriche
    fit, prec, prec_escaping_edges = calcola_aderenza_e_precisione(log, net, im, fm)
    gen = calcola_generalizzazione(log, net, im, fm)
    simp = calcola_semplicita(net)
    k = 5
    gen_k_fold = k_fold_cross_validation(log, k=5) # non serve passaere il modello poichè devo calcolarlo ad ogni split

    with open(log_path, 'w') as f:
        # Output risultati
        print(f"--- RISULTATI ---")
        print(path_file)
        print(f"Fitness (Token-based): {fit}")
        print(f"Precision (Token-based): {prec}")
        print(f"Precision (ETM): {prec_escaping_edges}")
        print(f"Generalization: {gen}")
        print(f"Generalization k-fold {k}: {gen_k_fold}")
        print(f"Simplicity: \nArc Degree {simp[0]},\n Extende Cardoso {simp[1]},\nCyclomatic {simp[2]}")
        print(f"--- FINE ---")


    
if __name__ == "__main__":
    # Read the command line arguments
    print("Starting CC --->")
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="file", help="input log file")
    parser.add_argument("-d", "--dot", dest="dot", help="create dot specs", default=False, action="store_true")
    parser.add_argument("-g", "--graph", dest="graph", help="draw a graph", default=False, action="store_true")
    parser.add_argument("-p", "--prefix", dest="prefix", help="output prefix for each state", default=False, action="store_true")
    parser.add_argument("-v", "--verbose", dest="verbose", help="verbose output", default=False, action="store_true")
    parser.add_argument("-m", "--measures", dest="measures", help="calculate other complexity measures", default=[], action="append", choices=["magnitude","support","variety","level_of_detail","time_granularity","structure","affinity","trace_length","distinct_traces","deviation_from_random","lempel-ziv","pentland","all"]) #store_true
    parser.add_argument("--hide-event", dest="subg", help="hide event nodes, keep only activity types", default=True, action="store_false")
    parser.add_argument("--png", dest="png", help="draw the graph in PNG (may fail if the graph is too big", default=False, action="store_true")
    parser.add_argument("-e", "--exponential-forgetting", dest="ex_k", help="coefficient for exponential forgetting", default=1)
    parser.add_argument("-t", dest="change", help="calculate complexity growth over time", default=False,action="store_true")
    parser.add_argument("-a", "--accepting", dest="accepting", help="explicitly mark accepting states", default=False, action="store_true")
    
    args = parser.parse_args()
    main(args.file)