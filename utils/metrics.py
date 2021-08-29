import numpy as np

def mrr_k(relev_positions, k):
    for rl in relev_positions:
        if rl <= k:
            return 1 / rl
    return 0

def mrr(true, prediction, K=5):
    array = []
    for true_label, pred in zip(true, prediction):
        relev_positions = []
        for pred_id, pred_label in enumerate(pred):
            if true_label == pred_label:
                relev_positions.append(pred_id + 1)
        array.append(mrr_k(relev_positions, K))
    return np.mean(array)