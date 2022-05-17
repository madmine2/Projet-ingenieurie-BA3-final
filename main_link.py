
from src import pUtils, cli
from src.PyraminxSolver import PyraminxSolver
from src import OptimalSolver
from src.Pyraminx import Pyraminx
import conversion
import time
import acquisition
from gpiozero import Button
#import raspberrypi_instead_of_arduino as ras

# utiliser main_acquisition pour récupérer la matrice des faces

#faces = main_acquisition()  (conceptuel)


a = ["334411113",
"233122433",
"412243344",
"121422241"]
b = ["333311114",
     "222233333",
     "111112222",
     "444444442"]
def main():
    matrix = []
    matrix2 = []
    isLast = [False,False,False,True]
    for i in range(4):
        matrix.append(main_acquisition.capture_video(isLast[i], button))
    print(matrix)
    for i in range(4):
        face = [int(a[i][j]) for j in range(9)]
        matrix2.append(face)


    #solveur pas optimal, envisager de laisser le choix avec solveur optimal
    pyraminx = Pyraminx(matrix[0], matrix[1], matrix[2], matrix[3])
    try:
        pyraminx = pUtils.fixColors(pyraminx)
    except:
        print("That's not a valid configuration. Aborting  .")
        return

    # Check if configuration is valid

    isValid = pUtils.checkIfValidConfig(pyraminx)
    if isValid == 0:
        print("That's not a valid configuration. Aborting .")
        return



#     algo = OptimalSolver.solve(pyraminx)
#     if algo == -789:
#         print("too long")
    pSolver = PyraminxSolver(pyraminx)
    algo = pSolver.solve()  # résous le pyraminx
    algo = pUtils.simplifyAlgo(algo) #simplifie l'algo
    #time.sleep(2) # problème avec les ports serial sans ce timer (pourquoi ???? I DON T FUCKING KNOW, je viens de perdre 2 heures à cause de ça)
    print([letter for letter in algo if letter.islower()])
    print([letter for letter in algo if letter.isupper()])
    main_arduino.main(algo, button)

    return


if __name__ == "__main__":
    while(True):
        button = Button(2)
        button.when_pressed = main
        pause()
