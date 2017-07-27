from basic import *
import sys
from paths import path_to_db

## these guys are for external sharing, as well as
## get_alpha_trim_probs
## get_beta_trim_probs
##
all_trim_probs = {}
all_countrep_pseudoprobs = {} ## pseudoprobs because they do not sum to 1.0, due to ambiguity of gene assignments
all_trbd_nucseq = {}

verbose = ( __name__ == '__main__' )


##############################################################################################################

# >K02545|TRBD1*01|Homo sapiens|F|D-REGION|82..93|12 nt|1| | | | |12+0=12| | |
# gggacagggggc
# >X02987|TRBD2*01|Homo sapiens|F|D-REGION|140..155|16 nt|1| | | | |16+0=16| | |
# gggactagcggggggg
# >M14159|TRBD2*02|Homo sapiens|F|D-REGION|569..584|16 nt|1| | | | |16+0=16| | |
# gggactagcgggaggg

trbd_nucseq_mouse = { ## mouse
    1:'gggacagggggc',   ## len 12
    2:'gggactgggggggc', ## len 14
}

trbd_nucseq_human = {
    1:'gggacagggggc',
    2:'gggactagcggggggg', ## actually 2*01
    3:'gggactagcgggaggg', ## actually 2*02
    #  1234567890123456

}

all_trbd_nucseq = {'mouse':trbd_nucseq_mouse, 'human':trbd_nucseq_human}

##The following hard-coded probabilities are actually derived from the probabilities files in the /db/ directory. This will eventually be re-coded to obtain the relevant probabilities directly from those files.
alpha_trim_prob_lines_mouse = """
PROB_A_v_trim  0.421946  0.141516  0.113666  0.114740  0.063751  0.045711  0.034423  0.029273  0.013622  0.009955  0.007622  0.002139  0.000761  0.000254  0.000527  0.000095
PROB_A_j_trim  0.209729  0.139163  0.128939  0.148367  0.110268  0.110984  0.060651  0.036761  0.027030  0.011851  0.006179  0.004318  0.001836  0.002154  0.001070  0.000701
PROB_A_vj_insert  0.086069  0.135083  0.184446  0.188326  0.156083  0.109790  0.063442  0.034039  0.019199  0.009582  0.005970  0.003617  0.001766  0.001005  0.000935  0.000647"""

alpha_trim_prob_lines_human = """
PROB_A_v_trim  0.245684  0.124964  0.101813  0.141642  0.112687  0.083126  0.062932  0.046923  0.030782  0.021188  0.009638  0.006040  0.009861  0.001567  0.000562  0.000593
PROB_A_j_trim  0.123552  0.085185  0.078736  0.103617  0.122755  0.118608  0.083612  0.085668  0.085359  0.030712  0.025076  0.029625  0.009966  0.007685  0.006333  0.003511
PROB_A_vj_insert  0.018433  0.037695  0.076474  0.121199  0.152592  0.142994  0.113346  0.091222  0.070496  0.053328  0.041467  0.030275  0.020646  0.014088  0.009481  0.006264
"""


beta_trim_prob_lines_mouse = """
PROB_B_D1_d01_trim 0,0:  0.017328 0,1:  0.019039 0,2:  0.039170 0,3:  0.051505 0,4:  0.015357 0,5:  0.049524 0,6:  0.061235 0,7:  0.017442 0,8:  0.026022 0,9:  0.010205 0,10:  0.007699 0,11:  0.004773 1,0:  0.008721 1,1:  0.009709 1,2:  0.016887 1,3:  0.023271 1,4:  0.007498 1,5:  0.021168 1,6:  0.022242 1,7:  0.006524 1,8:  0.012729 2,0:  0.009940 2,1:  0.011223 2,2:  0.018346 2,3:  0.027652 2,4:  0.009241 2,5:  0.023065 2,6:  0.020207 2,7:  0.005839 2,8:  0.011155 3,0:  0.011617 3,1:  0.010636 3,2:  0.020098 3,3:  0.025772 3,4:  0.006680 3,5:  0.014703 3,6:  0.014204 3,7:  0.006141 3,8:  0.002936 4,0:  0.019056 4,1:  0.019074 4,2:  0.032236 4,3:  0.042881 4,4:  0.013550 4,5:  0.024351 4,6:  0.013685 4,7:  0.003398 5,0:  0.010419 5,1:  0.015500 5,2:  0.021848 5,3:  0.014659 5,4:  0.007406 5,5:  0.003380 6,0:  0.011892 6,1:  0.016955 6,2:  0.009479 7,0:  0.006671 8,0:  0.007351 9,0:  0.006069 10,0:  0.002637
PROB_B_D1_v_trim 0:  0.218413 1:  0.114507 2:  0.145340 3:  0.121819 4:  0.141786 5:  0.132820 6:  0.079272 7:  0.017948 8:  0.016894 9:  0.003430 10:  0.002171 11:  0.001855 12:  0.002572 13:  0.000793 14:  0.000189 15:  0.000192
PROB_B_D1_j_trim 0:  0.300538 1:  0.113929 2:  0.110029 3:  0.141487 4:  0.118952 5:  0.068820 6:  0.058966 7:  0.057623 8:  0.014698 9:  0.005060 10:  0.004946 11:  0.002340 12:  0.001186 13:  0.000596 14:  0.000518 15:  0.000311
PROB_B_D1_vd_insert 0:  0.192147 1:  0.196064 2:  0.207559 3:  0.164503 4:  0.112413 5:  0.056638 6:  0.031895 7:  0.017549 8:  0.009929 9:  0.005574 10:  0.002926 11:  0.001532 12:  0.000759 13:  0.000334 14:  0.000130 15:  0.000047
PROB_B_D1_dj_insert 0:  0.235213 1:  0.206084 2:  0.205009 3:  0.151651 4:  0.099582 5:  0.052791 6:  0.026448 7:  0.012119 8:  0.005332 9:  0.002744 10:  0.001540 11:  0.000752 12:  0.000427 13:  0.000196 14:  0.000087 15:  0.000026
PROB_B_D1_tot_d_trim 0:  0.017328 1:  0.027760 2:  0.058819 3:  0.091232 4:  0.086666 5:  0.134265 6:  0.177044 7:  0.157783 8:  0.112495 9:  0.080803 10:  0.044697 11:  0.011108
PROB_B_D2_d01_trim 0,0:  0.018237 0,1:  0.012803 0,2:  0.028500 0,3:  0.036180 0,4:  0.029843 0,5:  0.020330 0,6:  0.010563 0,7:  0.006157 0,8:  0.013797 0,9:  0.012542 0,10:  0.018955 0,11:  0.006526 0,12:  0.004751 0,13:  0.002466 1,0:  0.013659 1,1:  0.010341 1,2:  0.020492 1,3:  0.022325 1,4:  0.017114 1,5:  0.011767 1,6:  0.006256 1,7:  0.003406 1,8:  0.005255 1,9:  0.004811 1,10:  0.008818 2,0:  0.020930 2,1:  0.015092 2,2:  0.025925 2,3:  0.025617 2,4:  0.019533 2,5:  0.014255 2,6:  0.007584 2,7:  0.003095 2,8:  0.004750 2,9:  0.004239 2,10:  0.006845 3,0:  0.015810 3,1:  0.010981 3,2:  0.018570 3,3:  0.018353 3,4:  0.014230 3,5:  0.009517 3,6:  0.004914 3,7:  0.001909 3,8:  0.006631 3,9:  0.003856 3,10:  0.001519 4,0:  0.026927 4,1:  0.019562 4,2:  0.034211 4,3:  0.034410 4,4:  0.024444 4,5:  0.017820 4,6:  0.008870 4,7:  0.004499 4,8:  0.010368 4,9:  0.001740 5,0:  0.013638 5,1:  0.012254 5,2:  0.018841 5,3:  0.017269 5,4:  0.015131 5,5:  0.008742 5,6:  0.005399 5,7:  0.002368 5,8:  0.001485 6,0:  0.021192 6,1:  0.018558 6,2:  0.018255 6,3:  0.010342 6,4:  0.006931 7,0:  0.016466 8,0:  0.005957 9,0:  0.007456 10,0:  0.007138 11,0:  0.007036 12,0:  0.002646
PROB_B_D2_v_trim 0:  0.246466 1:  0.124381 2:  0.142223 3:  0.124901 4:  0.131933 5:  0.127862 6:  0.065644 7:  0.013355 8:  0.015438 9:  0.002295 10:  0.001574 11:  0.001239 12:  0.002002 13:  0.000391 14:  0.000126 15:  0.000173
PROB_B_D2_j_trim 0:  0.310095 1:  0.123791 2:  0.110055 3:  0.135452 4:  0.115906 5:  0.061610 6:  0.067288 7:  0.057558 8:  0.008041 9:  0.003436 10:  0.003244 11:  0.001142 12:  0.001215 13:  0.000472 14:  0.000467 15:  0.000228
PROB_B_D2_vd_insert 0:  0.207097 1:  0.200057 2:  0.206337 3:  0.157210 4:  0.107401 5:  0.055060 6:  0.029684 7:  0.016179 8:  0.009612 9:  0.005406 10:  0.002867 11:  0.001583 12:  0.000916 13:  0.000381 14:  0.000164 15:  0.000047
PROB_B_D2_dj_insert 0:  0.225980 1:  0.195041 2:  0.202632 3:  0.155303 4:  0.110594 5:  0.057727 6:  0.028903 7:  0.012853 8:  0.005628 9:  0.002659 10:  0.001418 11:  0.000727 12:  0.000291 13:  0.000145 14:  0.000075 15:  0.000024
PROB_B_D2_tot_d_trim 0:  0.018237 1:  0.026462 2:  0.059771 3:  0.087573 4:  0.116000 5:  0.114831 6:  0.127873 7:  0.129173 8:  0.100228 9:  0.076556 10:  0.062106 11:  0.043147 12:  0.030833 13:  0.007210
"""


beta_trim_prob_lines_human = """
PROB_B_D1_d01_trim 0,0:  0.009851 0,1:  0.011135 0,2:  0.022044 0,3:  0.036833 0,4:  0.018447 0,5:  0.033472 0,6:  0.019981 0,7:  0.029005 0,8:  0.030576 0,9:  0.019285 0,10:  0.013880 0,11:  0.004568 1,0:  0.007021 1,1:  0.007797 1,2:  0.013446 1,3:  0.025040 1,4:  0.013249 1,5:  0.020490 1,6:  0.008990 1,7:  0.017085 1,8:  0.020509 2,0:  0.008305 2,1:  0.008952 2,2:  0.015849 2,3:  0.028920 2,4:  0.014885 2,5:  0.018680 2,6:  0.008733 2,7:  0.012326 2,8:  0.013034 3,0:  0.011053 3,1:  0.010166 3,2:  0.019387 3,3:  0.030241 3,4:  0.011725 3,5:  0.013405 3,6:  0.008559 3,7:  0.008527 3,8:  0.002443 4,0:  0.016647 4,1:  0.019585 4,2:  0.031096 4,3:  0.045679 4,4:  0.022926 4,5:  0.022043 4,6:  0.007483 4,7:  0.002514 5,0:  0.010447 5,1:  0.018929 5,2:  0.024847 5,3:  0.015999 5,4:  0.009198 5,5:  0.002895 6,0:  0.023243 6,1:  0.027351 6,2:  0.015789 7,0:  0.018253 8,0:  0.020088 9,0:  0.013621 10,0:  0.003471
PROB_B_D1_v_trim 0:  0.157589 1:  0.104315 2:  0.117445 3:  0.126611 4:  0.138668 5:  0.135088 6:  0.114681 7:  0.049114 8:  0.030956 9:  0.009715 10:  0.010220 11:  0.004192 12:  0.000871 13:  0.000318 14:  0.000119 15:  0.000100
PROB_B_D1_j_trim 0:  0.141419 1:  0.097561 2:  0.116769 3:  0.113486 4:  0.150125 5:  0.112037 6:  0.086083 7:  0.076976 8:  0.054844 9:  0.018727 10:  0.014717 11:  0.007935 12:  0.003650 13:  0.002480 14:  0.001903 15:  0.001288
PROB_B_D1_vd_insert 0:  0.129710 1:  0.115294 2:  0.141395 3:  0.147172 4:  0.131378 5:  0.094373 6:  0.072773 7:  0.055475 8:  0.040273 9:  0.028343 10:  0.018599 11:  0.011437 12:  0.006986 13:  0.003746 14:  0.002020 15:  0.001025
PROB_B_D1_dj_insert 0:  0.171766 1:  0.119727 2:  0.142725 3:  0.141787 4:  0.124684 5:  0.094005 6:  0.070183 7:  0.048422 8:  0.032195 9:  0.021871 10:  0.014164 11:  0.008843 12:  0.004997 13:  0.002781 14:  0.001295 15:  0.000556
PROB_B_D1_tot_d_trim 0:  0.009851 1:  0.018156 2:  0.038146 3:  0.070284 4:  0.086149 5:  0.125060 6:  0.158865 7:  0.184531 8:  0.144601 9:  0.105541 10:  0.049290 11:  0.009525
PROB_B_D2_d01_trim 0,0:  0.003106 0,1:  0.003250 0,2:  0.004931 0,3:  0.008087 0,4:  0.005932 0,5:  0.013381 0,6:  0.008743 0,7:  0.008790 0,8:  0.013185 0,9:  0.009668 0,10:  0.022819 0,11:  0.023607 0,12:  0.010705 0,13:  0.011276 0,14:  0.007957 0,15:  0.002231 1,0:  0.002585 1,1:  0.002798 1,2:  0.004298 1,3:  0.007090 1,4:  0.004385 1,5:  0.007805 1,6:  0.004206 1,7:  0.004680 1,8:  0.006041 1,9:  0.004188 1,10:  0.011055 1,11:  0.014133 1,12:  0.012301 2,0:  0.003043 2,1:  0.003074 2,2:  0.004856 2,3:  0.006895 2,4:  0.003645 2,5:  0.006535 2,6:  0.003742 2,7:  0.004266 2,8:  0.006045 2,9:  0.003090 2,10:  0.009224 2,11:  0.010099 2,12:  0.008687 3,0:  0.003294 3,1:  0.003369 3,2:  0.004944 3,3:  0.006048 3,4:  0.003119 3,5:  0.006509 3,6:  0.004124 3,7:  0.003547 3,8:  0.006259 3,9:  0.004124 3,10:  0.010972 3,11:  0.007242 3,12:  0.001614 4,0:  0.007152 4,1:  0.006908 4,2:  0.010572 4,3:  0.013555 4,4:  0.007351 4,5:  0.014211 4,6:  0.007394 4,7:  0.007204 4,8:  0.012770 4,9:  0.010973 4,10:  0.013798 4,11:  0.001669 5,0:  0.006243 5,1:  0.005088 5,2:  0.007507 5,3:  0.009954 5,4:  0.004701 5,5:  0.008158 5,6:  0.004279 5,7:  0.005144 5,8:  0.009949 5,9:  0.004619 5,10:  0.001528 6,0:  0.008426 6,1:  0.006817 6,2:  0.009806 6,3:  0.013257 6,4:  0.006417 6,5:  0.010680 6,6:  0.007189 6,7:  0.008940 6,8:  0.001677 7,0:  0.010760 7,1:  0.011067 7,2:  0.017205 7,3:  0.023545 7,4:  0.012010 7,5:  0.015848 7,6:  0.007688 7,7:  0.002079 8,0:  0.021589 8,1:  0.025013 8,2:  0.035743 8,3:  0.047765 8,4:  0.025273 8,5:  0.016927 8,6:  0.003964 9,0:  0.034725 9,1:  0.028198 9,2:  0.012732 9,3:  0.012333
PROB_B_D2_v_trim 0:  0.169031 1:  0.110850 2:  0.116548 3:  0.123818 4:  0.141250 5:  0.133656 6:  0.103275 7:  0.046453 8:  0.030576 9:  0.008795 10:  0.009750 11:  0.004570 12:  0.000879 13:  0.000310 14:  0.000154 15:  0.000087
PROB_B_D2_j_trim 0:  0.145654 1:  0.093288 2:  0.147318 3:  0.117107 4:  0.137770 5:  0.120607 6:  0.088698 7:  0.064087 8:  0.031993 9:  0.025429 10:  0.013738 11:  0.003418 12:  0.004503 13:  0.002507 14:  0.001800 15:  0.002083
PROB_B_D2_vd_insert 0:  0.136045 1:  0.114519 2:  0.138486 3:  0.141445 4:  0.124322 5:  0.093600 6:  0.074149 7:  0.056314 8:  0.041136 9:  0.029728 10:  0.020202 11:  0.012778 12:  0.008370 13:  0.004729 14:  0.002742 15:  0.001435
PROB_B_D2_dj_insert 0:  0.210516 1:  0.118778 2:  0.137680 3:  0.130190 4:  0.115404 5:  0.089071 6:  0.064532 7:  0.046262 8:  0.031714 9:  0.022390 10:  0.014478 11:  0.009122 12:  0.005175 13:  0.002840 14:  0.001329 15:  0.000520
PROB_B_D2_tot_d_trim 0:  0.003106 1:  0.005835 2:  0.010772 3:  0.018753 4:  0.028399 5:  0.042756 6:  0.050326 7:  0.061288 8:  0.087883 9:  0.133212 10:  0.146054 11:  0.138681 12:  0.116743 13:  0.099126 14:  0.050024 15:  0.007042
PROB_B_D3_d01_trim 0,0:  0.007485 0,1:  0.006285 0,2:  0.018537 0,3:  0.011290 0,4:  0.004350 0,5:  0.009813 0,6:  0.006411 0,7:  0.006446 0,8:  0.009669 0,9:  0.007090 0,10:  0.016734 0,11:  0.017311 0,12:  0.007850 0,13:  0.008269 0,14:  0.005835 0,15:  0.001636 1,0:  0.005848 1,1:  0.005010 1,2:  0.014423 1,3:  0.008272 1,4:  0.003216 1,5:  0.005723 1,6:  0.003084 1,7:  0.003432 1,8:  0.004430 1,9:  0.003071 1,10:  0.008107 1,11:  0.010364 1,12:  0.009021 2,0:  0.005530 2,1:  0.004513 2,2:  0.013177 2,3:  0.007094 2,4:  0.002673 2,5:  0.004792 2,6:  0.002744 2,7:  0.003129 2,8:  0.004433 2,9:  0.002266 2,10:  0.006764 2,11:  0.007406 2,12:  0.006371 3,0:  0.006390 3,1:  0.004895 3,2:  0.013959 3,3:  0.005993 3,4:  0.002287 3,5:  0.004773 3,6:  0.003024 3,7:  0.002601 3,8:  0.004590 3,9:  0.003024 3,10:  0.008046 3,11:  0.005311 3,12:  0.001184 4,0:  0.013568 4,1:  0.010513 4,2:  0.028067 4,3:  0.014426 4,4:  0.005391 4,5:  0.010422 4,6:  0.005422 4,7:  0.005282 4,8:  0.009364 4,9:  0.008047 4,10:  0.010119 4,11:  0.001224 5,0:  0.012148 5,1:  0.007828 5,2:  0.020669 5,3:  0.009494 5,4:  0.003448 5,5:  0.005983 5,6:  0.003138 5,7:  0.003772 5,8:  0.007296 5,9:  0.003387 5,10:  0.001120 6,0:  0.013388 6,1:  0.008235 6,2:  0.021322 6,3:  0.010356 6,4:  0.004706 6,5:  0.007832 6,6:  0.005272 6,7:  0.006556 6,8:  0.001230 7,0:  0.017281 7,1:  0.009627 7,2:  0.023095 7,3:  0.013500 7,4:  0.008807 7,5:  0.011622 7,6:  0.005637 7,7:  0.001524 8,0:  0.013073 8,1:  0.007534 8,2:  0.019132 8,3:  0.016186 8,4:  0.018533 8,5:  0.012413 8,6:  0.002907 9,0:  0.025754 9,1:  0.015882 9,2:  0.022488 10,0:  0.019202 10,1:  0.012742 10,2:  0.018947 11,0:  0.019925 11,1:  0.013685 11,2:  0.012792 12,0:  0.008820 12,1:  0.003885
PROB_B_D3_v_trim 0:  0.170023 1:  0.112737 2:  0.119393 3:  0.122189 4:  0.139578 5:  0.131807 6:  0.104116 7:  0.045618 8:  0.030275 9:  0.009019 10:  0.009777 11:  0.004158 12:  0.000790 13:  0.000282 14:  0.000156 15:  0.000082
PROB_B_D3_j_trim 0:  0.129408 1:  0.081998 2:  0.131730 3:  0.118524 4:  0.141433 5:  0.128631 6:  0.096193 7:  0.073308 8:  0.039357 9:  0.029611 10:  0.014790 11:  0.003309 12:  0.004822 13:  0.002552 14:  0.001964 15:  0.002369
PROB_B_D3_vd_insert 0:  0.122504 1:  0.110865 2:  0.138095 3:  0.143712 4:  0.128349 5:  0.096057 6:  0.074930 7:  0.058686 8:  0.044584 9:  0.031808 10:  0.021360 11:  0.012954 12:  0.007972 13:  0.004406 14:  0.002479 15:  0.001238
PROB_B_D3_dj_insert 0:  0.191460 1:  0.119231 2:  0.132207 3:  0.136987 4:  0.127059 5:  0.098257 6:  0.066858 7:  0.046364 8:  0.030425 9:  0.021105 10:  0.013290 11:  0.008440 12:  0.004655 13:  0.002267 14:  0.001016 15:  0.000380
PROB_B_D3_tot_d_trim 0:  0.007485 1:  0.012132 2:  0.029077 3:  0.036618 4:  0.044262 5:  0.056743 6:  0.070084 7:  0.077220 8:  0.079525 9:  0.098280 10:  0.110665 11:  0.128674 12:  0.118018 13:  0.089369 14:  0.036684 15:  0.005164
"""


alpha_trim_prob_lines = { 'mouse': alpha_trim_prob_lines_mouse,
                          'human': alpha_trim_prob_lines_human }

beta_trim_prob_lines = { 'mouse': beta_trim_prob_lines_mouse,
                         'human': beta_trim_prob_lines_human }


rep_freq_files = { 'mouse': { 'A':[ path_to_db+'/probs_files/alpha_highly_diverse_SRP010815_scjobs_tcrseq_tmp3.read_sra_matches.log_probs.txt',
                                    path_to_db+'/probs_files/mouse_LA_MC_PCR_tmp.read_sra_matches.alpha.log_probs.txt',
],
                              'B': [ path_to_db+'/probs_files/friedman_SRP015131_tmp.read_sra_matches.log_probs.txt',
                                     path_to_db+'/probs_files/mouse_LA_MC_PCR_tmp.read_sra_matches.beta.log_probs.txt',
                                     path_to_db+'/probs_files/Xiamen_SRP004475_tmp1.read_sra_matches.log_probs.txt',
                                 ],
                          },
                   'human': { 'B': [ path_to_db+'/probs_files/tmp7.read_sra_matches.log.subjectX_gdna_data_TCRB_probs.txt',
                                     path_to_db+'/probs_files/tmp7.read_sra_matches.log.subjectY_gdna_data_TCRB_probs.txt'],


                              'A': [ path_to_db+'/probs_files/tmp8.read_sra_matches.log.subjectX_gdna_data_TCRA_probs.txt',
                                     path_to_db+'/probs_files/tmp8.read_sra_matches.log.subjectY_gdna_data_TCRA_probs.txt' ] } }


for org in rep_freq_files:
    for ab in rep_freq_files[org]:
        for filename in rep_freq_files[org][ab]:
            assert exists(filename)

for organism in ['mouse','human']:

    trim_probs = {}
    for line in alpha_trim_prob_lines[organism].split('\n'):
        l = line.split()
        if not l:continue
        assert l[0].startswith('PROB_A')
        tag = l[0][5:]
        vals = map(float,l[1:])
        trim_probs[tag] = dict( zip( range(len(vals)), vals ) )


    for line in beta_trim_prob_lines[organism].split('\n'):
        l = line.split()
        if not l:continue
        assert l[0].startswith('PROB_B')
        tag = l[0][5:]
        trim_probs[tag] = {}
        assert len(l)%2==1
        num_vals = (len(l)-1)/2
        for i in range(num_vals):
            assert l[2*i+1][-1] == ':'
            key = l[2*i+1][:-1]
            if ',' in key:
                key = tuple(map(int,key.split(',')))
            else:
                key = int(key)
            trim_probs[tag][key] = float(l[2*i+2])


    ## fake probability for total trimming of the D gene
    for did,nucseq in all_trbd_nucseq[organism].iteritems():
        trimtag = 'B_D{}_d01_trim'.format(did)
        prob_trim_all_but_1 = 0.0
        for d0_trim in range(len(nucseq)):
            d1_trim = (len(nucseq)-1)-d0_trim
            assert d0_trim + d1_trim == len(nucseq)-1
            prob_trim_all_but_1 += trim_probs[trimtag].get((d0_trim,d1_trim),0)
        prob_trim_all = 0.0
        for d0_trim in range(len(nucseq)+1):
            d1_trim = (len(nucseq))-d0_trim
            prob_trim_all += trim_probs[trimtag].get((d0_trim,d1_trim),0)
        assert prob_trim_all <1e-6
        #print 'old_prob_trim_all:',prob_trim_all,'prob_trim_all_but_1:',prob_trim_all_but_1,'D',did
        new_prob_trim_all = 0.75 * prob_trim_all_but_1
        for d0_trim in range(len(nucseq)+1):
            d1_trim = (len(nucseq))-d0_trim
            if d0_trim == 0:
                #print 'new_prob_trim_all:',new_prob_trim_all
                trim_probs[trimtag][ (d0_trim,d1_trim) ] = new_prob_trim_all ## concentrate all here
            else:
                trim_probs[trimtag][ (d0_trim,d1_trim) ] = 0.0
        total = sum( trim_probs[trimtag].values())
        for k in trim_probs[trimtag]:
            trim_probs[trimtag][k] /= total
        assert abs( 1.0 - sum( trim_probs[trimtag].values()) ) < 1e-6



    beta_prob_tags_single = ['v_trim','j_trim','vd_insert','dj_insert']
    for tag in beta_prob_tags_single:
        tags = [ 'B_D{}_{}'.format(x,tag) for x in all_trbd_nucseq[organism] ]
        #tag1 = 'B_D1_{}'.format(tag)
        #tag2 = 'B_D2_{}'.format(tag)
        avgtag = 'B_{}'.format(tag)
        trim_probs[avgtag] = {}
        for k in trim_probs[tags[0]].keys():
            trim_probs[avgtag][k] = sum( trim_probs[x].get(k,0) for x in tags ) / float(len(tags))

    countrep_probs = {}
    for ab in rep_freq_files[organism]:
        files = rep_freq_files[organism][ab]
        for vj in 'VJ':
            probs ={}
            for file in files:
                assert exists(file)
                for line in popen('grep "^{}{}_COUNTREP_FREQ" {}'.format(ab,vj,file)):
                    l = line.split()
                    assert len(l) == 3
                    nonuniq_freq = float( l[1] ) / 100.0 ## now from 0 to 1
                    rep = l[2]
                    assert rep[2:4] == ab+vj
                    if rep not in probs:probs[rep] = []
                    probs[rep].append( nonuniq_freq )

            avg_probs = {}
            for rep in probs:
                vals = probs[rep] + [0.0]*(len(files) - len(probs[rep]) )
                if len(vals) == 2:
                    avg_probs[rep] = sum( vals )/2.0
                else:
                    assert len(vals) == 3 ## hack
                    avg_probs[rep] = get_median( vals)

            ## probs may have gone slightly below 1.0 due to combination of multiple datasets
            total = min( 1.0, sum( avg_probs.values() ) ) ##only increase probabilities...
            if verbose:
                print 'countrep_pseudoprobs total {:9.6f} actual_sum {:9.6f} {}{} {}'\
                    .format(total, sum(avg_probs.values()), vj, ab, organism )
            for rep in probs:
                countrep_probs[rep] = avg_probs[rep] / total
                if verbose: # __name__ == '__main__' and len(sys.argv) == 1:
                    print 'countrep_pseudoprobs: %12.6f %s %s'%(100.0*countrep_probs[rep],organism,rep)

    ## normalize trim_probs
    for tag,probs in trim_probs.iteritems():
        if type(probs) == type({}):
            total = sum( probs.values())
            assert abs(1.0-total)<1e-2
            #print 'normalize trim_probs:',tag,total
            for k in probs:
                probs[k] = probs[k] / total
        else:
            assert False
            assert type(probs) == type([])
            total = sum( probs )
            assert abs(1.0-total)<1e-2
            #print 'normalize trim_probs:',tag,total
            for i in range(len(probs)):
                probs[i] = probs[i]/total


    all_trim_probs[organism] = trim_probs
    #all_rep_probs[organism] = rep_probs
    all_countrep_pseudoprobs[organism] = countrep_probs



def get_alpha_trim_probs( organism, v_trim, j_trim, vj_insert ):
    total_prob = 1.0
    for ( val, tag ) in zip( [v_trim, j_trim, vj_insert], ['A_v_trim','A_j_trim','A_vj_insert'] ):
        probs = all_trim_probs[organism][tag]
        if val >= len(probs):
            return 0.0
        total_prob *= probs[val]
    return total_prob

def get_beta_trim_probs( organism, d_id, v_trim, d0_trim, d1_trim, j_trim, vd_insert, dj_insert ): ## work in progress
    assert d_id in all_trbd_nucseq[organism]
    dd = (d0_trim,d1_trim)
    d_trim_tag = 'B_D{}_d01_trim'.format(d_id)
    total_prob = all_trim_probs[organism][d_trim_tag].get(dd,0)
    #total_prob = trim_probs[d_trim_tag][dd] ## what about full trims?? will get an error
    for ( val, tag ) in zip( [v_trim, j_trim, vd_insert, dj_insert], beta_prob_tags_single ):
        probs = all_trim_probs[organism]['B_'+tag] ## a dictionary for beta (a list for alpha)
        if val not in probs:
            return 0.0
        total_prob *= probs[val]
    return total_prob


