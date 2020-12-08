from localreg import *

import pandas as pd
import numpy as np
import econtools
import econtools.metrics as mt

from auxiliary.auxiliary_subset import *
from auxiliary.auxiliary_tables import *


##===============================
## For descriptive statistics table 

def descriptive_main(data):
    
    variables = data[["tk","ab","dist1","ecs1"]]
    table = pd.DataFrame()


    mean = variables.mean()
    table['Mean'] = mean.round(2)
    table['Standard Deviation'] = variables.std()
    table = table.astype(float).round(2)
    table['Variable'] = ["Capital transfers","Alignment","Regional incumbent’s bloc vote margin (v)", "Regional seat margin"]

    table = table.set_index('Variable')
    table['RDD frame'] = ["outcome variable","treatment","forcing variable","heterogeneity effects"]
    table['Definition'] = ["Capital transfers from the Regional government per capita",
                "Dummy equal to one if the party of the mayor is the same as that of the president of the AC",
              "% of votes cast at the local elections that have to be added (subtracted from) to the ideological bloc of the Regional incumbent to win (lose) a majority of seats in the local council",
              "Difference between the seat share of the parties in the regional government and the seat share of the main opposition parties in the previous regional election. This variable is demeaned. "]
    table.style.set_properties(subset= ['Definition'], **{'width-min': '300px'})

    return(table)



def descriptive_controls(data):

    variables = data[["debt","tipo","vcp","pob","density","pob_mes6591","pob_5_1491",
     "extr_noeu91","unempl","income","educ2","presscirc","regre",
     "regde","meanden","regterm"]]
    table = pd.DataFrame()    


    mean = variables.mean()
    table['Mean'] = mean.round(2)
    table['Standard Deviation'] = variables.std()
    table = table.astype(float).round(2)
    table['Variable'] = ["Debt burden","Property tax rate","Property value", "Population","Population density","% Old",
                         "% Young","% Immigrant","% Unemployed","Income indicator","% Educated","Press circulation",
                        "Regional revenues pc","Regional debt","Municipal density","Tenure in office"]
    table = table.set_index('Variable')

    table['Definition'] = ["Debt burden (capital, item 9 of the spending budget, + interest, item 3), as a share of current revenues",
                            "Nominal property tax rate (IBI), % on assessed property value",
                            "Assessed property value (thousands of EUR) per capita",
                            "Resident population",
                            "Population per square kilometer",
                            "% resident population older than 65 years",
                            "% resident population younger than 14 years",
                            "% resident population non-EU immigrant",
                            "% resident population unemployed",
                            "Residents’ income level, as estimated from objective indicators (e.g., cars, bank deposits, etc.)",
                            "Percentage of people with primary and secondary education. This variable is demeaned",
                            "Newspaper copies (at the province level) per 1000 inhabitants. This variable is demeaned",
                            "Current revenues per capita in each region. This variable is demeaned",
                            "Debt burden (capital, item 9 of the spending budget, + interest, item 3) as a share of current revenues. This variable is demeaned",
                            "Average population density (population per square kilometer) of the municipalities in each region. This variable is demeaned",
                            "Dummy equal to one if it is the regional incumbent was not in office the previous term"]
    table.style.set_properties(subset= ['Definition'], **{'width-min': '300px'})

    return(table)

    
def descriptive_confounders(data):

    variables = data[["ecs1","regre","regde","meanden","regterm","presscirc","educ2"]]
    table1 = pd.DataFrame()

    table1['Mean'] = variables.mean()
    table1['Standard Deviation'] = variables.std()
    table1 = table1.astype(float).round(2)
    table1['Confounders'] = ["Regional seat margin","Regional revenues pc","Regional debt", "Municipal density",
               "Tenure in office","Press circulation","% Educated"]

    table1 = table1.set_index('Confounders')
    table1['Definition'] = ["Gap btw the seat share of the parties in the regional government and the opposition parties",
                        "Current revenues per capita in each region",
                        "Debt burden as a share of current revenues",
                        "Average population density (population per km^2) of the municipalities in each region",
                        "Dummy equal to one if it is the regional incumbent was not in office the previous term",
                        "Newspaper copies (at the province level) per 1000 inhabitants",
                        "Percentage of people with primary and secondary education"]

    table1 = table1.round(2).style.set_properties(subset= ['Definition'], **{'width-min': '300px'})
    table1



##===============================
## For table 1


def first_stage_2SLS_global(data,cluster_var,covariates):

    # cluster_var = codiine -> for the coefficient
    # cluster_var = codccaa -> for the p_value 
    
    df = data[["ab","dab","dist1","dist2","vda","vda2","codiine","codccaa",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15","lpob", "density", "debt", "vcp", "tipo"]]
    
    y = 'ab'
    X = ['dab', 'dist1', 'dist2', 'vda','vda2',
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"]
    
    if covariates == 1:
        X = X + ["lpob", "density", "debt", "vcp", "tipo"]
    elif covariates == 0:
        X = X

    
    results = mt.reg(
    df,                     # DataFrame
    y,                      # Dependent var (string)
    X,                      # Independent var(s) (string or list of strings)
    cluster=cluster_var,     # Cluster var (string)
    addcons=True
    )
    
    return(results)



def first_stage_2SLS_local(data,bandwidth,cluster_var,covariates):
    
    # calculated optimal bandwidth:
    # 2h* = 0.386
    # h* = 0.193
    # h*/2 = 0.0965
    # h*/4 = 0.048    
    
    df = data[["ab","dab","dist1","dist2","vda","vda2","codiine","codccaa",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15","lpob", "density", "debt", "vcp", "tipo"]]
    df_h = df[abs(df.dist1)<bandwidth]
    
    y = 'ab'
    X = ['dab', 'dist1', 'vda',
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"]

    if covariates == 1:
        X = X + ["lpob", "density", "debt", "vcp", "tipo"]
    elif covariates == 0:
        X = X

    
    results = mt.reg(
    df_h,                  # DataFrame
    y,                      # Dependent var (string)
    X,                      # Independent var(s) (string or list of strings)
    cluster=cluster_var,     # Cluster var (string)
    addcons=True
    )
    
    return(results)



def second_stage_2SLS_global(data,cluster_var,covariates):
    
    df = data[["ab","dab","dist1","dist2","vsa","vsa2","vda","vda2","tk",
               "codiine","codccaa",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15","lpob", "density", "debt", "vcp", "tipo"]]
    
    y = "tk" # dependent var
    E = ["ab","vsa","vsa2"] # endo reg
    Z = ["dab","vda","vda2"] # instrumental
    X = ["dist1","dist2",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"] # exo reg
    if covariates == 1:
        X = X + ["lpob", "density", "debt", "vcp", "tipo"]
    elif covariates == 0:
        X = X

    
    results = mt.ivreg(df, y, E, Z, X, cluster=cluster_var, addcons=True)
    
    return(results)



def second_stage_2SLS_global_codiine(data,covariates):
    
    df = data[["ab","dab","dist1","dist2","vsa","vsa2","vda","vda2","tk",
               "codiine","codccaa",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15","lpob", "density", "debt", "vcp", "tipo"]]
    
    y = "tk" # dependent var
    E = ["ab","vsa","vsa2"] # endo reg
    Z = ["dab","vda","vda2"] # instrumental
    X = ["dist1","dist2",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"] # exo reg
    if covariates == 1:
        X = X + ["lpob", "density", "debt", "vcp", "tipo"]
    elif covariates == 0:
        X = X

    
    results = mt.ivreg(df, y, E, Z, X, cluster='codiine', addcons=True)
    
    return(results)



def second_stage_2SLS_global_codccaa(data,covariates):
    
    df = data[["ab","dab","dist1","dist2","vsa","vsa2","vda","vda2","tk",
               "codiine","codccaa",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15","lpob", "density", "debt", "vcp", "tipo"]]
    
    y = "tk" # dependent var
    E = ["ab","vsa","vsa2"] # endo reg
    Z = ["dab","vda","vda2"] # instrumental
    X = ["dist1","dist2",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"] # exo reg
    if covariates == 1:
        X = X + ["lpob", "density", "debt", "vcp", "tipo"]
    elif covariates == 0:
        X = X

    
    results = mt.ivreg(df, y, E, Z, X, cluster='codccaa', addcons=True)
    
    return(results)



def second_stage_2SLS_local(data,bandwidth,cluster_var,covariates):
    
    # calculated optimal bandwidth:
    # 2h* = 0.386
    # h* = 0.193
    # h*/2 = 0.0965
    # h*/4 = 0.048    
    
    df = data[["ab","dab","dist1","dist2","vsa","vsa2","vda","vda2","tk",
               "codiine","codccaa",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15","lpob", "density", "debt", "vcp", "tipo"]]
    df_h = df[abs(df.dist1)<bandwidth]
    
    y = "tk" # dependent var
    E = ["ab","vsa"] # endo reg
    Z = ["dab","vda"] # instrumental
    X = ["dist1",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"] # exo reg
    if covariates == 1:
        X = X + ["lpob", "density", "debt", "vcp", "tipo"]
    elif covariates == 0:
        X = X

    
    results = mt.ivreg(df_h, y, E, Z, X, cluster=cluster_var,addcons=True)
    
    return(results)




def table1(data,covariates):

    table = pd.DataFrame({'2nd_stage': [], 'Std.err(2)': [], 'P-Value(2)': [],
                          '1st_stage': [], 'Std.err(1)': [], 'P-Value(1)': [],
                          'Observations': []})

    case = ('Global','Local(bd=2h*)','Local(bd=h*)','Local(bd=h*/2)','Local(bd=h*/4)')
    table['RD'] = case
    table = table.set_index('RD')


    #Global estimate
    r1 = first_stage_2SLS_global(data,cluster_var = "codiine", covariates = covariates)
    p1 = first_stage_2SLS_global(data,cluster_var = "codccaa", covariates = covariates)
    #r2 = second_stage_2SLS_global(data,cluster_var = "codiine", covariates = covariates)
    r2 = second_stage_2SLS_global_codiine(data,covariates= covariates)
    #p2 = second_stage_2SLS_global(data,cluster_var = "codccaa", covariates = covariates)
    p2 = second_stage_2SLS_global_codccaa(data,covariates= covariates)
    rg = [r2.beta['ab'] ,r2.se['ab'], p2.pt['ab'], 
          r1.beta['dab'], r1.se['dab'], p1.pt['dab'], r2.N]
    table.loc["Global"] = rg

    #Local estimates
    local = ('Local(bd=2h*)','Local(bd=h*)','Local(bd=h*/2)','Local(bd=h*/4)')
    for a in local:
    
        if a == 'Local(bd=2h*)':
            bandwidth = 0.386
        elif a == 'Local(bd=h*)':
            bandwidth = 0.193
        elif a == 'Local(bd=h*/2)':
            bandwidth = 0.0965
        elif a == 'Local(bd=h*/4)':
            bandwidth = .048
        
        rslt1 = first_stage_2SLS_local(data,bandwidth = bandwidth,cluster_var = "codiine", covariates = covariates)
        pval1 = first_stage_2SLS_local(data,bandwidth = bandwidth,cluster_var = "codccaa", covariates = covariates)
        rslt2 = second_stage_2SLS_local(data, bandwidth = bandwidth,cluster_var = "codiine", covariates = covariates)
        pval2 = second_stage_2SLS_local(data, bandwidth = bandwidth,cluster_var = "codiine", covariates = covariates)
        result = [rslt2.beta['ab'] , rslt2.se['ab'], pval2.pt['ab'], 
                  rslt1.beta['dab'], rslt1.se['dab'], pval1.pt['dab'], rslt2.N]
        table.loc[a] = result
    return table





##===============================
## For table 2


def effect_of_competition_global(data):
    

    dca_abi = []
    dca_vsai = []
    dca_2vsai = []
    dca_dabi = []
    dca_vdai = []
    dca_2vdai = []

    for i in range(1,16):
        dca_abi.append("dca_ab"+str(i))
        dca_vsai.append("dca_vsa"+str(i))
        dca_2vsai.append("dca_2vsa"+str(i))
        dca_dabi.append("dca_dab"+str(i))
        dca_vdai.append("dca_vda"+str(i))
        dca_2vdai.append("dca_2vda"+str(i))
    
    
    regional_columns = dca_abi + dca_vsai + dca_2vsai + dca_dabi + dca_vdai + dca_2vdai
    other_columns = ["ab","dab","dist1","dist2","ecs1","vsa","vsa2","vda","vda2","tk","codiine",
                     "codccaa","esas1","vsa_ecs1", "vsa2_ecs1","edas1","vda_ecs1", "vda2_ecs1",
                    "dist1_ecs1", "dist2_ecs1",
                    "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
                    "dca11","dca12","dca13","dca14","dca15"]
    rc = data[regional_columns]
    oc = data[other_columns]
    df = pd.concat([rc,oc],  axis=1).reindex(rc.index)
    

    y = "tk" # dependent var
    
    e = dca_abi + dca_vsai + dca_2vsai
    e_ = ["esas1", "vsa_ecs1", "vsa2_ecs1"]    
    E = e + e_ # endo reg
    
    z = dca_dabi + dca_vdai + dca_2vdai
    z_ = ["edas1", "vda_ecs1", "vda2_ecs1"]
    Z = z + z_ # instrumental
    
    X = ["dist1_ecs1", "dist2_ecs1", "dist1", "dist2",  "ecs1",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"]
    
    cluster_var = 'codccaa'
    
    results = mt.ivreg(df, y, E, Z, X, cluster=cluster_var,addcons=True)
    
    return(results)




def effect_of_competition_local(data, bandwidth):
    

    dca_abi = []
    dca_vsai = []
    dca_dabi = []
    dca_vdai = []

    for i in range(1,16):
        dca_abi.append("dca_ab"+str(i))
        dca_vsai.append("dca_vsa"+str(i))
        dca_dabi.append("dca_dab"+str(i))
        dca_vdai.append("dca_vda"+str(i))
    
    
    regional_columns = dca_abi + dca_vsai + dca_dabi + dca_vdai 
    other_columns = ["ab","dab","dist1","dist2","ecs1","vsa","vsa2","vda","vda2","tk","codiine",
                     "codccaa","esas1","vsa_ecs1", "vsa2_ecs1","edas1","vda_ecs1", "vda2_ecs1",
                    "dist1_ecs1", "dist2_ecs1",
                    "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
                    "dca11","dca12","dca13","dca14","dca15"]
    rc = data[regional_columns]
    oc = data[other_columns]
    df = pd.concat([rc,oc],  axis=1).reindex(rc.index)
    df_h = df[abs(df.dist1)<bandwidth]
    

    y = "tk" # dependent var
    
    e = dca_abi + dca_vsai
    e_ = ["esas1", "vsa_ecs1"]    
    E = e + e_ # endo reg
    
    z = dca_dabi + dca_vdai
    z_ = ["edas1", "vda_ecs1"]
    Z = z + z_ # instrumental
    
    X = ["dist1_ecs1","dist1","ecs1",
         "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
         "dca11","dca12","dca13","dca14","dca15"]
    
    cluster_var = 'codccaa'
    
    results = mt.ivreg(df_h, y, E, Z, X, cluster=cluster_var,addcons=True)
    
    return(results)



def table2(data):

    table = pd.DataFrame({'Alignment * RSM': [], 'Std.err(2)': [], 'P-Value(2)': [],
                          'RSM': [], 'Std.err(1)': [], 'P-Value(1)': [],
                          'Observations': []})

    case = ('Global','Local(bd=2h*)','Local(bd=h*)','Local(bd=h*/2)','Local(bd=h*/4)')
    table['RD'] = case
    table = table.set_index('RD')


    #Global
    r1 = effect_of_competition_global(data)
    rg = [r1.beta['esas1'] , r1.se['esas1'], r1.pt['esas1'], 
          r1.beta['ecs1'], r1.se['ecs1'], r1.pt['ecs1'], r1.N]
    table.loc["Global"] = rg

    #Local
    local = ('Local(bd=2h*)','Local(bd=h*)','Local(bd=h*/2)','Local(bd=h*/4)')
    for a in local:
    
        if a == 'Local(bd=2h*)':
            bandwidth = 0.386
        elif a == 'Local(bd=h*)':
            bandwidth = 0.193
        elif a == 'Local(bd=h*/2)':
            bandwidth = 0.0965
        elif a == 'Local(bd=h*/4)':
            bandwidth = .048
        
        rslt1 = effect_of_competition_local(data,bandwidth = bandwidth)
        result = [rslt1.beta['esas1'] , rslt1.se['esas1'], rslt1.pt['esas1'], 
                  rslt1.beta['ecs1'], rslt1.se['ecs1'], rslt1.pt['ecs1'],rslt1.N]
        table.loc[a] = result

    
    return table



##===============================
## For table 4


def time_varying_covariates(data, add_columns, add_endo, add_inst ):
    

    dca_abi = []
    dca_vsai = []
    dca_dabi = []
    dca_vdai = []

    for i in range(1,16):
        dca_abi.append("dca_ab"+str(i))
        dca_vsai.append("dca_vsa"+str(i))
        dca_dabi.append("dca_dab"+str(i))
        dca_vdai.append("dca_vda"+str(i))
    
    
    regional_columns = dca_abi + dca_vsai + dca_dabi + dca_vdai 
    other_columns = ["ab","dab","dist1","ecs1","vsa","vda","tk","codiine",
                     "codccaa","esas1","vsa_ecs1", "edas1","vda_ecs1", 
                    "dist1_ecs1",
                    "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
                    "dca11","dca12","dca13","dca14","dca15"]
    all_other_columns = other_columns + add_columns
    rc = data[regional_columns]
    oc = data[all_other_columns]
    df = pd.concat([rc,oc],  axis=1).reindex(rc.index)
    df_h = df[abs(df.dist1)<0.193]
    

    y = "tk" # dependent var
    
    e = dca_abi + dca_vsai
    e_ = ["esas1", "vsa_ecs1"]    
    E = e + e_ + add_endo # endogenous regressor
    
    z = dca_dabi + dca_vdai
    z_ = ["edas1", "vda_ecs1"]
    Z = z + z_ + add_inst # instrumental variables
    
    X = ["dist1_ecs1","dist1","ecs1",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"]#exogeneous regressor
    
    cluster_var = 'codccaa'
    
    results = mt.ivreg(df_h, y, E, Z, X, cluster=cluster_var,addcons=True)
    
    return(results)


def time_varying_covariates_all(data, bandwidth):
    
    dca_abi = []
    dca_vsai = []
    dca_dabi = []
    dca_vdai = []

    for i in range(1,16):
        dca_abi.append("dca_ab"+str(i))
        dca_vsai.append("dca_vsa"+str(i))
        dca_dabi.append("dca_dab"+str(i))
        dca_vdai.append("dca_vda"+str(i))
    
    
    regional_columns = dca_abi + dca_vsai + dca_dabi + dca_vdai 
    other_columns = ["ab","dab","dist1","ecs1","vsa","vda","tk","codiine",
                     "codccaa","esas1","vsa_ecs1", "edas1","vda_ecs1", 
                    "dist1_ecs1",
                    "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
                    "dca11","dca12","dca13","dca14","dca15"]
    add_endo = ["resa","desa","denssa","termssa","presssa","educ2sa",
                "vsa_re","vsa_de","vsa_dens","vsa_te","vsa_pr","vsa_edu"]
    add_inst = ["reda","deda","densda","termsda","pressda","educ2da",
               "vda_re","vda_de","vda_dens","vda_te","vda_pr","vda_edu"]
    all_other_columns = other_columns + add_endo + add_inst
    
    
    rc = data[regional_columns]
    oc = data[all_other_columns]
    df = pd.concat([rc,oc],  axis=1).reindex(rc.index)
    df_h = df[abs(df.dist1)<bandwidth]
    

    y = "tk" # dependent var
    
    e = dca_abi + dca_vsai
    e_ = ["esas1", "vsa_ecs1"]    
    E = e + e_ + add_endo# endo reg
    
    z = dca_dabi + dca_vdai
    z_ = ["edas1", "vda_ecs1"]
    Z = z + z_ + add_inst # instrumental
    
    X = ["dist1_ecs1","dist1","ecs1",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"]#exo var
    
    cluster_var = 'codccaa'
    
    results = mt.ivreg(df_h, y, E, Z, X, cluster=cluster_var,addcons=True)
    
    return(results)


def table4(data):

    table = pd.DataFrame({'(1)': [], '(2)': [], '(3)': [],
                          '(4)': [], '(5)': [], '(6)': [],
                          '(7)': []})

    case = ('Alig * Reg. seat margin','standard error(0)','p-value(0)',
            'Alig * Revenue','standard error(1)','p-value(1)',
            'Alig * Debt','standard error(2)','p-value(2)',
            'Alig * Population density','standard error(3)','p-value(3)',
            'Alig * Tenure in Office','standard error(4)','p-value(4)',
            'Alig * Press', 'standard error(5)','p-value(5)',
            'Alig * Educated(%)', 'standard error(6)','p-value(6)',
            'Reg. seat margin', 'standard error(7)','p-value(7)',
            'Observations')
    table['Covariates'] = case
    table = table.set_index('Covariates')


    # build the contents of table 
    
    endo_1 = ["resa","vsa_re"]
    inst_1 = ["reda","vda_re"]
    colu_1 = endo_1 + inst_1
    rslt1 = time_varying_covariates(data, colu_1, endo_1 , inst_1)
    
    endo_2 = ["desa","vsa_de"]
    inst_2 = ["deda","vda_de"]
    colu_2 = endo_2 + inst_2
    rslt2 = time_varying_covariates(data, colu_2, endo_2 , inst_2)    
    
    endo_3 = ["denssa","vsa_dens"]
    inst_3 = ["densda","vda_dens"]
    colu_3 = endo_3 + inst_3
    rslt3 = time_varying_covariates(data, colu_3, endo_3 , inst_3)    
    
    endo_4 = ["termssa","vsa_te"]
    inst_4 = ["termsda","vda_te"]
    colu_4 = endo_4 + inst_4
    rslt4 = time_varying_covariates(data, colu_4, endo_4 , inst_4)        
    
    endo_5 = ["presssa","vsa_pr"]
    inst_5 = ["reda","vda_pr"]
    colu_5 = endo_5 + inst_5
    rslt5 = time_varying_covariates(data, colu_5, endo_5 , inst_5)
    
    endo_6 = ["educ2sa","vsa_edu"]
    inst_6 = ["educ2da","vda_edu"]
    colu_6 = endo_6 + inst_6
    rslt6 = time_varying_covariates(data, colu_6, endo_6 , inst_6)
    
    rslt7 = time_varying_covariates_all(data,bandwidth = 0.193)
        
    
    # fill the table with the contents
    
    table['(1)'] = [rslt1.beta['esas1'], rslt1.se['esas1'], rslt1.pt['esas1'],
                     rslt1.beta['resa'], rslt1.se['resa'], rslt1.pt['resa'],
                     ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                     rslt1.beta['ecs1'], rslt1.se['ecs1'], rslt1.pt['ecs1'],rslt1.N]
    
    table['(2)'] = [rslt2.beta['esas1'], rslt2.se['esas1'], rslt2.pt['esas1'],
                     ' ',' ',' ',rslt2.beta['desa'], rslt2.se['desa'], rslt2.pt['desa'],
                     ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                     rslt2.beta['ecs1'], rslt2.se['ecs1'], rslt2.pt['ecs1'],rslt2.N]
    
    table['(3)'] = [rslt3.beta['esas1'], rslt3.se['esas1'], rslt3.pt['esas1'],
                     ' ',' ',' ',' ',' ',' ',rslt3.beta['denssa'], rslt3.se['denssa'], rslt3.pt['denssa'],
                     ' ',' ',' ',' ',' ',' ',' ',' ',' ',
                     rslt3.beta['ecs1'], rslt3.se['ecs1'], rslt3.pt['ecs1'],rslt3.N]
    
    table['(4)'] = [rslt4.beta['esas1'], rslt4.se['esas1'], rslt4.pt['esas1'],
                     ' ',' ',' ',' ',' ',' ',' ',' ',' ',
                     rslt4.beta['termssa'], rslt4.se['termssa'], rslt4.pt['termssa'],
                     ' ',' ',' ',' ',' ',' ',
                     rslt4.beta['ecs1'], rslt4.se['ecs1'], rslt4.pt['ecs1'],rslt4.N]
    
    table['(5)'] = [rslt5.beta['esas1'], rslt5.se['esas1'], rslt5.pt['esas1'],
                     ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                     rslt5.beta['presssa'], rslt5.se['presssa'], rslt5.pt['presssa'],' ',' ',' ',
                     rslt5.beta['ecs1'], rslt5.se['ecs1'], rslt5.pt['ecs1'],rslt5.N]
    
    table['(6)'] = [rslt6.beta['esas1'], rslt6.se['esas1'], rslt6.pt['esas1'],
                     ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
                     rslt6.beta['educ2sa'], rslt6.se['educ2sa'], rslt6.pt['educ2sa'],
                     rslt6.beta['ecs1'], rslt6.se['ecs1'], rslt6.pt['ecs1'],rslt6.N] 
    
    table['(7)'] = [rslt7.beta['esas1'], rslt7.se['esas1'], rslt7.pt['esas1'],
                     rslt7.beta['resa'], rslt7.se['resa'], rslt7.pt['resa'],
                     rslt7.beta['desa'], rslt7.se['desa'], rslt7.pt['desa'],
                     rslt7.beta['denssa'], rslt7.se['denssa'], rslt7.pt['denssa'],
                     rslt7.beta['termssa'], rslt7.se['termssa'], rslt7.pt['termssa'],
                     rslt7.beta['presssa'], rslt7.se['presssa'], rslt7.pt['presssa'],
                     rslt7.beta['educ2sa'], rslt7.se['educ2sa'], rslt7.pt['educ2sa'],
                     rslt7.beta['ecs1'], rslt7.se['ecs1'], rslt7.pt['ecs1'],rslt7.N]    
    
    return(table)




##===========================================
## For balance test(discontinuity test) table
##===========================================

def Balance_test(data,bandwidth,confounder,cluster_var):
    
    # calculated optimal bandwidth:
    # 2h* = 0.386
    # h* = 0.193
    # h*/2 = 0.0965
    # h*/4 = 0.048    
    
    df = data[["debt", "tipo", "vcp", "pob",  "density", "pob_mes6591", 
               "pob_5_1491", "extr_noeu91", "unempl", "income", "presscirc",
               "regre", "regde", "meanden", "educ2", "regterm", "ecs1",
               "dab", "dist1", "vda", "codiine", "codccaa","cprov",
              "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"]]
    
    df_h = df[abs(df.dist1)<bandwidth]
    
    y = confounder
    X = ['dab', 'dist1', 'vda', "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"]
    
    results = mt.reg(
    df_h,                  # DataFrame
    y,                      # Dependent var (string)
    X,                      # Independent var(s) (string or list of strings)
    cluster=cluster_var,     # Cluster var (string) 
    addcons=True
    )
    
    return(results)

    

def Balance_test_table(data):
    
    
    # set the confounders and corresponding optimal bandwidth
    combine = {"debt": 0.219, "tipo":0.171, "vcp":0.216, "pob":0.197,  "density":0.171, "pob_mes6591":0.185,
               "presscirc":0.253, "regre":0.247, "regde":0.245, "meanden":0.275, "educ2":0.347, "regterm":0.287, 
               "ecs1":0.247, "pob_5_1491":0.183, "extr_noeu91":0.223, "unempl":0.237, "income":0.229}
    temp_i = ["debt", "tipo", "vcp", "pob",  "density", "pob_mes6591", 
           "pob_5_1491", "extr_noeu91", "unempl", "income","presscirc",
         "regre", "regde", "meanden", "educ2", "regterm", "ecs1"]

        
    
    # create a table and temporarily set bandwidth value as index 
    table = pd.DataFrame({'Variable': [], 'Coef.': [], 'SE': [],
                          'P-value': [], 'Bandwidth': [], 'Observations': []})
    table['Variable'] = temp_i
    table = table.set_index('Variable')

    
    # regression and result 
    for i,j in combine.items():
        
        data = data
        confounder = i
        bandwidth = j
        
        if j < 0.24:
            cluster_var = 'codiine'
        elif j == 0.253:
            cluster_var = 'cprov'
        else:
            cluster_var = 'codccaa'
        
        rl = Balance_test(data,bandwidth,confounder,cluster_var)
        rg = [rl.beta['dist1'] , rl.se['dist1'], rl.pt['dist1'], j, rl.N]
        table.loc[i] = rg

    table['Variable'] = ["Debt burden","Property tax rate","Property value","Population",
                        "Population density","% Old","% Young","% Immigrant","% Unemployed",
                        "Income indicator","Press circulation p.c.","Regional revenues p.c",
                        "Regional debt","Municipal density","Education","Tenure in office",
                        "Regional seat margin"]
    

    
    return(table)




##===========================================
## Robustness Check
##===========================================

def first_stage_2SLS_order(data,order,bandwidth):

    
    df = data
    
    if bandwidth < 1:
        df_h = df[abs(df.dist1)<bandwidth]
    elif bandwidth == 1:
        df_h = df
            
    
    y = 'ab'
    X = ['dab',"dca2","dca3","dca4","dca5","dca6","dca7","dca8",
         "dca9","dca10","dca11","dca12","dca13","dca14","dca15"]
    
    if order == 1:
        add = ['dist1','vda']
    elif order == 2:
        add = ['dist1','dist2','vda','vda2']
    elif order == 3:
        add = ['dist1','dist2','dist3','vda','vda2','vda3'] 
        
    X = X + add
  
    results = mt.reg(
    df_h,                     # DataFrame
    y,                      # Dependent var (string)
    X,                      # Independent var(s) (string or list of strings)
    cluster='codiine',     # Cluster var (string)
    addcons=True
    )
    
    return(results)


def second_stage_2SLS_global(data,order,bandwidth):
    
    df = data
    
    if bandwidth < 1:
        df_h = df[abs(df.dist1)<bandwidth]
    elif bandwidth == 1:
        df_h = df        
    
    y = "tk" # dependent var
    E = ["ab"] # endo reg
    Z = ["dab"] # instrumental
    X = ["dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9",
         "dca10","dca11","dca12","dca13","dca14","dca15"] # exo reg
    
    if order == 1:
        add_endo = ['vsa']
        add_inst = ['vda']
        add_exo = ['dist1']
    elif order == 2:
        add_endo = ['vsa','vsa2']
        add_inst = ['vda','vda2']
        add_exo = ['dist1','dist2']
    elif order == 3:
        add_endo = ['vsa','vsa2','vsa3']
        add_inst = ['vda','vda2','vda3']
        add_exo = ['dist1','dist2','dist3'] 
    
    E = E + add_endo
    Z = Z + add_inst
    X = X + add_exo
            
    results = mt.ivreg(df_h, y, E, Z, X, cluster='codiine',addcons=True)
    
    return(results)



def table_Poly_Robust(data,bandwidth):
    
    
    # construct the table
    table = pd.DataFrame({'(1)': [], '(2)': [], '(3)': []})

    case = ('Second Stage','Alignment','se(2)',
            'p-value(2)','First Stage','Reg vote margin','se(1)',
            'p-value(1)','Polynomial Order','Observations')
    table[' '] = case
    table = table.set_index(' ')
    
    # regression results
    subset = subset_for_Poly_Robust(data)
    rslt_11 = first_stage_2SLS_order(data=subset,order=1,bandwidth = bandwidth)
    rslt_12 = first_stage_2SLS_order(data=subset,order=2,bandwidth= bandwidth)
    rslt_13 = first_stage_2SLS_order(data=subset,order=3,bandwidth= bandwidth)
    rslt_21 = second_stage_2SLS_global(data=subset,order=1,bandwidth= bandwidth)
    rslt_22 = second_stage_2SLS_global(data=subset,order=2,bandwidth= bandwidth)
    rslt_23 = second_stage_2SLS_global(data=subset,order=3,bandwidth= bandwidth)
     
    #fill the table with the contents
    table['(1)'] = [' ', rslt_21.beta['ab'],rslt_21.se['ab'],rslt_21.pt['ab'],
                   ' ',rslt_11.beta['dab'],rslt_11.se['dab'],rslt_11.pt['dab'],'1',rslt_11.N]
    table['(2)'] = [' ', rslt_22.beta['ab'],rslt_22.se['ab'],rslt_22.pt['ab'],
                   ' ',rslt_12.beta['dab'],rslt_12.se['dab'],rslt_12.pt['dab'],'2',rslt_12.N]
    table['(3)'] = [' ', rslt_23.beta['ab'],rslt_23.se['ab'],rslt_23.pt['ab'],
                   ' ',rslt_13.beta['dab'],rslt_13.se['dab'],rslt_13.pt['dab'],'3',rslt_13.N] 

    return(table)



def robust_bandwidth_LATE(data):

    table = pd.DataFrame({'2nd_stage': [], 'Std.err(2)': [], 'P-Value(2)': [],
                          '1st_stage': [], 'Std.err(1)': [], 'P-Value(1)': [],
                          'Observations': []})

    case = (0.11,0.13,0.15,0.17,0.193,0.21,0.23,0.25,0.27,0.29)
    table['Bandwidth'] = case
    table = table.set_index('Bandwidth')

    #Local
    for i in case:
        bandwidth = i
        rslt1 = first_stage_2SLS_local(data,bandwidth = bandwidth,cluster_var = "codiine",covariates = 0)
        rslt2 = second_stage_2SLS_local(data, bandwidth = bandwidth,cluster_var = "codiine",covariates = 0)
        result = [rslt2.beta['ab'] , rslt2.se['ab'], rslt2.pt['ab'], 
                  rslt1.beta['dab'], rslt1.se['dab'], rslt1.pt['dab'], rslt2.N]
        table.loc[i] = result
        
    return (table)



def robust_bandwidth_HLATE(data):

    table = pd.DataFrame({'Alignment * RSM': [], 'Std.err(2)': [], 'P-Value(2)': [],
                          'RSM': [], 'Std.err(1)': [], 'P-Value(1)': [],
                          'Observations': []})

    case = (0.11,0.13,0.15,0.17,0.193,0.21,0.23,0.25,0.27,0.29,0.31,0.33,0.35,0.386,0.4)
    table['Bandwidth'] = case
    table = table.set_index('Bandwidth')

    #Local
    for i in case:
        bandwidth = i
        rslt1 = effect_of_competition_local(data,bandwidth = bandwidth)
        result = [rslt1.beta['esas1'] , rslt1.se['esas1'], rslt1.pt['esas1'], 
                  rslt1.beta['ecs1'], rslt1.se['ecs1'], rslt1.pt['ecs1'],rslt1.N]
        table.loc[i] = result
        
    return (table)




def LATE_for_alternative_align(data,bandwidth,endo,cluster_var):
      
    """
    Compare LATE obtained by different alternative dummy variables which represent
     more comprehensible alignement status

    """

    
    df = subset_for_alternative_align(data) # Generate subset
    df = df.dropna()
    df_h = df[abs(df.dist1)<bandwidth] # Set optimal bandwidth
    

    """
    Take the result of the second stage of Instrument Regression
    
    """
    y = "tk" # dependent var
    E = endo # endo reg
    Z = ["dab","vda"] # instrumental
    X = ["dist1",
         "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
              "dca11","dca12","dca13","dca14","dca15"] # exo reg
    
    results = mt.ivreg(df_h, y, E, Z, X, cluster=cluster_var,addcons=True)
    
    return(results)



def HLATE_for_alternative_align(data, bandwidth, alter):

    """
    Compare HLATE obtained by different alternative dummy variables which represent
     more comprehensible alignement status

    """


    # add regional fixed effects as controls 
    dca_bcdi = []
    dca_vsbcdi = []
    dca_bloci = []
    dca_vsbloci = []
    dca_dabi = []
    dca_vdai = []

    for i in range(1,16):
        dca_bcdi.append("dca_bcd"+str(i))
        dca_vsbcdi.append("dca_vsbcd"+str(i))
        dca_bloci.append("dca_bloc"+str(i))
        dca_vsbloci.append("dca_vsbloc"+str(i))
        dca_dabi.append("dca_dab"+str(i))
        dca_vdai.append("dca_vda"+str(i))
    
    
    regional_columns = dca_bcdi + dca_vsbcdi + dca_bloci + dca_vsbloci + dca_dabi + dca_vdai     
    
    rc = data[regional_columns]
    oc = subset_for_alternative_align(data)
    df = pd.concat([rc,oc],  axis=1).reindex(rc.index)
    df = df.dropna()
    df_h = df[abs(df.dist1)<bandwidth]
    

    # put different endogenous variables to different alternative regression model
    if alter == 'part':        
        E = dca_bcdi + dca_vsbcdi + ["esas1_bis","vsbcd_ecs1"]
       
    elif alter == 'bloc':
        E = dca_bloci + dca_vsbloci + ["esas1_bisbis", "vsbloc_ecs1" ]
        
    y = 'tk'
    Z = dca_dabi + dca_vdai + ["edas1", "vda_ecs1"]
    X = ["dist1_ecs1","dist1","ecs1",
        "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
        "dca11","dca12","dca13","dca14","dca15"]
    
    cluster_var = 'codccaa'
    results = mt.ivreg(df_h, y, E, Z, X, cluster=cluster_var,addcons=True)
    return(results)



def table_alternative_alignment(data, data2):
    
    table = pd.DataFrame({'LATE': [], 'SE(1)': [], 'P-val(1)': [],
                          'HLATE(Align*RSM)': [], 'SE(2)': [], 'P-val(2)': [],
                          'RSM': [], 'SE(3)': [], 'P-val(3)': [], 'Bandwidth':[],
                          'Obs' : []})

    case = ('Alignment','Partner-Align','Bloc-Align')
    table['RD'] = case
    table = table.set_index('RD')
    
    # The First row shows the estimates of original alignment dummy
    align1 = second_stage_2SLS_local(data, bandwidth = 0.193, cluster_var = "codiine", covariates = 0)
    align2 =  effect_of_competition_local(data2, bandwidth = 0.193)
    result_align = [align1.beta['ab'] , align1.se['ab'], align1.pt['ab'], 
                    align2.beta['esas1'], align2.se['esas1'], align2.pt['esas1'],
                    align2.beta['ecs1'], align2.se['ecs1'], align2.pt['ecs1'], 0.193, align2.N]
    table.loc['Alignment'] = result_align
    
    # The second row shows the estimates of partner-alignment dummy
    part1 = LATE_for_alternative_align(data,bandwidth = 0.225 ,endo = ['abcd', 'vsbcd'],cluster_var = 'codiine')
    part2 = HLATE_for_alternative_align(data,bandwidth = 0.225, alter = 'part')
    result_part = [part1.beta['abcd'] , part1.se['abcd'], part1.pt['abcd'], 
                      part2.beta['esas1_bis'], part2.se['esas1_bis'], part2.pt['esas1_bis'],
                      part2.beta['ecs1'], part2.se['ecs1'], part2.pt['ecs1'], 0.225, part2.N]
    table.loc['Partner-Align'] = result_part 
    
    # The third row shows the estimates of bloc-alignment dummy
    bloc1 = LATE_for_alternative_align(data,bandwidth = 0.219 ,endo = ['bloc', 'vsbloc'],cluster_var = 'codiine')
    bloc2 = HLATE_for_alternative_align(data,bandwidth = 0.219, alter = 'bloc')
    result_bloc = [bloc1.beta['bloc'] , bloc1.se['bloc'], bloc1.pt['bloc'], 
                      bloc2.beta['esas1_bisbis'], bloc2.se['esas1_bisbis'], bloc2.pt['esas1_bisbis'],
                      bloc2.beta['ecs1'], bloc2.se['ecs1'], bloc2.pt['ecs1'], 0.219, bloc2.N]
    table.loc['Bloc-Align'] = result_bloc 
    
    return table
    
