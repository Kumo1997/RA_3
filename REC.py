import random
import randomhash 

def recordinality(stream, k, seed = None):
    # Initialize the set S with the first k distinct elements (hashed values)
    S = set()
    R = k
    if seed is not None:
        random.seed(seed)
    
    for z in stream:
        if isinstance(z, list): 
            z = " ".join(z)
        y = randomhash.hash(z) 
        if len(S) < k:
            S.add(z)
        elif y > min([randomhash.hash(x) for x in S]) and z not in S:
            min_element = min(S, key=lambda x: randomhash.hash(x))
            S.remove(min_element)
            S.add(z)
            R += 1
            
    # Return the estimated cardinality
    estimated_cardinality = k * (1 + 1 / k) ** (R - k + 1) - 1
    return estimated_cardinality
