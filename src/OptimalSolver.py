# from Pyraminx import Pyraminx
from src import pUtils, cli
from src.CentreSolver import CentreSolver
import time

moves = ["U", "F", "R", "L"]

algorithms = []
timeLimit = 30
def dfsearch(pyraminx, Time):
  layer = []
  solvedP = pUtils.solvedPyraminx()
  if pyraminx.eq(solvedP):
    print("Already solved?")
    algorithms.append([])
    return []
  layer.append((pyraminx, []))
  while True:
    newLayer = []
    for p in layer:
      add =  generateNeighbors(p[0], p[1], Time)
      if add == -789:
        return -789
      newLayer += add

    layer = newLayer
    for p in layer:

      if time.time() - Time >= timeLimit:
        return -789
      if p[0].eq(solvedP):
        return p[1]
    if len(layer[0][1]) >= 14:
      print("No solution found. Sorry.")
      return []

def generateNeighbors(pyraminx, scramble, Time):
  neighbors = []
  for move in moves:
    neighbors.append((pyraminx.makeMove(move), scramble + [move]))
    if time.time() - Time >= timeLimit:
      return -789
  return neighbors


def solveP(pyraminx, algo, Time):
  solvedP = pUtils.solvedPyraminx()
  currP = pyraminx.copy()
  currP.applyAlgo(algo)
  if currP.eq(solvedP):
    algorithms.append(algo)
    return 1
  if len(algo) >= 12:
    return 0
  else:
    for moveId in moves:
      if time.time() - Time >= timeLimit:
        return -789
      # print("Making move: " + moveId)
      newAlgo = algo[:]
      newAlgo.append(moveId)
      # cli.printAlgo(newAlgo)
      # cli.printPyraminx(pyraminx)
      solved = solveP(pyraminx, newAlgo)
      if solved:
        # print("RETURNED!!")
        return 1
    return 0

def solve(pyraminx):
  Time = time.time()
  cSolver = CentreSolver(pyraminx.copy())
  tipAlgo = cSolver.solveTips()
  pyraminx.applyAlgo(tipAlgo)
  # solveP(pyraminx, [])
  algo = dfsearch(pyraminx, Time)
  if algo == -789:
    return -789
  # return tipAlgo + pUtils.simplifyAlgo(algorithms[0])
  return tipAlgo + pUtils.simplifyAlgo(algo)


