from supy.samples import SampleHolder
from supy.sites import pnfs

pnfs = pnfs()
susy17 = SampleHolder()

susy17.add("T2tt_8.job351", '%s/yeshaq//ICF/automated/2012_09_04_23_14_16/")'%pnfs, xs = 1.0) #dummy XS
susy17.add("T2tt_8.job351_1", '["/uscms/home/elaird/141_ntuples/job351/SusyCAF_Tree_1000_1_Bim.root"]', xs = 1.0) #dummy XS; [(500.0, 100.0), (775.0, 200.0)]
susy17.add("T2tt_500_0",   '["/uscms/home/elaird/141_ntuples/job351/T2tt_8.job351_500_0.root"]', xs = 0.0855) #/pb
susy17.add("T2tt_500_100", '["/uscms/home/elaird/141_ntuples/job351/T2tt_8.job351_500_100.root"]', xs = 0.0855) #/pb
susy17.add("T2tt_500_300", '["/uscms/home/elaird/141_ntuples/job351/T2tt_8.job351_500_300.root"]', xs = 0.0855) #/pb

susy17.add("t1.yos", '%s/yeshaq//ICF/automated/2012_07_02_17_24_20/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("t2.yos", '%s/yeshaq//ICF/automated/2012_07_10_16_25_41/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("t2tt.yos", '%s/yeshaq//ICF/automated/2012_07_10_16_39_39/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("t2bb.yos", '%s/yeshaq//ICF/automated/2012_07_10_16_50_17/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("t1tttt.yos", '%s/yeshaq//ICF/automated/2012_07_10_17_01_28/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("t1bbbb.yos", '%s/yeshaq//ICF/automated/2012_07_10_17_11_44/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("t1tttt.chr", '%s/clucas//ICF/automated/2012_06_04_18_26_52/")'%pnfs, xs = 1.0) #dummy xs
susy17.add("t28tev.chr", '%s/clucas//ICF/automated/2012_08_01_11_43_66/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs

susy17.add("t2bb.job418", '%s/yeshaq//ICF/automated/2012_09_26_22_52_33/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs                                                  
susy17.add("T1tttt", '%s/yeshaq//ICF/automated/2012_10_04_23_15_25/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("t1bbbb.job443", '%syeshaq//ICF/automated/2012_10_04_22_34_28/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs                                                  
susy17.add("T1", '%s/yeshaq//ICF/automated/2012_10_04_23_04_08/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("T2tt", '%s/yeshaq//ICF/automated/2012_10_04_22_47_35/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("T2", '%s/yeshaq//ICF/automated/2012_10_06_13_53_17/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs

susy17.add("T2bb_mrst", '%s/yeshaq//ICF/automated/T2bb/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("T1bbbb_mrst", '%s/yeshaq//ICF/automated/t1bbbb/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs

susy17.add("T2bb", '%s/yeshaq//ICF/automated/T2bb_mstw_2/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("T1bbbb", '%s/yeshaq//ICF/automated/t1bbbb_mstw_2/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs

susy17.add("T2bb_nnpdf", '%s/yeshaq//ICF/automated/2012_11_27_14_01_59/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("T1bbbb_nnpdf", '%s/yeshaq//ICF/automated/2012_11_27_14_24_14/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs

susy17.add("T2bw", '%s/clucas//ICF/automated/2012_11_07_13_30_21/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("T1bbbb_nnpdf_ct10", '%s/yeshaq//ICF/automated/2012_12_03_10_43_11/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("T2bb_nnpdf_ct10", '%s/yeshaq//ICF/automated/2012_12_03_14_42_35/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs

susy17.add("T2cc_nnpdf_ct10", '%s/clucas//ICF/automated/2013_01_27_11_07_05/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
susy17.add("T2cc_nnpdf_ct10_2J", '%s/clucas//ICF/automated/2013_02_13_12_36_49/")'%pnfs, xs = {"LO":107.5}["LO"]) #dummy xs
