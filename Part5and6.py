'''
This file if for #5 and 6, Once 1-4 are completeted we can use this

Report: #5. Version space learning algorithm is a good alternative for approximating the opponents moves. Our current
algorithm runs on a hypothesis at a time method that can cause runtime and storage issues. Version space learning
algorithm would only retain hypothesis that are not ruled out after shortening the list. In other words we assume the
the most likely scenarios are correct and we remove the least likely scenarios. This algorithm takes a set of all
hypotheses and returns a subset that are not empty or within a certain margin. Since this algorithm is incremental
backtracking is not necessary. We use generalization and specialization space to order our targeted set. When Version
space is called, taking the matrix as the example space, it sets V = to the set of all hypotheses. Then it checks if
V is empty, if not then it updates the set using Version_Space_Update, taking in V and the set of examples space.
V will then be compared to generalized set and specialized set and return a set of the best hypothesis.

DO NOT INCLUDE-needs work

We decided to set the G_set with xxxx boundaries.
We decided to set the S_set with xxxx boundaries.

'''




#should take the matrix as the example case

def Version_Space_Learning(data_set):

    #V = Set_of all hyoptheses
    V = ObservationList
    for examples in data_set:
        if V is not data_set:
            V = Version_Space_Update(V,examples)
    return V
#returns and updated version of versionSpace
#takes a set of all hypotheses and compares to the set values of the matrix
#returns updated version Space
def Version_Space_Update(V,e):
    'the First step is to check the example and append to either B or S depending on qualifications'
    #G_set is defined as the general boundaries in the OVERALL set of examples
    #S_set is defined as the specific boundaries in the OVERALL set of Examples
    G_set = []
    S_set = []

    if e[0] or e[1] or e[2]

    '''These rules must be followed for S and B
    False positive for S,•: This means S, is too general, but there are no consistent specializations
    of 5,- (by definition), so we throw it out of the S-set.
    2. False negative for S,: This means S,- is too specific, so we replace it by all its immediate
    generalizations.
    3. False positive for G,: This means G, is too general, so we replace it by all its immediate
    specializations.
    4. False negative for G,: This means G, is too specific, but there are no consistent generalizations of G, (by definition) so we throw it out of the G-set.'''
    'The second step is to '

    #we set V to the set of examples that are between G-set and S-set
    #V = {h G V: h is consistent with e}

    'If S or G is empty, no consistent hypothesis'

    return #We return V as a set of the most optimal Hypothesis between S and B
