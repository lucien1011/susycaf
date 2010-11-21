import samples

jetmet = samples.SampleHolder()
srm = 'utils.fileListFromSrmLs(location="/pnfs/hep.ph.ic.ac.uk/data/cms/store/user'

#38X SKIMS
jetmet.add("Run2010B_MJ_skim5",
           'utils.fileListFromDisk(location = "/vols/cms02/bbetchar/01_skims/MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Burt3/")', lumi=0.651)#/pb
jetmet.add("Run2010B_MJ_skim4",
           'utils.fileListFromDisk(location = "/vols/cms02/bbetchar/01_skims/MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Robin/")', lumi=12.832)#/pb
jetmet.add("Run2010B_MJ_skim3",
           'utils.fileListFromDisk(location = "/vols/cms02/elaird1/14_skims/MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Bryn/")', lumi = 6.807) #/pb
jetmet.add("Run2010B_MJ_skim2",
           'utils.fileListFromDisk(location = "/vols/cms02/elaird1/14_skims/MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Burt2/")', lumi = 4.1508) #/pb
jetmet.add("Run2010B_MJ_skim",
           'utils.fileListFromDisk(location = "/vols/cms02/elaird1/14_skims/MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Burt/")', lumi = 3.467) #/pb
jetmet.add("Run2010B_J_skim2",
           'utils.fileListFromDisk(location = "/vols/cms02/elaird1/14_skims/Jet.Run2010B-PromptReco-v2.RECO.RAW.Burt2/")', lumi = 0.5107) #/pb
jetmet.add("Run2010B_J_skim",
           'utils.fileListFromDisk(location = "/vols/cms02/elaird1/12_skims/Jet.Run2010B-PromptReco-v2.RECO.RAW.Burt/")', lumi = 3.897) #/pb
jetmet.add("Run2010A_JM_skim",
           'utils.fileListFromDisk(location = "/vols/cms02/elaird1/12_skims/JetMET.Run2010A-Sep17ReReco_v2.RECO.RAW.Burt/")', lumi = 2.889) #/pb
jetmet.add("Run2010A_JMT_skim",
           'utils.fileListFromDisk(location = "/vols/cms02/elaird1/12_skims/JetMETTau.Run2010A-Sep17ReReco_v2.RECO.RAW.Henning/")', lumi = 0.172) #/pb

#38X ORIGINALS
jetmet.add("MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Burt3",    '%s/bbetchar//ICF/automated/2010_11_13_18_52_56/")'%srm,    lumi = 0.651) #/pb
jetmet.add("MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Robin",    '%s/rnandi//ICF/automated/2010_11_05_20_27_38/")'%srm,    lumi = 12.832) #/pb
jetmet.add("MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Bryn",     '%s/bm409//ICF/automated/2010_10_29_17_39_47/")'%srm,    lumi = 6.807) #/pb
jetmet.add("MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Burt2",    '%s/bbetchar//ICF/automated/2010_10_22_17_46_53/")'%srm, lumi = 99999.9 )
jetmet.add("MultiJet.Run2010B-PromptReco-v2.RECO.RAW.Burt",     '%s/bbetchar//ICF/automated/2010_10_18_00_39_32/")'%srm, lumi = 99999.9 )
jetmet.add("Jet.Run2010B-PromptReco-v2.RECO.RAW.Burt2",         '%s/bbetchar//ICF/automated/2010_10_18_00_34_11/")'%srm, lumi = 99999.9 )
jetmet.add("Jet.Run2010B-PromptReco-v2.RECO.RAW.Burt",          '%s/bbetchar//ICF/automated/2010_10_12_09_56_12/")'%srm, lumi = 99999.9 )
jetmet.add("JetMET.Run2010A-Sep17ReReco_v2.RECO.RAW.Burt",      '%s/bbetchar//ICF/automated/2010_10_12_10_01_47/")'%srm, lumi = 99999.9 )
jetmet.add("JetMETTau.Run2010A-Sep17ReReco_v2.RECO.RAW.Henning",'%s/henning//ICF/automated/2010_10_14_11_50_11/")'%srm,  lumi = 99999.9 )

#36X SKIM
jetmet.add("JetMET_skim", 'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/data2/")', lumi = 2.601 ) #/pb

#TEST
jetmet.add("2010_data_calo_skim", 'utils.fileListFromDisk(location = "/vols/cms02/elaird1/11_skims/22_hadronicLook/caloAK5_mix.root", isDirectory = False)', lumi = 34.724)
jetmet.add("2010_data_pf_skim", 'utils.fileListFromDisk(location = "/vols/cms02/elaird1/11_skims/22_hadronicLook/pfAK5_mix.root", isDirectory = False)', lumi = 34.724)
#jetmet.add("2010_data_calo_skim", 'utils.fileListFromDisk(location="/vols/cms02/elaird1/11_skims/22_hadronicLook/caloAK5/")', lumi = 999999.9 ) #/pb
#jetmet.add("2010_data_pf_skim",   'utils.fileListFromDisk(location="/vols/cms02/elaird1/11_skims/22_hadronicLook/pfAK5/")', lumi = 999999.9 ) #/pb
jetmet.add("tanjas7", 'utils.fileListFromDisk(location = "/vols/cms02/elaird1/11_skims/22_hadronicLook/tanjas7.root", isDirectory = False)', lumi = 34.724)
jetmet.add("tanjas14", 'utils.fileListFromDisk(location = "/vols/cms02/elaird1/11_skims/22_hadronicLook/tanjas14.root", isDirectory = False)', lumi = 34.724)
jetmet.add("markus38", 'utils.fileListFromDisk(location = "/vols/cms02/elaird1/11_skims/25_markus38/markus38_0_skim.root", isDirectory = False)', lumi = 34.724)
jetmet.add("toms17", 'utils.fileListFromDisk(location=  "/vols/cms02/elaird1/11_skims/26_tom17/toms17_0_skim.root", isDirectory = False)', lumi = 34.724)
jetmet.add("2010_data_photons_high_met",  'utils.fileListFromDisk(location="/vols/cms02/elaird1/11_skims/08_photons_high_met/")', lumi = 6.68 )
jetmet.add("Tanja_sync",
           'utils.fileListFromDisk(location = "/vols/cms02/elaird1/10_skims/Jet.Run2010B-PromptReco-v2.RECO.Burt2/Jet.Run2010B-PromptReco-v2.RECO.Burt2_[6-9]_skim.root", isDirectory = False)', lumi = 9999999.9) #/pb

