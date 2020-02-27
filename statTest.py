'''
Created on Jan 7, 2020

@author: Diyor.Zakirov
'''
from netCDF4 import Dataset
import numpy as np
from scipy.stats.mstats_basic import pearsonr
import matplotlib.pyplot as plt
import multiprocessing as mp
import seaborn as sb
import os
from sklearn.decomposition import PCA as sklearnPCA


def getPCA(matrix):
    sklearn_pca = sklearnPCA(n_components = 2)
    transformData = sklearn_pca.fit(matrix).transform(matrix)
    eigenValues = sklearn_pca.explained_variance_ratio_
    #loadings = sklearn_pca.components_ * np.sqrt(sklearn_pca.explained_variance_ratio_)
    
    print(transformData)
    print(eigenValues)
    #print(np.shape(loadings))
    
    return eigenValues
        

    
def popMatrix(variableList):
    pca_matrix = np.zeros((11,5))
    
    for i in range(1,11):
        print(i)
        for index, varName in enumerate(variableList):
            data = Dataset("/work/Diyor.Zakirov/ensembleData/" + str(i) + "/" + varName + ".nc").variables[varName]
            mean = np.mean(data)
            pca_matrix[i, index] = mean
    
    print("Global means size: ", np.shape(pca_matrix))
    
    for col in pca_matrix:
        ensMean = np.mean(col)
        ensStd = np.std(col)
        for row in col:
            row = (row - ensMean) / ensStd
    
    print("Standarized matrix size:", np.shape(pca_matrix))
    print(pca_matrix)
    
    return pca_matrix
    
if __name__ == '__main__':
    
    variableList = ["cld_amt","qo3_col","vsurf","WVP","high_cld_amt"]
    '''
                "low_cld_amt",
                "mid_cld_amt","pct_uwd","wind_ref","vshear","bk","lwup_sfc","rh",
                "swdn_sfc","u_ref","tot_cld_amt","cin_uwc","reff_modis","swup_sfc",
                "pk","olr","vcomp","reff_modis2","liq_drp","rh_ref","droplets",
                "lwdn_sfc","plcl_uwc","pcb_uwc","land_mask","plfc_uwc","diff_m","aliq",
                "swdn_toa","plnb_uwc","tke_uwc","k_t_troen","swup_toa","zsurf","slp_dyn",
                "pct_uwc","netrad_toa","lwflx","zsml","shflx","k_m_troen","ps",
                "lwdn_sfc_clr","lwup_sfc_clr","swdn_sfc_clr","gust_uwc","swup_sfc_clr","temp",
                "tau_x","k_t_entr","z_full","feq_uwd","k_m_entr","ice_mask","olr_clr","t_surf",
                "swdn_toa_clr","ucomp","swup_toa_clr","alb_sfc","diff_t","t_ref","heat2d_rad",
                "pcb_uws","cqn_uwc","pct_uws","v_ref","pcb_uwd","heat2d_sw","z_pbl","z_Ri_025",
                "convect","convpbl_fq","radpbl_fq","entr_pbl_fq","average_T1","average_T2","average_DT","time_bnds"]
                '''
    temp = popMatrix(variableList)
    pca_temp = getPCA(temp)
    
    plt.plot(pca_temp)
    plt.show()
    
    
    '''
    badVars = ["swdn_sfc_ad", "cbmf_uwc","evap","wat_uw_col","tau_y","lwtoa_ad","IWP_all_clouds",
    "snow_tot","wat_ls_col","mc_full","tot_liq_amt","feq_uwc","liq_wat","vrad","uw_precip","LWP",
    "swup_sfc_ad","prec_uwd","qdt_conv","tot_ice_amt","tdt_dyn","snow_conv","cqi_uwc","enth_ls_col","precip",
    "b_star","lwsfc_ad","qdt_dyn","swup_toa_ad","q_ref","snow_ls","sphum","tdt_lw","prec_uwc","enth_uw_col","WP_all_clouds",
    "tdt_pevap_uwc","prec_uws","tdt_ls","prec_ls","wentr_pbl","lwtoa_ad_clr","wentr_rad",
    "cpool_uwc","qdt_ls","swup_toa_ad_clr","wat_conv_col","prec_conv","lwsfc_ad_clr","swdn_sfc_ad_clr",
    "cmf_uwc","swup_sfc_ad_clr","tdt_conv","omega","IWP","tdt_vdif","enth_conv_col","qdt_pevap_uwc",
    "tdt_sw","qdt_vdif","cqa_uwc","cqa_uws","udt_topo","ice_wat","cql_uwc","qdt_uwd","cqa_uwd",
    "cmf_uwd","cql_uws","cmf_uws","vdt_topo","entr_rad_fq","cqi_uwd","udt_vdif","cqi_uws","cql_uwd","vdt_vdif"]
    
    goodVarsFile = open("/home/Diyor.Zakirov/Documents/statVars.txt", 'w')
    for var in os.listdir("/work/Diyor.Zakirov/ensembleData/1"):
        if var.split(".")[0] not in badVars:
            goodVarsFile.write("\""+ var + "\",")
            
    goodVarsFile.close()
    '''

            
            
            