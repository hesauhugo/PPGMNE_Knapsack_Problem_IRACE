import numpy as np
import pandas as pd

row = 30
col = 20
density = 0.6
rep = 25

for r in range(rep):
    RHS = np.zeros(row)

    A = 100*np.random.rand(row, col)
    Utility = 10*np.random.rand(col)    
    RHSrand =  np.random.normal(density, density/4, row)
    # print("Normal:", RHSrand)
    for i in range(len(RHSrand)):
        RHSrand[i] = min(RHSrand[i], 0.99)
        
    # print("Normal:", RHSrand)
    # print("ASum:", A.sum(axis = 1))
    RHS = A.sum(axis = 1)*RHSrand
    # print("RHS:",RHS)

    fname = "Knap_C" + str(row) + "I" + str(col) + "REP" + str(r+1) + ".txt"
    f=open(fname,'w')
    f.write(str(row) + "\n\n")
    f.write(str(col) + "\n\n\n")
    np.savetxt(f, Utility, fmt='%1.3f',newline=" ")
    f.write("\n\n")
    np.savetxt(f, A, fmt='%1.3f')
    f.write("\n")
    np.savetxt(f, RHS, fmt='%1.3f',newline=" ")
    f.write("\n")
    f.close()
