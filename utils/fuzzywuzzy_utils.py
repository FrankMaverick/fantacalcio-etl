from fuzzywuzzy import fuzz

def fuzzy_match_name(name, existing_names):
    """
    Confronta il nome con quelli esistenti utilizzando fuzzywuzzy e restituisce il miglior match.
    
    Args:
    - name (str): Il nome da confrontare.
    - existing_names (list): Elenco dei nomi esistenti da confrontare.
    
    Returns:
    - str: Il miglior match trovato tra i nomi esistenti.
    - int: Il punteggio di similarità del match.
    """
    best_match = None
    highest_score = 0
    
    for existing_name in existing_names:
        score = fuzz.WRatio(name, existing_name)
        if score > highest_score:
            highest_score = score
            best_match = existing_name
    
    return best_match, highest_score
