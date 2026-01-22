import os
import gc
import pandas as pd
from argparse import ArgumentParser
from sklearn.model_selection import KFold

import pm4py
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py.conformance import (
    fitness_token_based_replay,
    precision_token_based_replay,
    generalization_tbr
)
from pm4py import convert

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




def _load_csv(file_path):
    """Carica CSV con rilevamento automatico encoding."""
    encodings = ['utf-8', 'ISO-8859-1', 'cp1252', 'latin1']
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, sep=None, engine='python', encoding=encoding)
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    raise ValueError(f"Impossibile leggere il file {file_path}. Controlla che non sia corrotto.")

def carica_log(file_path):
    """Carica log da file XES o CSV. Supporta entrambi i formati."""
    file_path_csv = file_path.replace("xes", "csv")
    
    if os.path.exists(file_path_csv):
        print("Caricamento CSV:", file_path_csv)
        log = _load_csv(file_path_csv)
    else:
        print("Caricamento XES:", file_path)
        log = pm4py.read_xes(file_path, return_legacy_log_object=False)
        log = pm4py.format_dataframe(log, case_id='case:concept:name', 
                                     activity_key='concept:name',
                                     timestamp_key='time:timestamp')
    
    if "case:concept:name" not in log.columns or \
       "concept:name" not in log.columns or \
         "time:timestamp" not in log.columns:
        log = normalize_columns(log)
    log = log[['case:concept:name', 'concept:name', 'time:timestamp']]
    
    log['case:concept:name'] = log['case:concept:name'].astype('str')
    log['concept:name'] = log['concept:name'].astype('str')
    log['time:timestamp'] = pd.to_datetime(log['time:timestamp'], errors='coerce')
    
    # Assicura che il timestamp non contenga NaT (Not a Time)
    log = log[log['time:timestamp'].notna()]
    
    # Ordina il log per case e timestamp
    log = log.sort_values(['case:concept:name', 'time:timestamp']).reset_index(drop=True)
    
    gc.collect()
    return log


def scopri_modello(log):
    """Utilizza l'Inductive Miner per ottenere Rete di Petri, Marcatura Iniziale e Finale. Così ho modelli con proprietà sound"""
    print("Modello")
    print(type(log), len(log))
    
    # Converti DataFrame a EventLog se necessario
    try:
        process_tree = inductive_miner.apply(log, variant=inductive_miner.Variants.IMd)
        gc.collect()
    except Exception as e:
        print("Errore durante la scoperta del modello:", e)
        if isinstance(log, pd.DataFrame):
            print("Riconvertendo DataFrame a EventLog")
            print(log.head(10)["concept:name"])
            from pm4py.objects.conversion.log import converter as log_converter
            log = log_converter.apply(log, variant=log_converter.Variants.TO_EVENT_LOG)

        #     log = pm4py.convert.convert_to_event_log(
        #     log,
        #     case_id_column='case:concept:name',
        #     activity_column='concept:name',
        #     timestamp_column='time:timestamp'
        # )
        process_tree = inductive_miner.apply(log, variant=inductive_miner.Variants.IMd)
        gc.collect()
        
    net, initial_marking, final_marking = convert.convert_to_petri_net(process_tree)
    gc.collect()
    return net, initial_marking, final_marking

def calcola_conformance(log, net, im, fm):
    """Calcola metriche di conformance checking: fitness e precision.
    
    Metrics:
    - Fitness: misura quante tracce sono riproducibili dal modello
    - Precision: evita overfitting identificando transizioni aggiuntive
    """
    fitness = fitness_token_based_replay(log, net, im, fm)
    gc.collect()
    
    precision = precision_token_based_replay(log, net, im, fm)
    gc.collect()
    
    # precision_escaping = precision_evaluator.apply(
    #     log, net, im, fm, 
    #     variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN
    # )
    gc.collect()
    
    return fitness, precision #, precision_escaping

def calcola_generalizzazione(log, net, im, fm):
    """Calcola le metriche di generalizzazione disponibili in pm4py."""
    print("generalizzazione token based")
    gen = generalization_tbr(log, net, im, fm)
    gc.collect()
    return gen

def calcola_semplicita(net):
    """Calcola metriche di semplicità strutturale.
    
    Metrics:
    - Arc Degree: densità media degli archi (meno è meglio)
    - Extended Cardoso: complessità ciclomatica estesa
    - Cyclomatic: numero di decisioni indipendenti nel modello
    """
    metrics = {
        'Arc Degree': simplicity_evaluator.Variants.SIMPLICITY_ARC_DEGREE,
        'Extended Cardoso': simplicity_evaluator.Variants.EXTENDED_CARDOSO,
        'Cyclomatic': simplicity_evaluator.Variants.EXTENDED_CYCLOMATIC
    }
    
    simplicity_scores = {}
    for name, variant in metrics.items():
        score = simplicity_evaluator.apply(net, variant=variant)
        simplicity_scores[name] = score
        gc.collect()
    
    return simplicity_scores



def ottimizza_tipi_dato(df):
    """Riduce l'uso della RAM convertendo stringhe in categorie."""
    for col in ['concept:name', 'case:concept:name']:
        if col in df.columns:
            df[col] = df[col].astype('category')
    gc.collect()
    return df



def k_fold_cross_validation(log, k=5):
    """Esegue k-fold cross-validation per stimare la generalizzazione.
    
    Divide il log in k fold, addestra il modello su k-1 fold e valuta su 1 fold.
    Fornisce una stima realistica della performance su dati non visti.
    """
    case_ids = log['case:concept:name'].unique()
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    
    resultati = []
    for train_idx, test_idx in kf.split(case_ids):
        train_log = log[log['case:concept:name'].isin(case_ids[train_idx])]
        test_log = log[log['case:concept:name'].isin(case_ids[test_idx])]
        
        net, im, fm = scopri_modello(train_log)
        fitness = fitness_token_based_replay(test_log, net, im, fm)
        resultati.append(fitness['log_fitness'])
        gc.collect()
    
    avg_fitness = sum(resultati) / len(resultati)
    return avg_fitness




def main(path_file, log_path=None):
    """Esegue analisi completa di Conformance Checking.
    
    Pipeline:
    1. Carica log e normalizza colonne
    2. Scopre modello di processo (Inductive Miner IMd)
    3. Valuta conformance sul training set
    4. Stima generalizzazione su test set (k-fold cross-validation)
    5. Calcola semplicità strutturale del modello
    """
    print(f"\n=== ANALISI CONFORMANCE CHECKING ===")
    print(f"Input: {path_file}\n")
    
    log = carica_log(path_file)
    print(f"Log caricato: {len(log)} eventi, {log['case:concept:name'].nunique()} tracce\n")
    
    net, im, fm = scopri_modello(log)
    gc.collect()
    
    print("\n--- METRICHE DI CONFORMANCE (Training Set) ---")
    fit, prec = calcola_conformance(log, net, im, fm)
    
    print("\n--- METRICHE DI GENERALIZZAZIONE (Training Set) ---")
    gen = calcola_generalizzazione(log, net, im, fm)
    
    print("\n--- GENERALIZZAZIONE (K-Fold Cross-Validation) ---")
    k = 5
    gen_kfold = k_fold_cross_validation(log, k=k)
    
    print("\n--- METRICHE DI SEMPLICITÀ ---")
    simplicity = calcola_semplicita(net)
    
    print(f"\n\n=== RISULTATI FINALI ===")
    print(f"File: {path_file}")
    print(f"\nCONFORMANCE:")
    print(f"  Fitness (Token-based):      {fit}")
    print(f"  Precision (Token-based):    {prec}")
    # print(f"  Precision (Escaping Edges): {prec_escaping:.4f}")
    print(f"\nGENERALIZZAZIONE:")
    print(f"  Generalization (Training):  {gen}")
    print(f"  Generalization ({k}-fold):  {gen_kfold}")
    print(f"\nSEMPLICITÀ:")
    for name, score in simplicity.items():
        print(f"  {name}: {score:.4f}")
    print(f"\n=== FINE ===")
    
    if log_path:
        with open(log_path, 'w') as f:
            f.write(f"Conformance Checking Report\n")
            f.write(f"File: {path_file}\n")
            f.write(f"Fitness: {fit}\n")
            f.write(f"Precision: {prec}\n")
            f.write(f"Generalization: {gen}\n")
            f.write(f"Generalization k-fold: {gen_kfold}\n")


    
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