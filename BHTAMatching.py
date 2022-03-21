import numpy as np
import random
import itertools
from itertools import permutations
import matplotlib.pyplot as plt
from scipy.optimize import basinhopping

static_q = None
static_solution = None
good = []
bad = []

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
        for j in range(len(q['s'+str(i)])):
            q['s'+str(i)][j] = random.randint(0,5)
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
        score += qu["s" + str(student)][index]
        remove_col(qu, index)
        del qu["s"+ str(student)]
    return score, qu

def removes(bads, qu):
    # for all the pairs in bads, set them to a very bad number
    for (student, index) in bads:
        qu["s" + str(student)][index] = -1000
    return qu
    
def get_quality_score(student_num, class_num):
    global static_q
    q = static_q
    return q['s'+str(student_num)][class_num]

def calculate_full_score(solution):
    return solution[0]

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

def monte(qu, classes):
    N = 1000
    histogram = np.zeros(N)
    for i in range(N):
        histogram[i] = randomMatch(qu.copy(), classes.copy())[0]
    plt.hist(histogram)
    plt.show()

def rank_solution(pairings): # Given dictionary and matchings... rank
    answer = 0 
    global static_q
    for i in range(len(pairings)):
        answer += static_q['s'+str(i)][int(pairings[i])] # ranking is just how good the pairing was... 
    for i in range(len(good)):
        if (pairings[good[i][0]] != good[i][1]):
            return 10000
    for i in range(len(bad)):
        if (pairings[bad[i][0]] == bad[i][1]):
            return 10000
    return -1 * answer

def generate_candidate(pairings): ## do a random swap...
    idx1 = random.randrange(len(pairings))
    idx2 = random.randrange(len(pairings))
    while idx2 == idx1:
        idx2 = random.randrange(len(pairings))
    t = pairings[idx1]
    pairings[idx1] = pairings[idx2]
    pairings[idx2] = t
    return pairings

def get_starting_point(qu):
    return [i for i in range(len(qu))] # Basic starting point, match diagonally...

def change_class(qu, ci, number):
    # change the quality for some specific class...
    for student in qu.keys():
        qu[student][ci] += number
    return qu
    
if __name__ == "__main__":
    num_students = 20
    num_classes = 20
    q, classes = gen_quality_dyn(num_students,num_classes)
    static_q = q
    #print(static_q)
    #print(get_quality_score(0, 0))

    good = [(0,0), (1,1)]
    bad = [(2,2), (3,3)]
    
    #print("\ngreedy")
    #print(greedy(q.copy(), good, bad, classes.copy()))
    static_solution = greedy(q.copy(), good, bad, classes.copy())

    res = basinhopping(rank_solution, get_starting_point(q), take_step=generate_candidate, niter=1000)
    print(res)
    print(static_solution)