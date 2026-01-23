import numpy as np

def get_initial_activities(dfg_matrix):
    """
    Identifica le attività iniziali nel DFG.
    Un'attività è iniziale se non ha predecessori (colonna con somma 0).
    
    Args:
        dfg_matrix: matrice numpy rappresentante il DFG
    
    Returns:
        array di indici delle attività iniziali
    """
    # eliminate 1 on diagonal, 
    # if there is a loop from an activity to itself the value on the diagonal is >0
    for i in range(dfg_matrix.shape[0]):
        dfg_matrix[i, i] -= 1

    # computer incoming edges by summingn rows and look at columns
    incoming_edges = np.sum(dfg_matrix, axis=0)
    # if a column sums to 0, that activity has no incoming edges
    initial_activities = np.where(incoming_edges == 0)[0]

    return initial_activities


def get_final_activities(dfg_matrix):
    """
    Identifica le attività finali nel DFG.
    Un'attività è finale se non ha successori (riga con somma 0).
    
    Args:
        dfg_matrix: matrice numpy rappresentante il DFG
    
    Returns:
        array di indici delle attività finali
    """
    # eliminate 1 on diagonal, 
    # if there is a loop from an activity to itself 
    # there is no problem to make a diagonal = 0
    # because if there aren't any other successors, it is final
    for i in range(dfg_matrix.shape[0]):
        dfg_matrix[i, i] -= dfg_matrix[i, i] 
    
    
    outgoing_edges = np.sum(dfg_matrix, axis=1)
    
    final_activities = np.where(outgoing_edges == 0)[0]
    return final_activities


def get_source_and_sink_activities(dfg_matrix):
    """
    Identifica sia le attività iniziali che finali.
    
    Args:
        dfg_matrix: matrice numpy rappresentante il DFG
    
    Returns:
        tuple: (initial_activities, final_activities)
    """
    initial = get_initial_activities(dfg_matrix)
    final = get_final_activities(dfg_matrix)
    return initial, final


def get_activity_connectivity(dfg_matrix):
    """
    Restituisce il grado di connettività di ogni attività.
    
    Args:
        dfg_matrix: matrice numpy rappresentante il DFG
    
    Returns:
        dict con 'incoming' e 'outgoing' e 'total' per ogni attività
    """
    n_activities = dfg_matrix.shape[0]
    connectivity = {
        'incoming': np.sum(dfg_matrix, axis=0),
        'outgoing': np.sum(dfg_matrix, axis=1),
        'total': np.sum(dfg_matrix, axis=0) + np.sum(dfg_matrix, axis=1)
    }
    return connectivity