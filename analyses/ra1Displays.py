import supy,steps,calculables,samples
import ROOT as r

class ra1Displays(supy.analysis) :
    def useCachedFileLists(self) : return False
    
    def parameters(self) :
        objects = self.vary()
        fields =                           [ "jet",                        "jetId",     "muonsInJets",           "met",      "rechit",
                                             "compJet",                "compJetId", "compMuonsInJets",        "compMet", "compRechit",
                                             "muon",                    "electron",          "photon"]

        objects["calo"] = dict(zip(fields, [("xcak5Jet","Pat"),       "JetIDloose",             False,   "metP4TypeIPF",       "Calo",
                                            ("xcak5JetPF","Pat"),     "JetIDtight",              True,   "metP4TypeIPF",         "PF",
                                            ("muon","Pat"),     ("electron","Pat"),  ("photon","Pat")]))

        return { "objects": objects,
                 "nJetsMinMax" :      self.vary(dict([ ("ge2",(2,None)),  ("2",(2,2)),  ("ge3",(3,None)),  ("3",(3,3)), ("e23",(2,3)), ("ge4",(4,None))][4:5] )),
                 "nBTagJets":         self.vary(dict([ ("nbe0",(0,0)),  ("nbe1",(1,1)),  ("nbe2",(2,2)),  ("nbe3",(3,3)),  ("nbge4",(4,None)) ][0:1] )),
                 "etRatherThanPt" : True,
                 "lowPtThreshold" : 30.0,
                 "lowPtName" : "lowPt",
                 "highPtThreshold" : 50.0,
                 "highPtName" : "highPt",
                 "thresholds": self.vary(dict( [("375",        (375.0, None,  100.0, 50.0)),#0
                                                ("325_scaled", (325.0, 375.0,  86.7, 43.3)),#1
                                                ("275_scaled", (275.0, 325.0,  73.3, 36.7)),#2
                                                ("875", (875.0, None,  100.0, 50.0)),#3
                                                ][3:4] )),
                 }

    def calcListJet(self, obj, etRatherThanPt, ptMin, lowPtThreshold, lowPtName, highPtThreshold, highPtName, htThreshold) :
        def calcList(jet, met, photon, muon, electron, muonsInJets, jetIdFlag) :
            print "WARNING: synchronize muon addition"
            outList = [
                calculables.xclean.xcJet(jet,
                                         gamma = photon,
                                         gammaDR = 0.5,
                                         muon = muon,
                                         muonDR = 0.5,
                                         #correctForMuons = not muonsInJets,
                                         correctForMuons = False,
                                         electron = electron,
                                         electronDR = 0.5),
                calculables.jet.Indices( jet, ptMin = ptMin,           etaMax = 3.0, flagName = jetIdFlag),
                calculables.jet.Indices( jet, ptMin = lowPtThreshold,  etaMax = 3.0, flagName = jetIdFlag, extraName = lowPtName),
                calculables.jet.Indices( jet, ptMin = highPtThreshold, etaMax = 3.0, flagName = jetIdFlag, extraName = highPtName),
                calculables.jet.IndicesBtagged2(jet, tag = "CombinedSecondaryVertexBJetTags", threshold = 0.679),
                calculables.jet.SumP4(jet),
                calculables.jet.SumP4(jet, extraName = lowPtName),
                calculables.jet.SumP4(jet, extraName = highPtName),
                calculables.jet.SumP4(jet, extraName = "Btagged2"),
                calculables.jet.DeltaPhiStar(jet, extraName = lowPtName),
                calculables.jet.DeltaPseudoJet(jet, etRatherThanPt),
                calculables.jet.MaxEmEnergyFraction(jet),
                calculables.jet.AlphaT(jet, etRatherThanPt),
                calculables.jet.AlphaTMet(jet, etRatherThanPt, met),
                calculables.jet.MhtOverMet((jet[0], highPtName+jet[1]), met),
                calculables.jet.DeadEcalDR(jet, extraName = lowPtName, minNXtals = 10),
                supy.calculables.other.fixedValue("%sFixedHtBin%s"%jet, htThreshold),
                ]
            return outList+supy.calculables.fromCollections(calculables.jet, [jet])

        outList = calcList(obj["jet"], obj["met"], obj["photon"], obj["muon"], obj["electron"], obj["muonsInJets"], obj["jetId"])
        if all([("comp"+item in obj) for item in ["Jet", "Met","MuonsInJets","JetId"]]) :
            outList += calcList(obj["compJet"], obj["compMet"], obj["photon"], obj["muon"], obj["electron"], obj["compMuonsInJets"], obj["compJetId"])
        return outList

    def calcListOther(self, obj) :
        return [
            calculables.xclean.IndicesUnmatched(collection = obj["photon"], xcjets = obj["jet"], DR = 0.5),
            calculables.xclean.IndicesUnmatched(collection = obj["electron"], xcjets = obj["jet"], DR = 0.5),

            calculables.muon.Indices( obj["muon"], ptMin = 10, isoMax = 0.20, ISO = "PfIsolationR04DeltaBCorrected", ID = "IdPog2012Tight"),
            calculables.electron.Indices( obj["electron"], ptMin = 10, flag2012 = "Veto"),
            calculables.photon.Indices(obj["photon"], ptMin = 25, flagName = "photonIDRA3Pat"),
            calculables.photon.CombinedIsoDR03RhoCorrected(obj["photon"]),

            calculables.other.RecHitSumPt(obj["rechit"]),
            calculables.other.RecHitSumP4(obj["rechit"]),

            calculables.other.RecHitSumPt(obj["compRechit"]),
            calculables.other.RecHitSumP4(obj["compRechit"]),
            calculables.vertex.ID(),
            calculables.vertex.Indices(),
            ]
    
    def listOfCalculables(self, params) :
        obj = params["objects"]
        outList = []
        outList += supy.calculables.zeroArgs(supy.calculables)
        outList += supy.calculables.zeroArgs(calculables)
        outList += supy.calculables.fromCollections(calculables.muon, [obj["muon"]])
        outList += supy.calculables.fromCollections(calculables.electron, [obj["electron"]])
        outList += supy.calculables.fromCollections(calculables.photon, [obj["photon"]])
        outList += self.calcListOther(obj)
        outList += self.calcListJet(obj, params["etRatherThanPt"], params["thresholds"][3],
                                    params["lowPtThreshold"], params["lowPtName"], params["highPtThreshold"], params["highPtName"], params["thresholds"][0])
        return outList
    
    def listOfSteps(self, params) :
        return [
            supy.steps.printer.progressPrinter(),
            supy.steps.filters.value("%sSumEt%s"%params["objects"]["jet"], min = params["thresholds"][0]),
            supy.steps.filters.value("%sSumEt%s"%params["objects"]["jet"], max = params["thresholds"][1]),
            supy.steps.filters.multiplicity("%sIndicesBtagged2%s"%params["objects"]["jet"], min = params["nBTagJets"][0], max = params["nBTagJets"][1]),
            supy.steps.filters.multiplicity("%sIndices%s"%params["objects"]["jet"], min = params["nJetsMinMax"][0], max = params["nJetsMinMax"][1]),
            supy.steps.filters.value("%sRecHitSumPt"%params["objects"]["rechit"], max = 30.0),
            #supy.steps.filters.value("%sMaxEmEnergyFraction%s"%params["objects"]["jet"], min = .1),
            steps.displayer.displayer(jets      = params["objects"]["jet"],
                                      muons     = params["objects"]["muon"],
                                      met       = params["objects"]["met"],
                                      electrons = params["objects"]["electron"],
                                      photons   = params["objects"]["photon"],
                                      recHits   = params["objects"]["rechit"], recHitPtThreshold = 1.0,#GeV
                                      scale = 400.0,#GeV
                                      etRatherThanPt = params["etRatherThanPt"],
                                      deltaPhiStarExtraName = params["lowPtName"],
                                      deltaPhiStarCut = 0.5,
                                      deltaPhiStarDR = 0.3,
                                      j2Factor = params["thresholds"][2]/params["thresholds"][0],
                                      mhtOverMetName = "%sMht%sOver%s"%(params["objects"]["jet"][0], params["highPtName"]+params["objects"]["jet"][1], params["objects"]["met"]),
                                      metOtherAlgo  = params["objects"]["compMet"],
                                      jetsOtherAlgo = params["objects"]["compJet"],
                                      recHitsOtherAlgo = params["objects"]["compRechit"],
                                      #doGenJets = True,
                                      prettyMode = True,
                                      ),
            ]
    
    def listOfSampleDictionaries(self) :
        sampleDict = supy.samples.SampleHolder()
        #sampleDict.add("MT2_events", '["/home/hep/bm409/public_html/MT2Skim.root"]', lumi = 600)
        #sampleDict.add("Data_375", '["/home/hep/elaird1/73_candidates/v8/375.root"]', lumi = 1.1e3)
        #sampleDict.add("Data_375", '["/home/hep/elaird1/73_candidates/v9/HT_375_skim_27fb.root"]', lumi = 2.7e3)
        #sampleDict.add("T2_skim", '["/home/hep/db1110/public_html/Simplified_Models/T2_testpoint_results/T2_skims/T2_testpoint_200_175.root"]', xs = 1.0)
        #sampleDict.add("Data_275", '["/home/hep/db1110/public_html/AnalysisSkims/DefaultAnalysisSkims/275-325/Dataskims/275data.root"]', lumi = 602.) #/pb
        #sampleDict.add("MG_QCD", '["/home/hep/db1110/public_html/AnalysisSkims/DefaultAnalysisSkims/275-325/MCskims/275madgraph.root"]', xs = 1.0) #dummy xs
        #sampleDict.add("PY_QCD", '["/home/hep/db1110/public_html/AnalysisSkims/DefaultAnalysisSkims/275-325/AlphaT54MCSkims/275Pythia.root"]', xs = 1.0) #dummy xs
        #sampleDict.add("py_qcd_375", '["/home/hep/elaird1/87_qcd_hunt/02_ht375/py6/skims_alphaT.gt.0.55/all.root"]', xs = 1.0) #dummy xs
        sampleDict.add("Data_4bJets1", '["/uscms/home/yeshaq/work/susycaf/4bjets/SusyCAF_Tree_1.root"]', lumi = 1.1e3)
        sampleDict.add("Data_4bJets2", '["/uscms/home/yeshaq/work/susycaf/4bjets/SusyCAF_Tree_2.root"]', lumi = 1.1e3)
        sampleDict.add("Data_4bJets3", '["/uscms/home/yeshaq/work/susycaf/4bjets/SusyCAF_Tree_3.root"]', lumi = 1.1e3)
        sampleDict.add("Data_4bJets", '["/uscms/home/yeshaq/work/susycaf/4bjets/SusyCAF_Tree_1.root","/uscms/home/yeshaq/work/susycaf/4bjets/SusyCAF_Tree_2.root","/uscms/home/yeshaq/work/susycaf/4bjets/SusyCAF_Tree_3.root"]', lumi = 1.1e3)
        sampleDict.add("MC_4bJets1", '["/uscms/home/yeshaq/work/susycaf/4bjets/MC/TTJets/SusyCAF_Tree_1.root"]', lumi = 1.1e3)
        sampleDict.add("MC_4bJets2", '["/uscms/home/yeshaq/work/susycaf/4bjets/MC/TTJets/SusyCAF_Tree_2.root"]', lumi = 1.1e3)
        sampleDict.add("MC_4bJets3", '["/uscms/home/yeshaq/work/susycaf/4bjets/MC/TTJets/SusyCAF_Tree_3.root"]', lumi = 1.1e3)
        sampleDict.add("MC_4bJets4", '["/uscms/home/yeshaq/work/susycaf/4bjets/MC/Zinv/SusyCAF_Tree.root"]', lumi = 1.1e3)        
        sampleDict.add("Data_High_HT", '["~/nobackup/supy-output/hadronicLook/375_ge2_caloAK5JetMet_recoLepPhot_pythia6/High_HT_skim.root"]', lumi = 1.1e3)
        sampleDict.add("Data_375_ge2", '["~/nobackup/supy-output/hadronicLook/375_calo_ge2/HadronicRegion.root"]', lumi = 1.1e3)
        sampleDict.add("Data_875_ge2_Darren", '["~/nobackup/supy-output/hadronicLook/375_calo_ge2/Had_875_Skim_fromDarren.root"]', lumi = 1.1e3)
        return [sampleDict]
    
    def listOfSamples(self,params) :
        #return supy.samples.specify(names = ["Data_875_ge2_Darren"])
        return supy.samples.specify(names = ["Data_375_ge2"])
