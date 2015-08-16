"""
    minimum_edit_distance.py
    Implementation of Minimum Edit Distance (Levenshtein) algorithm
    --------------------------------------------
    Uses a DP approach to compute the minimum edit distance between two 
    strings.  Specifically, it computes the minimum number of editing 
    operations needed to transform one string into another.  This specific
    algorithm uses Levenshtein's version in which the substitution operation
    counts as two operations.

    Time Complexity: O(NM) where N = len(s1) and M = len(s2)

    Source: https://web.stanford.edu/class/cs124/lec/med.pdf
"""

COST_OF_ADD = 1
COST_OF_DEL = 1
COST_OF_SUB = 2
COST_OF_MATCH = 0

def min_edit_distance(s1, s2):
    n = len(s1)
    m = len(s2)
    ed_table = _initialize_distance_table(n, m)
    for i in range(1, n+1):
        for j in range(1, m+1):
            deletion = ed_table[i-1][j] + COST_OF_DEL
            addition = ed_table[i][j-1] + COST_OF_ADD
            if s1[i-1] == s2[j-1]:
                substitution = ed_table[i-1][j-1] + COST_OF_MATCH
            else:
                substitution = ed_table[i-1][j-1] + COST_OF_SUB

            ed_table[i][j] = min(deletion, addition, substitution)
    return ed_table[n][m]

def _initialize_distance_table(n, m):
    ed_table = [[0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(1, n+1):
        ed_table[i][0] = ed_table[i-1][0] + COST_OF_DEL
    for j in range(1, m+1):
        ed_table[0][j] = ed_table[0][j-1] + COST_OF_ADD
    return ed_table
