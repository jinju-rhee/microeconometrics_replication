
cd "/Users/jj/Desktop/GitubReplication/Electoral/113710-V1/data/data"






**********
** Figure 7 - Marginal effects
**********
clear all

use "db_main.dta", clear

//Generate "within" regional competition variable
su compreg1 if dca1==1
gen ecs1_bis = (compreg1 - r(mean)) if dca1==1

foreach i of numlist 2/15 {
su compreg1 if dca`i'==1
replace ecs1_bis = (compreg1 - r(mean)) if dca`i'==1
}

ge aecs1_bis=ecs1_bis*ab 
ge decs1_bis=ecs1_bis*dab 

ge aecs1_bis_vsa=ecs1_bis*ab*dist1 
ge decs1_bisvsa=ecs1_bis*dab*dist1 
ge aecs1_bisvsa2=ecs1_bis*ab*dist2
ge decs1_bisvsa2=ecs1_bis*dab*dist2 

ge dist1_ecs1_bis=ecs1_bis*dist1
ge dist2_ecs1_bis=ecs1_bis*dist2

global controls1 "dist1_ecs1  dist1 ecs1"

global regFE "i.codccaa"
global controls2 "dist1_ecs1 dist2_ecs1 dist1 dist2  ecs1"
global controls2b "dist1_ecs1_bis dist2_ecs1_bis dist1 dist2 "
global regFE "i.codccaa"

foreach i of numlist 1/15{
su codiine if dca`i'==1  //To know how many observations in each region
}

ivregress 2sls tk  (dca_ab* aecs1_bis aecs1_bis_vsa aecs1_bisvsa2 dca_vsa* dca_2vsa* resa desa denssa termssa presssa educ2sa vsa_ecs1 vsa_re vsa_dens vsa_te vsa_pr vsa_edu = dca_dab* decs1_bis decs1_bisvsa decs1_bisvsa2 dca_vda* reda deda densda vda_ecs1 vda_re vda_dens termsda pressda educ2da  vda_te vda_pr vda_edu dca_2vda*) $controls1 $regFE $controls2b dist1_regre regre regde dist1_regde meanden dist1_meanden dist1_regterm regterm dist1_presscirc presscirc  dist1_educ educ2, vce(cluster codccaa)
predictnl marginal=_b[dca_ab1]*(1078/6050)+_b[dca_ab2]*(202/6050)+_b[dca_ab3]*(147/6050)+_b[dca_ab4]*(115/6050)+_b[dca_ab5]*(160/6050)+_b[dca_ab6]*(112/6050)+_b[dca_ab7]*(533/6050)+_b[dca_ab8]*(661/6050)+_b[dca_ab9]*(828/6050)+_b[dca_ab10]*(707/6050)+_b[dca_ab11]*(384/6050)+_b[dca_ab12]*(747/6050)+_b[dca_ab13]*(207/6050)+_b[dca_ab14]*(102/6050)+_b[dca_ab15]*(67/6050)+_b[aecs1_bis]*ecs1_bis  if e(sample), ci (conf1 conf2)
sort ecs1_bis
twoway (line marginal ecs1_bis if e(sample), yaxis(1) lc(black) lw(thin)) (line conf1 ecs1_bis if e(sample), yaxis(1) lc(black) lw(thin) lp(dash)) (line conf2 ecs1_bis if e(sample), yaxis(1) lc(black) lw(thin) lp(dash)) (kdensity ecs1_bis if e(sample), bwidth(4)  yaxis(2) lc(cranberry) lw(thin)),  yscale(range(-50 250)) yscale(range(0 0.15)) ylabel(-100(100)200, axis(1)) ylabel(0(0.01)0.06, axis(2)) xlabel(-12(4)12) xline(0, lp(dot) lc(black)) yline(0, lp(dot) lc(black)) legend(off) graphregion(fc(white)) ///
 ytitle("Marginal effect", margin(medsmall) axis(1) size(vlarge))  ytitle("Density", margin(medsmall) axis(2) size(vlarge))   xtitle("Regional seat margin", margin(medsmall) size(vlarge)) 
