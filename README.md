# Student Project: Replication of Marta Curto-Grau, Albert Solé-Ollé, and Pilar Sorribas-Navarro. (2018)

>This repository constains my repliacation of following article :
[Marta Curto-Grau, Albert Solé-Ollé, and Pilar Sorribas-Navarro. (2018)](https://www.aeaweb.org/articles?id=10.1257/app.20160618). Curto-Grau, M., Solé-Ollé, A., & Sorribas-Navarro, P. (2018). Does electoral competition curb party favoritism?. American Economic Journal: Applied Economics, 10(4), 378-407.

## Curto-Grau et al. (2018)
Curto-Grau et al. (2018) examined the political favoritism in Spain and the impact of the electoral competition on it by exploiting RDD(Regression Discontinuity Design) frame work. To investigate the relation of the political favoritism to electoral competition, the study used information on capital transfers from regional to local government in Spain, considering that the intergovernmental transfers like this kind is especially vulnerable to the party favoritism. The main result of the study shows that political favoritism shown in the allocation of transfers to the local government is lowered when the regional government meets much competitive elections.
 - The original data provided by the authors can be found [here](https://www.aeaweb.org/articles?id=10.1257/app.20160618).

## Replication
 This repository contains the replication of the main result of Curto-Grau et al. (2018). I reproduced the RD estimates of LATE and HLATE and checked the validity of RDD and robustness of the result. Moreover as an extension, I calculated LATE and HLATE with inclusion of observed regional factors and visualized bandwidth sensitivity. Readers can access to my replication as following ways.
 
 - See the notebook [here](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-jinju-rhee/blob/master/replication_notebook.ipynb)
 - Download the file [here](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-jinju-rhee)
 - [![nbviewer](https://img.shields.io/badge/render-nbviewer-purple.svg?style=flat-square)](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics-course-project-jinju-rhee/blob/master/replication_notebook.ipynb) [![badge](https://img.shields.io/badge/launch-binder-579ACA.svg?logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics-course-project-jinju-rhee/5ce39d47bfb7ff7e0c3040b4d7cc3e42cd7b7e04)


## Reproducibility
Here is the link for the Travis Ci [![Build Status](https://travis-ci.com/jinju-rhee/Student-Project.svg?branch=master)](https://travis-ci.com/jinju-rhee/Student-Project)



## Reference 
- **Marta Curto-Grau, Albert Solé-Ollé, and Pilar Sorribas-Navarro. (2018).** Does electoral competition curb party favoritism?. American Economic Journal: Applied Economics, 10(4), 378-407.
- **Sascha O. Becker, Peter H. Egger, and Maximilian von Ehrlich. (2013).** Absortive Capacity and the Growth and Investment Effects of Regional Transfers: A Regression Discontinuity Design with Heterogeneous Treatment Effects. American Economic Journal:Economic Policy 2013, 5(4): 29–77.
- **Lee, D. S., & Lemieux, T. (2010).** Regression discontinuity designs in economics. Journal of economic literature, 48(2), 281-355.
- **Skovron, C., & Titiunik, R. (2015).** A practical guide to regression discontinuity designs in political science. American Journal of Political Science, 2015, 1-36.
- **Cerulli, G., Dong, Y., Lewbel, A., & Poulsen, A. (2017).** Testing stability of regression discontinuity models. Regression Discontinuity Designs: Theory and Applications, 38, 317Ā339.
- **Gelman, A., & Imbens, G. (2019).** Why high-order polynomials should not be used in regression discontinuity designs. Journal of Business & Economic Statistics, 37(3), 447-456.
- **Jacob, R., Zhu, P., Somers, M. A., & Bloom, H. (2012).** A practical guide to regression discontinuity. MDRC.
- **Eisenhauer, P. (2019).** Course project template, HumanCapitalAnalysis,

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/HumanCapitalAnalysis/template-course-project/blob/master/LICENSE)

