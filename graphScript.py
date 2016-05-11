## The goal of this project is to put together a directed graph of UW courses with
## Math courses as prerequisites.  I'll put together a graph of all courses with
## Prereqs indicated by directed edges.  Then I can run dfs from a given course
## to find everything that has that in its prerequistie lineage.

## This will involve using regular expressions to dissect the UW course catalog.

import os
import re

os.chdir("C:\Users\Kris\Documents\PythonProjects\UWMathPrerequisites")

def getCourses(courseAbbrev, filename):
    """
    Returns a set of all course abbreviations that have courseAbbrev 
    as a prerequisite, as well as courseAbbrev itself.
    """
    descriptions = buildDescriptions(filename)
    #print(descriptions)
    abbreviations, abbrevDict, adjacencyList = buildAdjacencyList(descriptions)
    titles = courseTitles(descriptions)
    startingIndex = abbrevDict[courseAbbrev]
    #print("Starting at: "+str(startingIndex))
    postReqs = dfs(startingIndex, adjacencyList)
    result = []
    for index in postReqs:
        result.append(abbreviations[index]+" "+titles[index])
    return set(result[1:])


def buildDescriptions(filename):
    """
    Takes a filename for the text file of course descriptions.
    Returns a list of lists.
    Each item in the outer list corresponds to a course from the catalog.
    Each item is a list of 2-3 strings, depending on how the entry was
    formatted in the UW ccourse catalog.
    """
    #Read data into a list.
    L = []
    with open(filename) as infile:
        for line in infile:
            L.append(line)
    #Rearrange as list of lists.  
    #Each line in the outer list corresponds to a single course.
    #There can be 2-3 strings per inner list, depending on the course description
    #as it appears onthe UW website.
    descriptions = [[]]
    for line in L:
        if line == "\n":
            descriptions.append([])
        else:
            descriptions[-1].append(line)
    return descriptions




def buildAbbreviationsAndDictionary(descriptions):
    """
    Returns a list and a dictionary.  The list contains all the couse abbreviations
    found in the course desccriptions.  The dictionary provides a lookup table to
    determine which index for the list corresponds to a given abbreviation.
    We use regular expressions to extract the abbrevation by searching for a substring
    of the form NON_WHITE_SPACE_CHARACTERS-single-space-NON_WHITE_SPACE_CHARACTERS.
    """
    abbreviations = []
    abbrevDictionary = {}
    for entry in descriptions:
        match = re.search("\S* \S*",entry[0])
        abbrev = entry[0][match.start():match.end()]
        abbreviations.append(abbrev)
        abbrevDictionary[abbrev]=(len(abbreviations)-1)
    return abbreviations, abbrevDictionary
    

    
def findMatches(prereqCourse, descriptions):
    """
    This funnction takes a course abbreviation (e.g. "MATH 124") and identifies
    the indices of items in the list descriptions for which that course is 
    a prerequisite.
    """
    result = []
    for k in xrange(len(descriptions)):
        pattern = "Prerequisite:.*"+prereqCourse
        match = re.search(pattern, descriptions[k][1])
        if match != None:
            result.append(k)
    return result
    

def buildAdjacencyList(descriptions):
    """
    Returns a list of course abbreviations, a lookup dictionary, and an
    adjacency list.  The adjacency list can be used to construct a digraph.
    Each row of the adjacenncy list corresponds to a course from the descriptions,
    and the items in that row are indices of courses which have that course as
    a prerequisite.
    """
    abbreviations, abbrevDict = buildAbbreviationsAndDictionary(descriptions)
    result = []
    for abbrev in abbreviations:
        result.append(findMatches(abbrev, descriptions))
    return abbreviations, abbrevDict, result
    
### Now I want to code up either DFS or BFS to find all the courses that have,
### say, MATH 124 as a prerequisite.

### I think DFS would be easier to code because I can just use a list as a stack.
### There shouldn't be any need for recursion.

def dfs(startingIndex, adjacencyList):
    """
    Returns a list of all indices of nodes reachable from startingIndex,
    INCLUDING the startingIndex, even if there is no self-loop there.
    If that is not desired, the user should ignore the first entry of the
    returned list.
    """
    stack = [startingIndex]
    #print(stack)
    #raw_input()
    result = []
    visited = {}
    while stack != []:
        #print("Stack:")
        #print(stack)
        current = stack.pop()
        visited[current] = True
        #print("Adjacent Items:")
        #print(adjacencyList[current])
        #if raw_input() == "b":
            #break
        for item in adjacencyList[current]:
            if not visited.get(item):
                stack.append(item)
                result.append(current)
    return result

def courseTitles(descriptions):
    titles = []
    for entry in descriptions:
        abbrevMatch = re.search("\S* \S*",entry[0])
        e = abbrevMatch.end()
        stringFollowingAbbrev = entry[0][e:]
        titleMatch = re.search(".*\(", stringFollowingAbbrev)
        title = stringFollowingAbbrev[titleMatch.start():titleMatch.end()-2]
        titles.append(title)
    return titles
    
def writeCoursesToFile(courseSet, filename):
    courseList = list(courseSet)
    courseList.sort()
    with open(filename, "w") as outputfile:
        for item in courseList:
            outputfile.write("%s\n" % item)
            

