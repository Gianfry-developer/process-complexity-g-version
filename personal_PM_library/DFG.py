import polars as pl
import numpy as np
from pathlib import Path
import gc 


def create_dfg_from_csv(csv_path : str, activity :str = "concept:name", timestamp:str = "time:timestamp", case :str = "case:concept:case"):
    """
    Open a CSV file and generate a DFG (Directly-Follows Graph) as a numpy matrix.
    
    Args:
        csv_path: Path to the CSV file
        activity: Name of the activity column
        timestamp: Name of the timestamp column
        case: Name of the case column
        
    Returns:
        A uint32 numpy matrix where each cell contains the frequency of direct relations
        A dictionart with activities and associeted index
    """
    # Read CSV with polars
    df = pl.read_csv(csv_path)
    
    # Get unique activities (assuming activity column exists)
    activities = df.select(pl.col(activity)).unique().to_series().to_list()
    activities = sorted(activities)
    
    # Create activity to index mapping
    activity_to_idx = {act: idx for idx, act in enumerate(activities)}
    n_activities = len(activities)
    
    # Initialize DFG matrix
    dfg = np.zeros((n_activities, n_activities), dtype=np.uint32)
    
    df.sort([timestamp, case], reverse=[False, False], in_place=True)

    

    # Build DFG by counting direct follows
    for case_name, trace in df.group_by(case, maintain_order=True):
        current_act = trace[activity][0]
        current_act_idx = activity_to_idx[current_act]

        for events in trace.iter_rows():
            new_act = events[activity]
            next_act_idx = activity_to_idx[new_act]
            dfg[current_act_idx][next_act_idx] += 1
        gc.collect()
    return dfg, activity_to_idx


if __name__ == "__main__":
    # Example usage
    csv_file = "your_file.csv"
    dfg_matrix, activities = create_dfg_from_csv(csv_file)
    print(f"DFG Matrix shape: {dfg_matrix.shape}")
    print(f"Activities: {activities}")
    print(f"Matrix dtype: {dfg_matrix.dtype}")