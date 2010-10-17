from wrappedChain import *
import math,calculables

def xcStrip(collection) :
    return (collection[0].lstrip("xc"),collection[1])
##############################
class jetIndicesModified(wrappedChain.calculable) :
    def name(self) : return "%sIndicesModified%s"%self.cs

    def __init__(self, collection = None) :
        self.cs = collection
        self.indices = "%sIndices%s"%self.cs
        self.xcP4 = "%sCorrectedP4%s"%self.cs
        self.p4 = self.xcP4[2:]
        self.moreName = "%s differs from %s"%(self.p4,self.xcP4)

    def differentP4(self,i) : return self.source[self.p4][i] != self.source[self.xcP4][i]
        
    def update(self,ignored) :
        self.value = filter(self.differentP4, self.source[self.indices])
##############################
class jetIndicesKilled(wrappedChain.calculable) :
    def name(self) : return "%sIndicesKilled%s"%self.cs
    
    def __init__(self, collection = None) :
        self.cs = collection
        self.moreName = "removed from consideration; gamma,e match or jetkill study"

    def update(self,ignored) : self.value = set()
##############################
class jetIndicesOther(calculables.indicesOther) :
    def __init__(self, collection = None) :
        super(jetIndicesOther, self).__init__(collection)
        self.moreName = "pass ptMin; fail jetID or etaMax"
##############################
class jetIndices(wrappedChain.calculable) :
    def name(self) : return self.indices
    
    def __init__(self, collection = None, ptMin = None, etaMax = None, flagName = None, extraName = ""):
        self.extraName = extraName
        self.indices = "%sIndices%s%s"      % (collection[0],collection[1],extraName)
        self.other = "%sIndicesOther%s%s"   % (collection[0],collection[1],extraName)
        self.killed = "%sIndicesKilled%s%s" % (collection[0],collection[1],extraName)
        self.p4s = '%sCorrectedP4%s' % collection
        self.pt2Min = ptMin*ptMin
        self.etaMax = etaMax
        self.flag = None if not flagName else \
                    ( "%s"+flagName+"%s" if xcStrip(collection)[0][-2:] != "PF" else \
                      "%sPF"+flagName+"%s" ) % xcStrip(collection)
        self.moreName = "pT>=%.1f GeV; |eta|<%.1f; %s"% (ptMin, etaMax, flagName if flagName else "")

    def update(self,ignored) :
        self.value = []
        other  = self.source[self.other]  if self.extraName=="" else []
        killed = self.source[self.killed] if self.extraName=="" else []
        jetIds = self.source[self.flag] if self.flag else p4s.size()*[1]
        p4s    = self.source[self.p4s]
        pt2s    = []

        for i in range(p4s.size()) :
            pt2 = p4s.at(i).Perp2()
            pt2s.append(pt2)
            if pt2 < self.pt2Min or i in killed: continue
            elif jetIds[i] and abs(p4s.at(i).eta()) < self.etaMax :
                self.value.append(i)
            else: other.append(i)
        self.value.sort( key = pt2s.__getitem__, reverse = True)
####################################
class PFJetID(wrappedChain.calculable) :
    def name(self) : return self.idName
    
    # following http://indico.cern.ch/getFile.py/access?contribId=0&resId=0&materialId=slides&confId=97994
    def __init__(self, collection = None, level = None) :
        self.cs = xcStrip(collection)
        self.idName = "%sPFJetID%s%s" % (self.cs[0],level,self.cs[1])
        self.p4Name = "%sCorrectedP4%s" % self.cs
        for var in ["FneutralHad","FneutralEm","FchargedHad","FchargedEm","Ncharged","Nneutral"] :
            setattr(self,var, ("%s"+var+"%s")%xcStrip(self.cs))

        i = ["loose","medium","tight"].index(level)
        self.fNhMax   = [0.99, 0.95, 0.90][i]
        self.fNeMax   = [0.99, 0.95, 0.90][i]
        self.nMin     = [2,    2,    2   ][i]
        self.etaDiv       = 2.4
        self.fChMin   = [0.0,  0.0,  0.0 ][i]
        self.fCeMax   = [0.99, 0.99, 0.99][i] 
        self.nCMin    = [1,    1,    1   ][i]     

        self.moreName = "fN_had<%.2f; fN_em<%.2f; nC+nN>=%d;"% \
                        ( self.fNhMax, self.fNeMax, self.nMin) 
        self.moreName2 = "|eta|>2.4 or {fC_had>%.2f; fC_em <%.2f; nC>%d}" % \
                         (self.fChMin, self.fCeMax, self.nCMin )

    def update(self,ignored) :
        self.value = map(self.passId, 
                         self.source[self.p4Name],
                         self.source[self.FneutralHad],
                         self.source[self.FneutralEm],
                         self.source[self.FchargedHad],
                         self.source[self.FchargedEm],
                         self.source[self.Nneutral],
                         self.source[self.Ncharged] )

    def passId(self, p4, fNh, fNe, fCh, fCe, nN, nC ) :
        return fNh    < self.fNhMax and \
               fNe    < self.fNeMax and \
               nN+nC >= self.nMin   and \
               ( abs(p4.eta()) > self.etaDiv or \
                 fCh > self.fChMin  and \
                 fCe < self.fCeMax  and \
                 nC >= self.nCMin )
class PFJetIDloose(PFJetID) :
    def __init__(self, collection = None) :
        super(PFJetIDloose,self).__init__(collection,"loose")
class PFJetIDmedium(PFJetID) :
    def __init__(self, collection = None) :
        super(PFJetIDmedium,self).__init__(collection,"medium")
class PFJetIDtight(PFJetID) :
    def __init__(self, collection = None) :
        super(PFJetIDtight,self).__init__(collection,"tight")
#############################
class leadingJetPt(wrappedChain.calculable) :
    def name(self) : return "%sLeadingPt%s"% self.cs

    def __init__(self, collection = None) :
        self.cs = collection
        self.p4Name = '%sCorrectedP4%s' % self.cs
        self.indicesName = "%sIndices%s" % self.cs

    def update(self,ignored) :
        p4s = self.source[self.p4Name]
        indices = self.source[self.indicesName]
        self.value = p4s.at(indices[0]).pt() if len(indices) else None
##############################
class jetSumPt(wrappedChain.calculable) :
    def name(self) : return "%sSumPt%s"% self.cs

    def __init__(self, collection = None) :
        self.cs = collection
        self.p4Name = '%sCorrectedP4%s' % self.cs
        self.indicesName = "%sIndices%s" % self.cs

    def update(self,ignored) :
        p4s = self.source[self.p4Name]
        indices = self.source[self.indicesName]
        self.value = reduce( lambda x,i: x+p4s.at(i).pt(), indices , 0)
##############################
class jetSumEt(wrappedChain.calculable) :
    def name(self) : return "%sSumEt%s"% self.cs

    def __init__(self, collection = None) :
        self.cs = collection
        self.p4Name = '%sCorrectedP4%s' % self.cs
        self.indicesName = "%sIndices%s" % self.cs

    def update(self,ignored) :
        p4s = self.source[self.p4Name]
        indices = self.source[self.indicesName]
        self.value = reduce( lambda x,i: x+p4s.at(i).Et(), indices , 0)
##############################
class jetSumP4(wrappedChain.calculable) :
    def name(self) : return "%sSumP4%s" % self.cs

    def __init__(self, collection = None, mcScaleFactor = None) :
        self.cs = collection
        self.p4Name = '%sCorrectedP4%s' % self.cs
        self.indicesName = "%sIndices%s" % self.cs
        self.mcScaleFactor = mcScaleFactor

    def update(self,ignored) :
        p4s = self.source[self.p4Name]
        indices = self.source[self.indicesName]
        self.value = reduce( lambda x,i: x+p4s.at(i), indices[1:], p4s.at(indices[0]) ) if len(indices) else None

        if "genpthat" not in self.source or not self.value : return
        #for MC only
        self.value *= self.mcScaleFactor
        ht = self.source["%sSumPt%s"%self.cs]
        if self.value.pt()>ht :
            self.value *= 0.99*ht / self.value.pt()
##############################
class jetSumP4Low(wrappedChain.calculable) :
    def name(self) : return "%sSumP4Low%s" % self.cs

    def __init__(self, collection = None, ptMin = None) :
        self.cs = collection
        self.p4Name = '%sCorrectedP4%s' % self.cs
        self.ptMin = ptMin
        self.moreName = "jets with pT>%.1f GeV"%self.ptMin
        
    def update(self,ignored) :
        p4s = self.source[self.p4Name]
        size = p4s.size()
        self.value = reduce( lambda x,i: x+p4s.at(i) if p4s.at(i).pt() > self.ptMin else x, range(1,size), p4s.at(0) ) if size>0 else None
##############################
class deltaPseudoJet(wrappedChain.calculable) :
    def name(self) : return self.nameString

    def __init__(self, collection = None, etRatherThanPt = None) :
        self.etRatherThanPt = etRatherThanPt
        self.cs = collection
        self.p4Name = '%sCorrectedP4%s' % self.cs
        self.indicesName = "%sIndices%s" % self.cs
        self.nameString = "%sDeltaPseudoJetPt%s" % self.cs if not self.etRatherThanPt else "%sDeltaPseudoJetEt%s" % self.cs
        
    def update(self,ignored) :
        indices = self.source[self.indicesName]
        p4s = self.source[self.p4Name]
        
        size = len(indices)
        diff = [0.] * (1<<size)
        for j in indices :
            pt = p4s.at(j).pt() if not self.etRatherThanPt else p4s.at(j).Et()
            for i in range( len(diff) ) :
                diff[i] += pt * (1|-(1&(i>>j)))
        
        self.value = min([abs(d) for d in diff])
##############################
class alphaT(wrappedChain.calculable) :
    def name(self) : return "%sAlphaT%s" % self.cs

    def __init__(self, collection = None, etRatherThanPt = None) :
        self.cs = collection
        self.etRatherThanPt = etRatherThanPt
        self.sumP4Name = "%sSumP4%s" % self.cs
        self.sumPtName = "%sSumPt%s" % self.cs
        self.sumEtName = "%sSumEt%s" % self.cs
        self.deltaPseudoName = "%sDeltaPseudoJetPt%s" % self.cs if not self.etRatherThanPt else "%sDeltaPseudoJetEt%s" % self.cs

    def update(self,ignored) :
        sumP4   = self.source[self.sumP4Name]
        dPseudo = self.source[self.deltaPseudoName]
        ht = self.source[self.sumPtName] if not self.etRatherThanPt else self.source[self.sumEtName]
        self.value = 0.5 * ( ht - dPseudo ) / math.sqrt( ht*ht - sumP4.Perp2() ) 
##############################
class alphaTMet(wrappedChain.calculable) :
    def name(self) : return "%sAlphaTMet%s" % self.cs

    def __init__(self, collection = None, etRatherThanPt = None, metName = None) :
        self.cs = collection
        self.etRatherThanPt = etRatherThanPt
        self.metName = metName
        self.sumPtName = "%sSumPt%s" % self.cs
        self.sumEtName = "%sSumEt%s" % self.cs
        self.deltaPseudoName = "%sDeltaPseudoJetPt%s" % self.cs if not self.etRatherThanPt else "%sDeltaPseudoJetEt%s" % self.cs
        self.truncFactor = 0.99
        self.moreName = "met**2 < ht**2 or met**2 = %.2f * ht**2"%self.truncFactor

    def update(self,ignored) :
        ht = self.source[self.sumPtName] if not self.etRatherThanPt else self.source[self.sumEtName]
        met2 = self.source[self.metName].Perp2()
        ht2 = ht*ht
        if met2>ht2 :
            met2= ht2*self.truncFactor
        dPseudo = self.source[self.deltaPseudoName]
        self.value = 0.5 * ( ht - dPseudo ) / math.sqrt( ht2 - met2 )
##############################
class diJetAlpha(wrappedChain.calculable) :
    def name(self) : return "%sDiJetAlpha%s" % self.cs
    
    def __init__(self,collection = None) :
        self.cs = collection
        self.indicesName = "%sIndices%s" % self.cs
        self.p4Name = '%sCorrectedP4%s' % self.cs
        
    def update(self,ignored) :
        cleanJetIndices = self.source[self.indicesName]
        #return if not dijet
        if len(cleanJetIndices)!=2 :
            self.value=None
            return
        p4s=self.source[self.p4Name]
        mass=(p4s.at(cleanJetIndices[0])+p4s.at(cleanJetIndices[1])).M()
        if mass<=0.0 :
            self.value=None
        else :
            self.value=p4s.at(cleanJetIndices[1]).pt()/mass
##############################
class jetDeltaX01(wrappedChain.calculable) :
    def name(self) : return "%sDeltaX01%s" % self.cs

    def __init__(self,collection = None) :
        self.cs = collection
        self.indicesName = "%sIndices%s" % self.cs
        self.p4Name = '%sCorrectedP4%s' % self.cs
        
    def update(self,ignored) :
        self.value={}
        
        indices = self.source[self.indicesName]
        if len(indices)<2 :
            self.value["phi"]=None
            self.value["eta"]=None
            self.value["R"]=None
            return
        p4s=self.source[self.p4Name]
        jet0=p4s.at(indices[0])
        jet1=p4s.at(indices[1])
        self.value["phi"] = r.Math.VectorUtil.DeltaPhi(jet0,jet1)
        self.value["R"  ] = r.Math.VectorUtil.DeltaR(jet0,jet1)
        self.value["eta"] = jet0.eta()-jet1.eta()
##############################
class deltaPhiStar(wrappedChain.calculable) :
    def name(self) : return "%sDeltaPhiStar%s"%self.cs

    def __init__(self, collection = None, ptMin = None, extraName = None) :
        self.cs = collection
        self.ptMin = ptMin
        self.p4Name = '%sCorrectedP4%s' % self.cs
        self.indicesName = '%sIndices%s%s' % (self.cs[0],self.cs[1],extraName)
        self.sumP4Name = "%sSumP4%s" % self.cs
        self.moreName = "pT>%.1f GeV"%self.ptMin
        
    def update(self,ignored) :
        self.value=None

        indices = self.source[self.indicesName]
        if not len(indices) : return
        jets = self.source[self.p4Name]
        sumP4 = self.source[self.sumP4Name]

        self.value = {}
        self.value["DeltaPhiStar"] = None
        self.value["DeltaPhiStarJetIndex"] = None
        dPhi = []
        for i in indices :
            if jets.at(i).pt()<self.ptMin : continue
            dPhi.append( (abs(r.Math.VectorUtil.DeltaPhi(jets.at(i),jets.at(i)-sumP4)),i) )
        if len(dPhi) :
            self.value["DeltaPhiStar"],self.value["DeltaPhiStarJetIndex"] = min(dPhi)
##############################
class maxProjMHT(wrappedChain.calculable) :
    def name(self) : return "%sMaxProjMHT%s"%self.cs

    def __init__(self,collection = None) :
        self.cs = collection
        self.p4Name = '%sCorrectedP4%s' % self.cs
        self.indicesName = '%sIndices%s' % self.cs
        self.sumP4Name = "%sSumP4%s" % self.cs

    def update(self,ignored) :
        self.value = None

        indices = self.source[self.indicesName]
        if not len(indices) : return
        jets = self.source[self.p4Name]
        sumP4 = self.source[self.sumP4Name]

        self.value = -min( [ sumP4.pt() / math.sqrt(jets.at(i).pt()) * \
                             math.cos(r.Math.VectorUtil.DeltaPhi(jets.at(i),sumP4)) for i in indices])
#####################################
class metPlusPhoton(wrappedChain.calculable) :

    def __init__(self, met, photons, photonIndex) :
        self.met = met
        self.photons = photons
        self.photonIndex = photonIndex
        self.moreName = "%s + %s%s[index[%d]]"%(self.met, self.photons[0], self.photons[1], self.photonIndex)
        
    def update(self, ignored) :
        index = self.source["%sIndices%s"%self.photons][self.photonIndex]
        self.value = self.source[self.met] + self.source["%sP4%s"%self.photons].at(index)
#####################################
class mhtMinusMetOverMeff(wrappedChain.calculable) :

    def __init__(self, jets, met, etRatherThanPt) :
        self.jets = jets
        self.met = met
        self.etRatherThanPt = etRatherThanPt
        self.moreName = "%s%s; %s; %s"%(self.jets[0], self.jets[1], self.met, "ET" if self.etRatherThanPt else "pT")
        self.mht = "%sSumP4%s"%self.jets
        self.ht  = "%sSumEt%s"%self.jets if self.etRatherThanPt else "%sSumPt%s"%self.jets
        
    def update(self, ignored) :
        mht = self.source[self.mht].pt()
        self.value = (mht - self.source[self.met].pt())/(self.source[self.ht] + mht)
#####################################
class ecalDeadTowerMatchedJetIndices(wrappedChain.calculable) :
    def name(self) : return "ecalDeadTowerMatched%sIndices%s"%self.cs

    def __init__(self, collection) :
        self.cs = collection
        self.moreName = "tp.Et()>0, dR(tp,%s%s)<0.5"%self.cs

    def matchingJetIndex(self,tpP4) :
        jetP4s = self.source["%sCorrectedP4%s"%self.cs]
        for i in self.source["%sIndices%s"%self.cs] :
            p4= jetP4s[i]
            ptetaphieV4 = r.Math.PtEtaPhiEVector(p4.pt(),p4.eta(),p4.phi(),p4.E())
            if r.Math.VectorUtil.DeltaR(tpP4,ptetaphieV4) < 0.5:
                return i
        return -1

    def update(self,ignored) :
        self.value = map(self.matchingJetIndex,self.source["ecalDeadTowerTrigPrimP4"])
