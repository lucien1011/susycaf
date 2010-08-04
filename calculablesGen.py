from wrappedChain import wrappedChain
##############################
class genParticleCounter(wrappedChain.calculable) :
    def name(self) : return "GenParticleCategoryCounts"

    def __init__(self) :
        self.pdgToCategory={}
        #copied from PDG
        self.initPdgToCategory(1000001,1000004,"squarkL")#left-handed
        self.initPdgToCategory(1000005,1000006,"squarkA")#ambiguous
        self.initPdgToCategory(1000011,1000016,"slepton")
        self.initPdgToCategory(2000001,2000004,"squarkR")#right-handed
        self.initPdgToCategory(2000005,2000006,"squarkA")#ambiguous
        self.initPdgToCategory(2000011,2000011,"slepton")
        self.initPdgToCategory(2000013,2000013,"slepton")
        self.initPdgToCategory(2000015,2000015,"slepton")
        self.initPdgToCategory(1000021,1000021,"gluino")
        self.initPdgToCategory(1000022,1000023,"chi0")
        self.initPdgToCategory(1000024,1000024,"chi+")
        self.initPdgToCategory(1000025,1000025,"chi0")
        self.initPdgToCategory(1000035,1000035,"chi0")
        self.initPdgToCategory(1000037,1000037,"chi+")
        self.initPdgToCategory(1000039,1000039,"gravitino")

        self.combineCategories(["squarkL","squarkR","squarkA"],"squark")
        self.combineCategories(["slepton","chi0","chi+","gravitino"],"other name")

        self.badCategoryName="no name"
        self.categories=list(set(self.pdgToCategory.values()))
        self.categories.append(self.badCategoryName)
        self.categories.sort()
        #self.printDict(self.pdgToCategory)

    def initPdgToCategory(self,lower,upper,label) :
        for i in range(lower,upper+1) :
            self.pdgToCategory[i]=label
        for i in range(-upper,-lower+1) :
            self.pdgToCategory[i]=label

    def combineCategories(self,someList,someLabel) :
        for key in self.pdgToCategory :
            if self.pdgToCategory[key] in someList :
                self.pdgToCategory[key]=someLabel
        
    def printDict(self,someDict) :
        for key in someDict :
            print key,someDict[key]

    def zeroCategoryCounts(self) :
        for key in self.categories :
            selv.value[key]=0

    def isSusy(self,pdgId) :
        reducedPdgId=abs(pdgId)/1000000
        #if (reducedPdgId==2) : print "isSusy(",pdgId,"):",reducedPdgId,reducedPdgId==1 or reducedPdgId==2
        return reducedPdgId==1 or reducedPdgId==2

    def incrementCategory(self,pdgId) :
        if pdgId in self.pdgToCategory:
            category=self.pdgToCategory[pdgId]
        else :
            category=self.badCategoryName
        self.value[category]+=1
        #print "found one:",iParticle,pdgId

    def update(self,ignored) :
        self.zeroCategoryCounts()

        if not self.source["genHandleValid"] : return
        #print dir(self.source)
        nParticles=len(self.source["genPdgId"])
        for iParticle in range(nParticles) :
            #consider only status 3 particles
            if self.source["genStatus"].at(iParticle)!=3 : continue
            #which are SUSY particles
            if not self.isSusy(self.source["genPdgId"].at(iParticle)) : continue
            #which have mothers
            if not self.source["genHasMother"].at(iParticle) : continue
            #which are stored
            if not self.source["genMotherStored"].at(iParticle) : continue
            motherIndex=self.source["genMother"].at(iParticle)
            if (motherIndex<0) : continue
            #and are not SUSY particles
            if self.isSusy(self.source["genPdgId"].at(motherIndex)) : continue
        
            pdgId=self.source["genPdgId"].at(iParticle)
            self.incrementCategory(pdgId)
##############################
