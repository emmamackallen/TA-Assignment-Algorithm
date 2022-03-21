import numpy as np
import random

def gen_quality():
    q = dict()
    quality = [1,2,3,4,5]
    # Generates a dictionary of
    # Student: [Qualities]
    q['a'] = np.random.permutation(quality)
    q['b'] = np.random.permutation(quality)
    q['c'] = np.random.permutation(quality)
    q['d'] = np.random.permutation(quality)
    #quality[-1] += 2
    q['e'] = np.random.permutation(quality)
    classesList = ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5"]
    return q, classesList

def gen_quality_dyn(students, classes):
    q = dict()
    classesList = []
    quality = [i for i in range(0, classes)]
    for i in range(students):
        q['s'+str(i)] = np.random.permutation(quality)
        classesList.append("Class " + str(i))
    return q, classesList
    
    
def remove_col(dic, index):
    # Remove a column in the dictionary by index
    for student in dic.keys():
        dic[student] = np.delete(dic[student], index)
    return dic
    
def max_with_index(arr):
    # Get the maximum (And the index where it resides (on the vector)) of some array
    maximum = max(arr)
    for i in range(len(arr)):
        if arr[i] == maximum:
            return i, maximum

def keeps(good, qu):
    score = 0
    # for a list students, take all the matchings in good
    for (student, index) in good:
        score += qu[student][index]
        remove_col(qu, index)
        del qu[student]
    return score, qu

def removes(bads, qu):
    # for all the pairs in bads, set them to a very bad number
    for (student, index) in bads:
        qu[student][index] = -1000
    return qu
    

def greedy(qu, good, bads, classes):
    # Greedy way to solve the problem after dealing with all the good and bad matchings
    #print(qu)
    score, qu = keeps(good, qu)
    #print(score)
    qu = removes(bads, qu)
    #print(qu)
    match = []
    while len(qu) != 0:
        student = ""
        idx, maximum = 0, 0
        for (k, v) in qu.items(): # repeat finding maximum till we run out...
            idx2, maximum2 = max_with_index(v) # find maximum value in student
            if maximum2 >= maximum:
                student = k
                idx, maximum = idx2, maximum2
        score += maximum
        qu = remove_col(qu, idx)
        #print("Matching Done....")
        match.append((student, classes[idx], maximum))
        #print(student, classes[idx], maximum)
        classes.pop(idx)
        del qu[student]
        #print(maximum)
    return score, match

def randomMatch(qu, classes):
    score = 0
    matches = []
    for student in qu:
        idx = random.randrange(len(qu[student]))
        quality = qu[student][idx]
        matches.append((student, classes[idx],quality))
        score += quality
        qu = remove_col(qu, idx)
        #print(qu)
        #print(str(student) + " " + str(idx) + " " + str(quality) + "\n")
        classes.pop(idx)
    return score, matches

def repeatRandom(qu, classes, attempts=1000):
    max = 0
    bestMatch = []
    for i in range(attempts):
        score, matching = randomMatch(qu.copy(), classes.copy())
        if (score > max): 
            max = score
            bestMatch = matching
    return max, bestMatch

def change_class(qu, ci, number):
    # change the quality for some specific class...
    for student in qu.keys():
        qu[student][ci] += number
    return qu
    
if __name__ == "__main__":
    q, classes = gen_quality_dyn(20,20)
    #good = [('a', 4)]
    q = change_class(q, 0, 10)
    #bad = [('e', -1)]
    good = []
    bad = []
    
    print("greedy")
    print(greedy(q.copy(), good, bad, classes.copy()))
    print("randomquick")
    print(repeatRandom(q, classes.copy()))
    print("randomslow")
    print(repeatRandom(q, classes.copy(), 100000))
    
