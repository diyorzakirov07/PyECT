'''
Created on Jan 15, 2020

@author: Diyor.Zakirov
'''
from netCDF4 import Dataset
import numpy as np
from scipy.stats.mstats_basic import pearsonr
import multiprocessing as mp
import matplotlib.pyplot as plt
import os

badVars = mp.Manager().list()

#Creates single variable files out of ensemble data.
#You can change the directory where you want your new data saved
#and what kind of data you will be sorting.
#In this example data is saved to /work/Diyor.Zakirov/ensembleData/
#Data used 19790101.atmos_month.tileX.nc
def sortData():
    for i in range(1,352):
        os.mkdir("/work/Diyor.Zakirov/ensembleData/" + str(i))
        os.chdir("/work/Diyor.Zakirov/ensembleData/" + str(i))
        for key in Dataset("/work/Thomas.Robinson/ensemble/ensemble_home/gfdl.intel-prod-openmp-mid/" + str(i) + "/19790101.atmos_month.tile1.nc").variables.keys():
            os.system("ncks -C -v " + key + " /work/Thomas.Robinson/ensemble/ensemble_home/gfdl.intel-prod-openmp-mid/" + str(i) + "/19790101.atmos_month.tile1.nc /work/Diyor.Zakirov/ensembleData/" + str(i) + "/" + key + "_tile1.nc")
            os.system("ncks -C -v " + key + " /work/Thomas.Robinson/ensemble/ensemble_home/gfdl.intel-prod-openmp-mid/" + str(i) + "/19790101.atmos_month.tile2.nc /work/Diyor.Zakirov/ensembleData/" + str(i) + "/" + key + "_tile2.nc")
            os.system("ncks -C -v " + key + " /work/Thomas.Robinson/ensemble/ensemble_home/gfdl.intel-prod-openmp-mid/" + str(i) + "/19790101.atmos_month.tile3.nc /work/Diyor.Zakirov/ensembleData/" + str(i) + "/" + key + "_tile3.nc")
            os.system("ncks -C -v " + key + " /work/Thomas.Robinson/ensemble/ensemble_home/gfdl.intel-prod-openmp-mid/" + str(i) + "/19790101.atmos_month.tile4.nc /work/Diyor.Zakirov/ensembleData/" + str(i) + "/" + key + "_tile4.nc")
            os.system("ncks -C -v " + key + " /work/Thomas.Robinson/ensemble/ensemble_home/gfdl.intel-prod-openmp-mid/" + str(i) + "/19790101.atmos_month.tile5.nc /work/Diyor.Zakirov/ensembleData/" + str(i) + "/" + key + "_tile5.nc")
            os.system("ncks -C -v " + key + " /work/Thomas.Robinson/ensemble/ensemble_home/gfdl.intel-prod-openmp-mid/" + str(i) + "/19790101.atmos_month.tile6.nc /work/Diyor.Zakirov/ensembleData/" + str(i) + "/" + key + "_tile6.nc")
            os.system("ncecat " + key + "_tile[1-6].nc " + key + ".nc")
            os.remove(key + "_tile1.nc")
            os.remove(key + "_tile2.nc")
            os.remove(key + "_tile3.nc")
            os.remove(key + "_tile4.nc")
            os.remove(key + "_tile5.nc")
            os.remove(key + "_tile6.nc")
            

#Checks the variance of all sorted variables
#and appends variable name to badVars if variance is close to 0
def checkVariance(variableName):
    varianceArr = np.empty(0)
    for i in range(1,352):
        data = Dataset("/work/Diyor.Zakirov/ensembleData/" + str(i) + "/" + variableName + ".nc").variables[variableName]
        variance = np.var(data)
        if variance < 0.01:
            varianceArr = np.append(varianceArr, variance)
            
    if len(varianceArr) > 350:
        print(variableName + "_" + str(len(varianceArr)))
        badVars.append(variableName)
                
#Creates correlation graphs from the correlation data    
def plotCorr(variableName):
    data = Dataset("/home/Diyor.Zakirov/Heatmaps/" + variableName + ".nc").variables["corr_data"][:,:]
    
    fig, ax = plt.subplots()
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.savefig("/home/Diyor.Zakirov/Heatmaps_Graphs/" + variableName + ".pdf")   
    
    print(variableName)

#Creates new files that contain correlation data for each variable between ensembles     
def getCorr(variableName):
    corrArr = np.zeros((352,352))
    for i in range(1,352):
        print(variableName + "_" + str(i))
        dataI = Dataset("/work/Diyor.Zakirov/ensembleData/" + str(i) + "/" + variableName + ".nc").variables[variableName][:].flatten()
        for j in range(1,352):
            dataJ = Dataset("/work/Diyor.Zakirov/ensembleData/" + str(j) + "/" + variableName + ".nc").variables[variableName][:].flatten()
            
            corr = pearsonr(dataI, dataJ)
            corrArr[i][j] = corr[0]
            
    
    newNcFile = Dataset("/home/Diyor.Zakirov/Heatmaps/" + variableName + '.nc', 'w')
    newNcFile.description = 'Correlation data for variable: ' + variableName
    
    newNcFile.createDimension('memberX', 352)
    newNcFile.createDimension('memberY', 352)
    
    corr_data = newNcFile.createVariable('corr_data', np.float32, ('memberX', 'memberY'))
    corr_data[:,:] = corrArr[:,:] 
    
    newNcFile.close()
    
        
    return corrArr

#Writes good variables to a txt file
def writeVars():
    goodVarsFile = open("/home/Diyor.Zakirov/Documents/statVars.txt", 'w')
    for var in os.listdir("/work/Diyor.Zakirov/ensembleData/1"):
        if var.split(".")[0] not in badVars:
            goodVarsFile.write(var.split(".")[0] + "\n")
        
    goodVarsFile.close()
    
if __name__ == '__main__':
    
    sortData()
    
    variableList = []
    for variable in os.listdir("/work/Diyor.Zakirov/ensembleData/1"):
            variableList.append(variable.split(".")[0])
    
    #Change amount of core to desired number
    pool = mp.Pool(16)
    
    results = pool.map(checkVariance, [variableName for variableName in variableList])
    
    writeVars()

    
    
    
