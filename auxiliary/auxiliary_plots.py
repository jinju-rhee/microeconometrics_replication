from localreg import *

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels as sm
import seaborn as sns

from auxiliary.auxiliary_subset import *
from auxiliary.auxiliary_plots import *
from auxiliary.auxiliary_tables import *


##=========================
## Figure 1



def plot_figure1(data,boot_figure1):

    """
     argument : data = data
                boot_figure1 = dataframe for bootstraping 
        

     return: discontinuity on alignment when forcing variable is
            regional incumbent's seat margin(left)  and
            regional incumbent's vote margin(right) 
    """


    data1 = append_subset_for_figure(data)
    x11 = data1[(data1.dif < 0) & (data.dif >= -9)].loc[:, 'av_dif']
    y11 = data1[(data1.dif < 0) & (data.dif >= -9)].loc[:, 'av_alig_ab2']
    x22 = data1[(data1.dif > 0) & (data.dif <= 9)].loc[:, 'av_dif']
    y22 = data1[(data1.dif > 0) & (data.dif <= 9)].loc[:, 'av_alig_ab2']

    plt.figure(figsize=(17, 4.5))
    plt.subplot(1, 2, 1)
    plt.grid(True)
    plt.xlim(-9, 9)
    plt.ylim(-0.1, 1.1)
    plt.xticks(np.arange(-9, 9, step=1))
    plt.axvline(x=0, color='r')   
    plt.scatter(x11, y11, s=20, facecolors='none', edgecolors='b')
    plt.scatter(x22, y22, s=20, facecolors='none', edgecolors='b')
    plt.xlabel('Regional incumbents bloc seat margin',fontsize = 13)
    plt.ylabel('Alignment Regional-Local',fontsize = 13)
    plt.title('Alignment versus Seat Margins',fontsize = 13)


    x1 = data1[(data1.dist1 < 0) & (data.dist1 > -0.6)].loc[:,'av_dist']
    y1 = data1[(data1.dist1 < 0) & (data.dist1 > -0.6)].loc[:,'av_alig_ab']
    x2 = data1[(data1.dist1 > 0) & (data.dist1 < 0.6)].loc[:,'av_dist']
    y2 = data1[(data1.dist1 > 0) & (data.dist1 < 0.6)].loc[:,'av_alig_ab']
    x3 = data1[data1.dist1<0].loc[:,'dist1'].to_numpy()    
    y3 = data1[data1.dist1<0].loc[:,'ab'].to_numpy()
    x4 = data1[data1.dist1>0].loc[:,'dist1'].to_numpy()
    y4 = data1[data1.dist1>0].loc[:,'ab'].to_numpy()
    
    x3grid = np.linspace(x3.min(),x3.max())
    x4grid = np.linspace(x4.min(),x4.max())
    
    K = 100
    left = np.stack([bootstrap_left(boot = boot_figure1, y_var = 'ab', x_var = 'dist1') for k in range(K)]).T
    right = np.stack([bootstrap_right(boot = boot_figure1, y_var = 'ab', x_var = 'dist1') for k in range(K)]).T
    
    mean_left = np.nanmean(left, axis=1)
    stderr_left = scipy.stats.sem(left, axis=1)
    stderr_left = np.nanstd(left, axis=1, ddof=0)    
    mean_right = np.nanmean(right, axis=1)
    stderr_right = scipy.stats.sem(right, axis=1)
    stderr_right = np.nanstd(right, axis=1, ddof=0)
    
    
    plt.subplot(1, 2, 2)
    plt.grid(True)
    plt.axvline(x=0, color='r')
    plt.xlim(-0.51, 0.51)
    plt.xticks([-0.5, 0, 0.5])
    plt.ylim(-0.05, 1.05)
    plt.scatter(x1, y1, s=30, facecolors='none', edgecolors='black')
    plt.scatter(x2, y2, s=30, facecolors='none', edgecolors='black')
    plt.fill_between(x3grid, mean_left-1.96*stderr_left, mean_left+1.96*stderr_left, alpha=0.25)
    plt.fill_between(x4grid, mean_right-1.96*stderr_right, mean_right+1.96*stderr_right, alpha=0.25)    
    plt.plot(x3grid, mean_left, color='green')
    plt.plot(x4grid, mean_right, color='green')
    plt.xlabel('Regional incumbents bloc vote margin',fontsize = 13)
    plt.ylabel('Alignment Regional-Local',fontsize = 13)
    plt.title('Alignment versus Vote Margins',fontsize = 13)
    plt.show()



##=========================
## Figure 2



def plot_histogram(data):

    """
    return: histogram of forcing variable to check its manipulation
    
    """


    x = subset_for_figure2(data) # forcing variable in array

    bins_ten = np.linspace(-1, 1, 20) # when Band width is 10%
    bins_five = np.linspace(-1, 1, 40) # when Band width is 5%
    bins_two = np.linspace(-1, 1, 80) # when Band width is 1%

    plt.figure(figsize=[8,6])
    plt.grid(True)
    plt.xlim(-1.1, 1.1)
    plt.ylim(-0.1, 900)
    plt.xticks(np.arange(-1, 1, step=0.5))
    plt.axvline(x=0, color='black')   
    plt.xlabel("Regional incumbent's bloc vote margin",fontsize = 13)
    plt.ylabel('Frequency',fontsize = 13)
    plt.title('Histogram',fontsize = 13)

    plt.hist(x, bins = bins_ten, range = [-1,1], facecolor='g', alpha=0.75, label = 'Binwidth 0.1')
    plt.hist(x, bins = bins_five, range = [-1,1], facecolor='b', alpha=0.75, label = 'Binwidth 0.05')
    plt.hist(x, bins = bins_two, range = [-1,1], facecolor='r', alpha=0.75, label = 'Binwidth 0.01')
    plt.legend(loc='best')

    plt.show()  


##=========================
## Figure 4



def plot_figure4 (data,boot_figure4):

    """
    argument: boot_figure4 = dataframe for bootstraping  


    return: visualization of discontinuity on transfer at the cutoff
    
    """

    data1 = append_subset_for_figure(data)
    x11 = data1[(data1.dist1 < 0)].loc[:, 'av_dist']
    y11 = data1[(data1.dist1 < 0)].loc[:, 'av_tk']
    x22 = data1[(data1.dist1 > 0)].loc[:, 'av_dist']
    y22 = data1[(data1.dist1 > 0)].loc[:, 'av_tk']
    x3 = data1[data1.dist1<0].loc[:,'dist1'].to_numpy()    
    y3 = data1[data1.dist1<0].loc[:,'tk'].to_numpy()
    x4 = data1[data1.dist1>0].loc[:,'dist1'].to_numpy()
    y4 = data1[data1.dist1>0].loc[:,'tk'].to_numpy()

    x3grid = np.linspace(x3.min(),x3.max())
    x4grid = np.linspace(x4.min(),x4.max())
    
    K = 100
    left = np.stack([bootstrap_left(boot = boot_figure4, y_var = 'tk', x_var = 'dist1') for k in range(K)]).T
    right = np.stack([bootstrap_right(boot = boot_figure4, y_var = 'tk', x_var = 'dist1') for k in range(K)]).T
    
    mean_left = np.nanmean(left, axis=1)
    stderr_left = scipy.stats.sem(left, axis=1)
    mean_right = np.nanmean(right, axis=1)
    stderr_right = scipy.stats.sem(right, axis=1)

    plt.figure(figsize=[7.5,5.5])
    plt.grid(True)
    plt.axvline(x=0, color='r')
    plt.xlim(-0.51, 0.51)
    plt.xticks([-0.5, 0, 0.5])
    plt.ylim(70, 190)
            
    plt.scatter(x11, y11, s=30, facecolors='none', edgecolors='black')
    plt.scatter(x22, y22, s=30, facecolors='none', edgecolors='black')
    
    plt.plot(x3grid, mean_left-1.96*stderr_left, 'b--')
    plt.plot(x3grid, mean_left+1.96*stderr_left, 'b--')
    plt.plot(x4grid, mean_right-1.96*stderr_right, 'b--')
    plt.plot(x4grid, mean_right+1.96*stderr_right, 'b--') 

    plt.plot(x3grid, mean_left, color='green')
    plt.plot(x4grid, mean_right, color='green')
    
    plt.xlabel("Regional incumbent's bloc vote margin",fontsize = 13)
    plt.ylabel("Regional transfers",fontsize = 13)


##=========================
## Figure 3


def plot_Covariates_Continuity(data, boot_fig_cov, y_var_sca, y_var_pre, y_lowerb, y_upperb, plot_title):

    """
    argument: boot_fig_cov = dataframe for bootstraping
              y_var_sca = covariate for generating bin-average 
              y_var_pre = covariate 
              y_lowerb = the lowerbound of y axis
              y_upperb = the upperbound of y axis


    return: visualization of discontinuity on the covariate at the cutoff
    
    """
     
    dt = data
    dt = dt.dropna()

    xls = dt[(dt.dist1 < 0)].loc[:, 'av_dist1']  # xls = x_left_scatter
    yls = dt[(dt.dist1 < 0)].loc[:, y_var_sca]  # yls = y_left_scatter 
                                                # y_var_sca = 'av' + i 

    xrs = dt[(dt.dist1 > 0)].loc[:, 'av_dist1']  # x_right_scatter
    yrs = dt[(dt.dist1 > 0)].loc[:, y_var_sca]  # y_right_scatter 
                                                # y_var_sca = 'av' + i 

    x3 = dt[(dt.dist1 < 0)].loc[:,'dist1'].to_numpy()    
    y3 = dt[(dt.dist1 < 0)].loc[:,y_var_pre].to_numpy() # y_var_pre = i 
    z3 = localreg(x3, y3, x0=None, degree=1, kernel=epanechnikov, frac=None)
    x4 = dt[(dt.dist1 > 0)].loc[:,'dist1'].to_numpy()
    y4 = dt[(dt.dist1 > 0)].loc[:,y_var_pre].to_numpy()
    z4 = localreg(x4, y4, x0=None, degree=1, kernel=epanechnikov, frac=None)

    x3grid = np.linspace(x3.min(),x3.max())
    x4grid = np.linspace(x4.min(),x4.max())
    
    K = 100
    left = np.stack([bootstrap_left(boot = boot_fig_cov, y_var = y_var_pre, x_var = 'dist1') for k in range(K)]).T
    right = np.stack([bootstrap_right(boot = boot_fig_cov, y_var = y_var_pre, x_var = 'dist1') for k in range(K)]).T    
    mean_left = np.nanmean(left, axis=1)
    stderr_left = scipy.stats.sem(left, axis=1)    
    mean_right = np.nanmean(right, axis=1)
    stderr_right = scipy.stats.sem(right, axis=1)


    plt.grid(True)
    plt.axvline(x=0, color='r')
    plt.xlim(-0.51, 0.51)
    plt.xticks([-0.5, 0, 0.5])
    plt.ylim(y_lowerb, y_upperb)
            
    plt.scatter(xls, yls, s=30, facecolors='none', edgecolors='black')
    plt.scatter(xrs, yrs, s=30, facecolors='none', edgecolors='black')

    plt.plot(x3grid, mean_left-1.96*stderr_left, 'b--')
    plt.plot(x3grid, mean_left+1.96*stderr_left, 'b--')
    plt.plot(x4grid, mean_right-1.96*stderr_right, 'b--')
    plt.plot(x4grid, mean_right+1.96*stderr_right, 'b--') 

    plt.plot(x3grid, mean_left, color='orange')
    plt.plot(x4grid, mean_right, color='orange')
    plt.title(plot_title)



def plot_cc(data, boot_fig_cov):

    """
    return: combine all visualizations of discontinuity on covariates
            in one figure
    
    """
    
    
    abc = ["debt","tipo","vcp","pob","density","pob_mes6591","pob_5_1491",
     "extr_noeu91","unempl","income","educ2","presscirc","regre",
     "regde","meanden","regterm"]
    cv = for_cov(abc)
        
    plt.figure(figsize=(17, 13.2))

    for i in cv.index:
                   
        plt.subplot(4, 4, i + 1)
        plot_Covariates_Continuity(data, boot_fig_cov,y_var_sca = cv.iloc[i,1],
                                         y_var_pre = cv.iloc[i,0], y_lowerb = cv.iloc[i,3],
                                         y_upperb = cv.iloc[i,4], plot_title = cv.iloc[i,2])
                                   



##=========================
## Figure 5


def plot_subplot_fig5 (data,low_comp,boot_figure5,plot_title):


    """
    argument: low_comp; if == 1, subgroup of low competition
                        if == 0, subgroup of high competition,
              boot_figure5 = dataframe for bootstraping  

    return: visualization of discontinuity on transfer of a subgroup
            (low competition group or high competition group)
    
    """
    

    data1 = data
    
    x11 = data1[(data1.dist1 < 0)].loc[:, 'av_dist1']
    y11 = data1[(data1.dist1 < 0)].loc[:, 'av_tk']
    x22 = data1[(data1.dist1 > 0)].loc[:, 'av_dist1']
    y22 = data1[(data1.dist1 > 0)].loc[:, 'av_tk']
    x3 = data1[data1.dist1<0].loc[:,'dist1'].to_numpy()    
    y3 = data1[data1.dist1<0].loc[:,'tk'].to_numpy()
    x4 = data1[data1.dist1>0].loc[:,'dist1'].to_numpy()
    y4 = data1[data1.dist1>0].loc[:,'tk'].to_numpy()

    x3grid = np.linspace(x3.min(),x3.max())
    x4grid = np.linspace(x4.min(),x4.max())
    
    K = 100
    left = np.stack([bootstrap_left(boot = boot_figure5, y_var = 'tk', x_var = 'dist1') for k in range(K)]).T
    right = np.stack([bootstrap_right(boot = boot_figure5, y_var = 'tk', x_var = 'dist1') for k in range(K)]).T
    mean_left = np.nanmean(left, axis=1)
    stderr_left = scipy.stats.sem(left, axis=1)
    mean_right = np.nanmean(right, axis=1)
    stderr_right = scipy.stats.sem(right, axis=1)

    plt.grid(True)
    plt.axvline(x=0, color='r')
    plt.xlim(-0.51, 0.51)
    plt.xticks([-0.5, 0, 0.5])
    plt.ylim(40, 210)
    plt.yticks([50, 100, 150, 200])
            
    plt.scatter(x11, y11, s=30, facecolors='none', edgecolors='black')
    plt.scatter(x22, y22, s=30, facecolors='none', edgecolors='black')
    
    plt.plot(x3grid, mean_left-1.96*stderr_left, 'b--')
    plt.plot(x3grid, mean_left+1.96*stderr_left, 'b--')
    plt.plot(x4grid, mean_right-1.96*stderr_right, 'b--')
    plt.plot(x4grid, mean_right+1.96*stderr_right, 'b--') 

    plt.plot(x3grid, mean_left, color='green')
    plt.plot(x4grid, mean_right, color='green')
    
    plt.xlabel("Regional incumbent's bloc vote margin",fontsize = 13)
    plt.ylabel("Regional transfers",fontsize = 13)
    plt.title(plot_title)





##=========================
## Figure 6
    


def plot_figure6 (data,boot_figure6):


    """
    argument: boot_figure6 = dataframe for bootstraping  

    return: graphically check if regional seat margin does not
            show systematic discontinuity at the cutoff. 
    """


    data1 = subset_figure6(data)
    x11 = data1[(data1.dist1 < 0)].loc[:, 'av_dist1']
    y11 = data1[(data1.dist1 < 0)].loc[:, 'av_ecs1']
    x22 = data1[(data1.dist1 > 0)].loc[:, 'av_dist1']
    y22 = data1[(data1.dist1 > 0)].loc[:, 'av_ecs1']
    x3 = data1[data1.dist1<0].loc[:,'dist1'].to_numpy()    
    y3 = data1[data1.dist1<0].loc[:,'ecs1'].to_numpy()
    x4 = data1[data1.dist1>0].loc[:,'dist1'].to_numpy()
    y4 = data1[data1.dist1>0].loc[:,'ecs1'].to_numpy()

    x3grid = np.linspace(x3.min(),x3.max())
    x4grid = np.linspace(x4.min(),x4.max())
    
    K = 100
    left = np.stack([bootstrap_left(boot = boot_figure6, y_var = 'ecs1', x_var = 'dist1') for k in range(K)]).T
    right = np.stack([bootstrap_right(boot = boot_figure6, y_var = 'ecs1', x_var = 'dist1') for k in range(K)]).T
    
    mean_left = np.nanmean(left, axis=1)
    stderr_left = scipy.stats.sem(left, axis=1)
    mean_right = np.nanmean(right, axis=1)
    stderr_right = scipy.stats.sem(right, axis=1)

    plt.figure(figsize=[7.5,5.5])
    plt.grid(True)
    plt.axvline(x=0, color='r')
    plt.xlim(-0.51, 0.51)
    plt.xticks([-0.5, 0, 0.5])
    plt.ylim(-6, 4)
            
    plt.scatter(x11, y11, s=30, facecolors='none', edgecolors='black')
    plt.scatter(x22, y22, s=30, facecolors='none', edgecolors='black')
    
    plt.plot(x3grid, mean_left-1.96*stderr_left, 'b--')
    plt.plot(x3grid, mean_left+1.96*stderr_left, 'b--')
    plt.plot(x4grid, mean_right-1.96*stderr_right, 'b--')
    plt.plot(x4grid, mean_right+1.96*stderr_right, 'b--') 

    plt.plot(x3grid, mean_left, color='orange')
    plt.plot(x4grid, mean_right, color='orange')
    
    plt.xlabel("Regional incumbent's bloc vote margin",fontsize = 13)
    plt.ylabel("Regional seat margin",fontsize = 13)




##=========================
## Figure 7


def plot_figure7(data, color):

    """ 
    return: marginal effect of alignment along the different level of
            competition. (the indicator of the level of competition is
            regional seat margin)
    """
    
    x = data["ecs1_bis"]
    y1 = data["marginal"]
    y2 = data["conf1"]
    y3 = data["conf2"]

    fig, ax1 = plt.subplots(figsize=(8,6))

    ax1.set_xlabel('Regional seat margin',fontsize = 13)
    ax1.set_ylabel('Marginal effect', color='black',fontsize = 13)
    ax1.set_xlim([-12, 12])
    ax1.set_yticks([-100, 0, 100, 200])
    ax1.axvline(x=0,linestyle = ':', color='gray') 
    ax1.plot(x, y1,  label='marginal effect')
    ax1.plot(x, y2, '--', color = 'black',label='95% lower bound')
    ax1.plot(x, y3, '-.', color = 'black',label='95% upper bound')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Density', color=color,fontsize = 13)  # we already handled the x-label with ax1
    sns.kdeplot(x, bw = 4, kernel='epa',ax = ax2, color = color, legend=False, shade =True)
    ax2.tick_params(axis='y', labelcolor=color)

    leg1 = ax1.legend(loc='upper left')



##=========================
## Robustness Checks




def plot_subplot_robust(data,low_comp,boot_figure,plot_title):

    """ 
    argument:low_comp; if == 1, subgroup of low competition
                        if == 0, subgroup of high competition,
              boot_figure = dataframe for bootstraping
              
    return: subplot of discontinuity on social spending
    
    """


    data1 = data
    
    x11 = data1[(data1.dist1 < 0)].loc[:, 'av_dist1']
    y11 = data1[(data1.dist1 < 0)].loc[:, 'av_f34142_c6_c6'] # bin-average of social spending
    x22 = data1[(data1.dist1 > 0)].loc[:, 'av_dist1']
    y22 = data1[(data1.dist1 > 0)].loc[:, 'av_f34142_c6_c6'] # bin-average of social spending
    x3 = data1[data1.dist1<0].loc[:,'dist1'].to_numpy()    
    y3 = data1[data1.dist1<0].loc[:,'f34142_c6_c6'].to_numpy()
    x4 = data1[data1.dist1>0].loc[:,'dist1'].to_numpy()
    y4 = data1[data1.dist1>0].loc[:,'f34142_c6_c6'].to_numpy()

    x3grid = np.linspace(x3.min(),x3.max())
    x4grid = np.linspace(x4.min(),x4.max())
    
    K = 100
    left = np.stack([bootstrap_left(boot = boot_figure, y_var = 'f34142_c6_c6', x_var = 'dist1') for k in range(K)]).T
    right = np.stack([bootstrap_right(boot = boot_figure, y_var = 'f34142_c6_c6', x_var = 'dist1') for k in range(K)]).T
    mean_left = np.nanmean(left, axis=1)
    stderr_left = scipy.stats.sem(left, axis=1)
    mean_right = np.nanmean(right, axis=1)
    stderr_right = scipy.stats.sem(right, axis=1)

    plt.grid(True)
    plt.axvline(x=0, color='r')
    plt.xlim(-0.51, 0.51)
    plt.xticks([-0.5, 0, 0.5])
    plt.ylim(0, 20)
    plt.yticks([5, 10, 15, 20])
            
    plt.scatter(x11, y11, s=30, facecolors='none', edgecolors='black')
    plt.scatter(x22, y22, s=30, facecolors='none', edgecolors='black')
    
    plt.plot(x3grid, mean_left-1.96*stderr_left, 'b--')
    plt.plot(x3grid, mean_left+1.96*stderr_left, 'b--')
    plt.plot(x4grid, mean_right-1.96*stderr_right, 'b--')
    plt.plot(x4grid, mean_right+1.96*stderr_right, 'b--')
    plt.fill_between(x3grid, mean_left-1.96*stderr_left, mean_left+1.96*stderr_left, alpha=0.25)
    plt.fill_between(x4grid, mean_right-1.96*stderr_right, mean_right+1.96*stderr_right, alpha=0.25)     

    plt.plot(x3grid, mean_left, color='green')
    plt.plot(x4grid, mean_right, color='green')
    
    plt.xlabel("Regional incumbent's bloc vote margin",fontsize = 13)
    plt.ylabel("Social Spending",fontsize = 13)
    plt.title(plot_title)




def policy_preference_robust(data):

    plt.figure(figsize=(17, 4.5))

    plt.subplot(1, 2, 1)
    ab = append_av_for_figure_robust(data,low_comp = 1,left = 1)
    plot_subplot_robust(data = ab,low_comp = 1,boot_figure = ab,plot_title = "Low Competition")


    plt.subplot(1, 2, 2)
    cd = append_av_for_figure_robust(data,low_comp = 0,left = 1)
    plot_subplot_robust(data = cd,low_comp = 0,boot_figure = cd,plot_title = "High Competition")
    plt.suptitle("(1) Left-wing ",fontsize=16)


    plt.figure(figsize=(17, 4.5))

    plt.subplot(1, 2, 1)
    ef = append_av_for_figure_robust(data,low_comp = 1,left = 0)
    plot_subplot_robust(data = ef,low_comp = 1,boot_figure = ef,plot_title = "Low Competition")


    plt.subplot(1, 2, 2)
    gh = append_av_for_figure_robust(data,low_comp = 0,left = 0)
    plot_subplot_robust(data = gh,low_comp = 0,boot_figure = gh,plot_title = "High Competition")
    plt.suptitle(" (2) Right-wing",fontsize=16)
    




def bandwidth_graph_LATE(data):
    
    bw = np.linspace(0.01, 1, num=51)
    
    est = []
    ci_lo = []
    ci_up = []
    for i in bw:
        result = second_stage_2SLS_local(data, bandwidth = i,cluster_var = "codiine",covariates = 0)
        est.append(result.beta["ab"])    
        ci_lo.append(result.ci_lo["ab"])
        ci_up.append(result.ci_hi["ab"])
        
    plt.figure(figsize=[9,7])

    plt.ylim(50,140)
    plt.axvline(x=0.193,linestyle = '-.', color='green',label='h* = 0.193')
    plt.axvline(x=0.386,linestyle = '-.', color='brown',label='2h* = 0.386')
    plt.axvline(x=0.0965,linestyle = '-.', color='purple',label='1/2h* = 0.0965')
    plt.axhline(y=102.57, color='black',label='True effect = 102.57')
    plt.axhline(y=120,color = 'gray', linewidth=0.3)
    plt.axhline(y=80,color = 'gray', linewidth=0.3)
    plt.axhline(y=60,color = 'gray', linewidth=0.3)    
    plt.plot(bw, est, color='black', linewidth=4,label='Estimate')
    plt.plot(bw, ci_lo, 'b--',label='95% lower bound')
    plt.plot(bw, ci_up,  '-.', color ='blue',label='95% upper bound')
    plt.xlabel("Bandwidth",fontsize = 13)
    plt.ylabel("LATE Estimate",fontsize = 13)
    plt.legend(loc='upper right')



def bandwidth_graph_HLATE(data):
    
    bw = np.linspace(0.05, 1, num=51)
    
    est = []
    ci_lo = []
    ci_up = []
    for i in bw:
        result = effect_of_competition_local(data, bandwidth = i)
        est.append(result.beta["esas1"])    
        ci_lo.append(result.ci_lo["esas1"])
        ci_up.append(result.ci_hi["esas1"])
        
    plt.figure(figsize=[9,7])

    plt.ylim(-10,20)
    plt.axvline(x=0.193,linestyle = '-.', color='green',label='h* = 0.193')
    plt.axvline(x=0.386,linestyle = '-.', color='brown',label='2h* = 0.386')
    plt.axvline(x=0.0965,linestyle = '-.', color='purple',label='1/2h* = 0.0965')
    plt.axhline(y=7.7, color='black',label='True effect = 7.7')
   
    plt.plot(bw, est, color='black', linewidth=4,label='Estimate')
    plt.plot(bw, ci_lo, 'b--',label='95% lower bound')
    plt.plot(bw, ci_up,  '-.', color ='blue',label='95% upper bound')
    plt.legend(loc='upper right')
    plt.xlabel("Bandwidth",fontsize = 13)
    plt.ylabel("HLATE Estimate",fontsize = 13)
        
 
