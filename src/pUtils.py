from src.Pyraminx import Pyraminx
import random
from src.PyraminxSolver import PyraminxSolver

# SOLVED_PYRAMINX = Pyraminx([1,1,1,1,1,1,1,1,1], [2,2,2,2,2,2,2,2,2], [3,3,3,3,3,3,3,3,3], [4,4,4,4,4,4,4,4,4])

def scramble(algo):
  pyraminx = solvedPyraminx()
  pyraminx.applyAlgo(algo)
  return pyraminx

def missingNum(array, totalSum = 10):
  for i in array:
    totalSum -= i
  return totalSum

def getSwitcher(pyraminx):
  yellow = missingNum((pyraminx.red_face[0][0], pyraminx.green_face[0][1], pyraminx.blue_face[0][2]))
  red = missingNum((pyraminx.yellow_face[0][0], pyraminx.blue_face[0][1], pyraminx.green_face[0][2]))
  green = missingNum((pyraminx.blue_face[0][0], pyraminx.yellow_face[0][1], pyraminx.red_face[0][2]))
  blue = missingNum((pyraminx.green_face[0][0], pyraminx.red_face[0][1], pyraminx.yellow_face[0][2]))
  switcher = {yellow: 4, red: 1, green: 2, blue: 3}
  return switcher

def fixColors(pyraminx):
  switcher = getSwitcher(pyraminx)
  for i in range(3):
    for j in range(3):
      pyraminx.red_face[i][j] = switcher[pyraminx.red_face[i][j]]
      pyraminx.green_face[i][j] = switcher[pyraminx.green_face[i][j]]
      pyraminx.yellow_face[i][j] = switcher[pyraminx.yellow_face[i][j]]
      pyraminx.blue_face[i][j] = switcher[pyraminx.blue_face[i][j]]
  return pyraminx

def faceIsSolved(face):
  color = face[0][0]
  for i in range(3):
    for j in range(3):
      if face[i][j] != color:
        return 0
  return 1

def isSolved(pyraminx):
  if not faceIsSolved(pyraminx.red_face):
    return 0
  if not faceIsSolved(pyraminx.green_face):
    return 0
  if not faceIsSolved(pyraminx.blue_face):
    return 0
  if not faceIsSolved(pyraminx.yellow_face):
    return 0
  return 1

def checkSolution(pyraminx, algo):
  newP = pyraminx.copy()
  newP.applyAlgo(algo)
  return isSolved(newP)

def rotateList(givenList, rotations):
  length = len(givenList)
  rotations %= length
  for rotation in range(rotations):
    lastElem = givenList[-1]
    givenList = givenList[:-1]
    givenList.insert(0, lastElem)
  return givenList

# numOfRots should be number of CLOCKWISE rotations of whole pyraminx
# algo should be algo applied from non-standard orientation
def modifyAlgoForOrientation(algo, numOfRots):
  if numOfRots%3 == 0:
    return algo

  clockwiseSwitcher = {
    "U":"U", "U'":"U'",
    "F":"R", "F'":"R'",
    "R":"L", "R'":"L'",
    "L":"F", "L'":"F'"
  }
  anticlockwiseSwitcher = {
    "U": "U", "U'": "U'",
    "F": "L", "F'": "L'",
    "R": "F", "R'": "F'",
    "L": "R", "L'": "R'"
  }

  if numOfRots%3 == 1:
    for i in range(len(algo)):
      algo[i] = clockwiseSwitcher[algo[i]]
  elif numOfRots%3 == 2:
    for i in range(len(algo)):
      algo[i] = anticlockwiseSwitcher[algo[i]]
  return algo

# Method to add start and end rotations to algo acc to top rotations
# FOR LayerSolver.insertEdge()
def fixAlgoWithRots(algo, clockRots):
  clockRots %= 3
  if clockRots == 0:
    return algo
  if clockRots == 1:
    algo.append("U'")
    algo.insert(0, "U")
    return algo
  if clockRots == 2:
    algo.append("U")
    algo.insert(0, "U'")
    return algo

# Method to check if an edgeMap is solved
def edgeMapSolved(edgeMap):
  eMap = edgeMap.map
  # For red face
  red_bottom = eMap[0][0][1] # + eMap[1][2][0] + eMap[1][1][1]
  if red_bottom != eMap[1][2][0] or red_bottom != eMap[1][1][1]:
    # print("Red face not solved")
    return 0
  green_bottom = eMap[0][1][1] # + eMap[1][0][0] + eMap[1][2][1]
  if green_bottom != eMap[1][0][0] or green_bottom != eMap[1][2][1]:
    # print("Green face not solved")
    return 0
  blue_bottom = eMap[0][2][1] # + eMap[1][1][0] + eMap[1][0][1]
  if blue_bottom != eMap[1][1][0] or blue_bottom != eMap[1][0][1]:
    # print("Blue face not solved")
    return 0
  return 1

# Helper function for algo simplifier
def inv(move):
  inverter = {
    "U": "U'", "U'": "U",
    "F": "F'", "F'": "F",
    "R": "R'", "R'": "R",
    "L": "L'", "L'": "L",
    "u": "u'", "u'": "u",
    "f": "f'", "f'": "f",
    "r": "r'", "r'": "r",
    "l": "l'", "l'": "l"
  }
  return inverter[move]

# Cleans the algo by removing redundant steps, etc
# Method is for just one go-through-the-algo
# Use it successively for full cleaning
def simplifyAlgoOnce(algo):
  length = len(algo)
  if length < 2:
    return algo
  if algo[0] == inv(algo[1]):
    return simplifyAlgoOnce(algo[2:])
  if algo[0] == algo[1]:
    return [inv(algo[0])] + simplifyAlgoOnce(algo[2:])
  return [algo[0]] + simplifyAlgoOnce(algo[1:])

# Cleans the algo
def simplifyAlgo(algo):
  while algo != simplifyAlgoOnce(algo):
    algo = simplifyAlgoOnce(algo)
  return algo

# Random scramble generator
def generateScramble(length):
  moves = ["U", "F", "R", "L", "U'", "F'", "R'", "L'"]
  rScramble = []
  for i in range(length):
    rScramble.append(random.choice(moves))
  return rScramble

# Returns a solved pyraminx
def solvedPyraminx():
  SOLVED_PYRAMINX = Pyraminx([1,1,1,1,1,1,1,1,1], [2,2,2,2,2,2,2,2,2], [3,3,3,3,3,3,3,3,3], [4,4,4,4,4,4,4,4,4])
  return SOLVED_PYRAMINX

def checkIfValidConfig(pyraminx):
  try:
    newP = pyraminx.copy()
    solver = PyraminxSolver(newP)
    algo = solver.solve()
  except:
    return 0
  else:
    return checkSolution(pyraminx, algo)
