from localreg import *

import pandas as pd
import numpy as np
import scipy.interpolate

from auxiliary.auxiliary_subset import *



##===============================
## Subset for Figure 1 and 4 


def subset_for_figure(data):

    df = data[["ab", "dist1", "dif", "tk", "debt","tipo","vcp","pob","density","pob_mes6591","pob_5_1491",
                  "extr_noeu91","unempl","income","localp","educ2","presscirc","regre","regde","meanden",
                  "regterm","ecs1","above","bloc","abcd"]]
    bins = np.linspace(-1, 1, num=41)
    df["bin"] = pd.cut(df["dist1"], bins, labels=False, include_lowest = True)
    df.sort_values(by="bin", inplace=True)

    return (df)



def append_subset_for_figure(data):

    df = subset_for_figure(data)
    bin2s = np.linspace(-12, 12, num=25)
    df["bin2"] = pd.cut(df["dif"], bin2s, labels=False, include_lowest = True)
    df.sort_values(by="bin2", inplace=True)

    ab = df.groupby('bin')['dist1']
    df['av_dist'] = ab.transform('mean')

    cd = df.groupby('bin2')['dif']
    df['av_dif'] = cd.transform('mean')

    ef = df.groupby('bin')['ab']
    df['av_alig_ab'] = ef.transform('mean')

    gh = df.groupby('bin2')['ab']
    df['av_alig_ab2'] = gh.transform('mean')

    ij = df.groupby('bin')['tk']
    df['av_tk'] = ij.transform('mean')

    return (df)  




def bootstrap_left(boot, y_var, x_var):

    """
    return: find the value of new point which return a smooth regression
            function using interpolation
    """

    # y_var = 'tk'
    # x_var = 'dist1'
    
    data1 = boot
    y = data1[data1.dist1<0].loc[:,y_var].to_numpy()
    x = data1[data1.dist1<0].loc[:,x_var].to_numpy()
    samples = np.random.choice(len(x), 50, replace=True)
    xgrid = np.linspace(x.min(),x.max())
    
    y_s = y[samples]
    x_s = x[samples]

    y_sm = localreg(x_s, y_s, x0=None, degree=1, kernel=epanechnikov, frac=None)

    # regularly sample it onto the grid
    y_grid = scipy.interpolate.interp1d(x_s, y_sm, 
                                        fill_value='extrapolate')(xgrid)
    return y_grid


def bootstrap_right(boot, y_var, x_var):

    """
    return: find the value of new point which return a smooth regression
            function using interpolation
    """

    # y_var = 'tk'
    # x_var = 'dist1'
    
    data1 = boot
    y = data1[data1.dist1>0].loc[:,y_var].to_numpy()
    x = data1[data1.dist1>0].loc[:,x_var].to_numpy()
    samples = np.random.choice(len(x), 50, replace=True)
    xgrid = np.linspace(x.min(),x.max())
    
    y_s = y[samples]
    x_s = x[samples]

    y_sm = localreg(x_s, y_s, x0=None, degree=1, kernel=epanechnikov, frac=None)

    # regularly sample it onto the grid
    y_grid = scipy.interpolate.interp1d(x_s, y_sm, 
                                        fill_value='extrapolate')(xgrid)
    return y_grid


##===============================
##  Subset for Figure 2

def subset_for_figure2(data):


    forcing_variable = data[["dist1"]]
    forc_var = forcing_variable.dropna() # drop missing values
    forc_var_nu = forc_var.to_numpy() # convert from dataframe to array

    return forc_var_nu 


##===============================
## Subset for Figure 3


def subset_for_figure3(data):

    data2 = subset_for_figure(data)
    data2['pob'] = data2['pob']/1000

    limit = np.percentile(data2.loc[:, "pob"], 95)

    blank = []
    for row in data2['pob']:
        if row > limit:
            blank.append(np.nan)
        else:
            blank.append(row)
        
    data2["pob"] = blank
    data2 = data2.dropna()

    for i in ["dist1","debt","tipo","vcp","pob","density","pob_mes6591","pob_5_1491",
          "extr_noeu91","unempl","income","localp","educ2","presscirc",
          "regre","regde","meanden","regterm","ecs1"]:
        ab = data2.groupby('bin')[i]
        data2['av_'+i] = ab.transform('mean')

    return (data2)
    


def for_cov(abc):
    

    blank = []
    for i in abc:
        blank.append('av_'+i)
    title = ["Debt burden", "Property tax rate","Property value","Population(thousands)",
             "Population density","%Old","%Young","%Immigrant","%Unemployed","Income indicator",
             "%Educated","Press circulation","Regional revenues per capita","Regional debt",
             "Municipal density","Tenure in office"]

    y_lower_bound = [0,0.4,15,2,100,0.12,0.18,0,5,0.8,-0.5,-20,-300,-2,-150,0]
    y_upper_bound = [0.12,0.8,30,12,1100,0.22,0.26,0.03,7,1.1,1,30,300,4,250,0.7]
    
    covplot = {'covar':abc,'av_cov':blank,'title':title, 'y_low':y_lower_bound, 'Y_upp':y_upper_bound}
    covplot = pd.DataFrame.from_dict(covplot)
    return (covplot)





##===============================
## Subset for Figure 5


"""

 For creating two subsets, low competiton group and high competion group
 If low_comp == 1, low competition
 If low_comp == 0, high competition

"""


def subset_figure5 (data, low_comp):

    comp = data[["ab","dist1","tk","ecs1","above"]]
    comp_group = comp[comp.above == low_comp].loc[:,:]

    bins = np.linspace(-1, 1, num=41)
    comp_group["bin"] = pd.cut(comp_group["dist1"], bins, labels=False,
                               include_lowest = True)
    comp_group.sort_values(by="bin", inplace=True)
    return (comp_group)




def append_av_for_figure5(data, low_comp):

    comp_group = subset_figure5(data, low_comp)
    
    for i in ["ab","dist1","tk","ecs1"]:
        ab = comp_group.groupby('bin')[i]
        comp_group['av_'+i] = ab.transform('mean')

        
    return (comp_group)




##===============================
##  Subset for Figure 6

def subset_figure6(data):
    data1 = subset_for_figure(data)
    data1 = data1[["dist1","ecs1","bin"]]

    ab = data1.groupby('bin')['dist1']
    data1['av_dist1'] = ab.transform('mean')

    cd = data1.groupby('bin')['ecs1']
    data1['av_ecs1'] = cd.transform('mean')
    
    return (data1)




##===============================
##  Subset for Robustness Check


def subset_for_alternative_align(data):
    df = data
    df = df[["abcd","bloc","dist1","compreg1","ab","dab","vsa","vda","vsbloc","vsbcd",
             "dab_bis","dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
             "dca11","dca12","dca13","dca14","dca15","codiine","codccaa","tk"]]
    c = df["compreg1"].mean()
    df["ecs1"] = df["compreg1"] - c
    df["esas1"] = df["ecs1"] * df["ab"]
    df["edas1"] = df["ecs1"] * df["dab"]
    df["vsa_ecs1"] = df['vsa'] * df['ecs1']
    df['vda_ecs1'] = df['vda'] * df['ecs1']
    df['dist1_ecs1'] = df['dist1'] * df['ecs1']
    df['esas1_bis'] = df['ecs1'] * df['abcd']
    df['vsbcd_ecs1'] = df['vsbcd'] * df['ecs1']
    df['esas1_bisbis'] = df['ecs1'] * df['bloc']
    df['edas1_bis'] = df['ecs1'] * df['dab_bis']
    df['vsbloc_ecs1'] = df['vsbloc'] * df['ecs1']
    return(df)



def subset_for_alter_figure(data):

    df = data[["ab", "dist1", "dif", "tk","bloc","abcd"]]
    bins = np.linspace(-1, 1, num=41)
    df["bin"] = pd.cut(df["dist1"], bins, labels=False, include_lowest = True)
    df.sort_values(by="bin", inplace=True)
    
    for i in ["ab","abcd","bloc"]:
        ab = df.groupby('bin')[i]
        df['av_alig_'+i] = ab.transform('mean')

    return (df)    
    



def subset_for_Poly_Robust(data):
    
    temp = data[["ab","dab","dist1","dist2","vsa","vsa2","vda","vda2","codiine","codccaa",
            "dca2","dca3","dca4","dca5","dca6","dca7","dca8","dca9","dca10",
            "dca11","dca12","dca13","dca14","dca15","tk"]].dropna()
    
    dist3 = []
    vda3 = []
    vsa3 = []
    for i in temp.index:
        a = temp.loc[i,"dist1"]
        b = a**3
        c = temp.loc[i,"dab"]*b
        d = temp.loc[i,"ab"]*b
        dist3.append(b)
        vda3.append(c)
        vsa3.append(d)
    
    temp["dist3"] = dist3
    temp["vda3"] = vda3
    temp["vsa3"] = vsa3
    
    return(temp)




def subset_figure_robust(data,low_comp,left):
    
    comp = data[["above","f34142_c6_c6","left_auto","dist1","ab","ecs1"]].dropna()
    comp_group = comp.loc[(comp["above"] == low_comp) & (comp['left_auto'] == left)]


    bins = np.linspace(-1, 1, num=41)
    comp_group["bin"] = pd.cut(comp_group["dist1"], bins, labels=False,
                               include_lowest = True)
    comp_group.sort_values(by="bin", inplace=True)

    return (comp_group)

    


def append_av_for_figure_robust(data,low_comp,left):

    comp_group = subset_figure_robust(data,low_comp,left)
    
    for i in ["ab","dist1","f34142_c6_c6","ecs1"]:
        ab = comp_group.groupby('bin')[i]
        comp_group['av_'+i] = ab.transform('mean')        
    return (comp_group)



def subset_for_alter_figure(data):

    df = data[["ab", "dist1", "dif", "tk","bloc","abcd"]]
    bins = np.linspace(-1, 1, num=41)
    df["bin"] = pd.cut(df["dist1"], bins, labels=False, include_lowest = True)
    df.sort_values(by="bin", inplace=True)
    
    for i in ["ab","abcd","bloc","dist1"]:
        ab = df.groupby('bin')[i]
        if i == "dist1":
            df['av_dist'] = ab.transform('mean')
        else:
            df['av_alig_'+i] = ab.transform('mean')

    return (df)
