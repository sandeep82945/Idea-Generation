# Improved Python code based on the algorithm for future work extraction

# Placeholder for the complete list of regular expressions for both tiers

import re
TR1 = [
    r"we will", r"we plan", r"we want", 
    r"we wish", r"future", r"to extend", 
    # Placeholder for other ten regular expressions
]

TR2 = [
    r"we can", r"we believe", r"we could", 
    r"is to", r"further", r"suggest", r"promising", 
    r"potential",
    # Placeholder for other eleven regular expressions
]


# The algorithm to extract future work sentences
def future_work_extraction_algorithm(F):
    FS = []  # The future work sentence set
    FWFound = False  # A flag to check if a TR1 match was found
    
    # Compile regular expressions for efficiency
    TR1_patterns = [re.compile(regex) for regex in TR1]
    TR2_patterns = [re.compile(regex) for regex in TR2]
    
    # Process each sentence in F
    for s in F:
        # Check against first tier regular expressions
        if any(pattern.search(s) for pattern in TR1_patterns):
            FS.append(s)
            FWFound = True
        # If a first tier match was found, then reset FWFound after checking second tier
        elif FWFound:
            if any(pattern.search(s) for pattern in TR2_patterns):
                FS.append(s)
            FWFound = False  # Reset the flag as per the algorithm's instruction
    
    return FS
