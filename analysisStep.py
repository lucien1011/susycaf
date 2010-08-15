from bisect import bisect
#####################################
class analysisStep(object) :
    """generic analysis step"""

    nPass=0
    nFail=0
    nTotal=0
    integerWidth=10
    docWidth=30
    moreWidth=40
    moreName=""
    moreName2=""
    skimmerStepName="skimmer"
    displayerStepName="displayer"
    jsonMakerStepName="jsonMaker"

    ignoreInAccounting=False
    disabled=False
    quietMode=False
    splitMode=False
    needToConsiderPtHatThresholds=False
    
    def go(self,eventVars) :
        self.nTotal+=1

        if self.disabled :
            self.nPass+=1
            return True
        
        if self.selectNotImplemented :
            self.nPass+=1
            if self.uponAcceptanceImplemented :
                self.uponAcceptance(eventVars)
            return True

        if self.select(eventVars) :
            self.nPass+=1
            if self.uponAcceptanceImplemented :
                self.uponAcceptance(eventVars)
            return True
        else :
            self.nFail+=1
            if self.uponRejectionImplemented :
                self.uponRejection(eventVars)
            return False

    def name(self) :
        return self.__doc__.ljust(self.docWidth)+self.moreName.ljust(self.moreWidth)

    def name2(self) :
        return "" if self.moreName2=="" else "\n"+"".ljust(self.docWidth)+self.moreName2.ljust(self.moreWidth)

    def disable(self) :
        self.disabled=True
        
    def ignore(self) :
        self.ignore=True
        
    def makeQuiet(self) :
        self.quietMode=True
        
    def setSplitMode(self) :
        self.splitMode=True
        
    def printStatistics(self) :
        passString="-" if self.disabled else str(self.nPass)
        failString="-" if self.disabled else str(self.nFail)

        statString = "" if not hasattr(self,"select") else \
                     "  %s %s" % ( passString.rjust(self.integerWidth), ("("+failString+")").rjust(self.integerWidth+2) )
        print "%s%s%s" % (self.name(),self.name2(),statString)

    def book(self,eventVars) :
        if not self.needToConsiderPtHatThresholds :
            return self.books[None]
        else :
            if not eventVars["genGenInfoHandleValid"] :
                raise Exception("pt hat is needed but its handle is not valid")
            index=bisect(self.ptHatThresholds,eventVars["genpthat"])
            return self.books[index]
#####################################
