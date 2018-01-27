import sys
import nqueens as nq
import math

print('Python version:', sys.version)
average_epochs=0
fails=0
print("Enter number of tries and maximum epochs")
num_of_tryes=int(input())
max_epochs = int(input())
for i in range(1,num_of_tryes):
    solver=nq.Solver_8_queens()
    best_fit, epoch_num, visualization = solver.solve(0.9, max_epochs)
    if math.fabs(best_fit - 1.0) <0.00001 :
        average_epochs+=epoch_num
    else:
        fails+=1
    print(best_fit, epoch_num)
print ( "number of fails", fails)
print ("average epoches", average_epochs //(num_of_tryes-fails))