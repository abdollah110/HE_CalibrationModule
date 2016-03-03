import numpy
import ROOT
from ROOT import TCanvas
from ROOT import TFile
from ROOT import TH1F
from ROOT import TF1
from ROOT import TGraph
from ROOT import TPaveText
from array import array
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas


class ADCConverter:
    # Bitmasks for 8-bit ADC input
    expMask = 192
    manMask = 63

    baseSensitivity = 3.1

    # Base charges for each subrange
    # Use array for which 0 ADC = 0 fC input charge
    inputCharge = [
        -1.6, 48.4, 172.4, 433.4, 606.4,
        517, 915, 1910, 3990, 5380,
        4780, 7960, 15900, 32600, 43700,
        38900, 64300, 128000, 261000, 350000
    ]

    #Defines the size of the ADC mantissa subranges
    adcBase = [0, 16, 36, 57, 64]

    # A class to convert ADC to fC
    fc = {}

    def __init__(self):
        # Loop over exponents, 0 - 3
        for exp in xrange(0, 4):
            # Loop over mantissas, 0 - 63
            for man in xrange(0, 64):
                subrange = -1

                # Find which subrange the mantissa is in
                for i in xrange(0, 4):
                    if man >= self.adcBase[i] and man < self.adcBase[i + 1]:
                        subrange = i
                if subrange == -1:
                    print "Something has gone horribly wrong!"

                # Sensitivity = 3.1 * 8^exp * 2^subrange
                sensitivity = self.baseSensitivity * 8.0**float(exp) * 2.0**subrange

                # Add sensitivity * (location in subrange) to base charge
                #fc[exp * 64 + man] = (inputCharge[exp * 5 + subrange] + ((man - adcBase[subrange])) * sensitivity) / gain;
                self.fc[exp * 64 + man] = self.inputCharge[exp * 5 + subrange] + ((man - self.adcBase[subrange]) + .5) * sensitivity

    def linearize(self, adc):
        return self.fc[adc]


adc2fC = ADCConverter()

def getData(f):
    link = 0
    iBin = 0
    event = 0
    valid = False
    totalValid = False
    totalData = []
    dataArray = {}
    tempDataArray = []
    for line in f:
        if "START EVENT" in line:
            if dataArray != {} and totalValid:
                totalData.append(dataArray)
            event = int(line.split()[3].strip("-"))
            totalValid = True
            dataArray = {}
        if "N  RAW0  RAW1" in line or "START EVENT" in line:
            if valid and tempDataArray !=[]:
                dataArray[int(link)] = tempDataArray
            if "N  RAW0  RAW1" in line: link = int(line.split(":")[1])
            iBin = 0
            valid = True
            tempDataArray = []
        if "(Suspicious data format!)" in line:
            valid = False
            totalValid = False
        if "ADC:" in line:
            data = line.split(":")[1]
            datums = data.split()
            linDatum = []
            for datum in datums:
                linDatum.append(adc2fC.linearize(int(datum)))
            tempDataArray.append(linDatum)
            iBin += 1
    return totalData

    #means = {}
    #sumws = {}
    #for event in totalData:
    #    for link in event:
    #        iChan = (link - 15)*6
    #        for chan in xrange(0, 6):
    #            #ped = 0
    #            #for iBin in xrange(20, 50):
    #            #    ped += event[link][iBin][chan]
    #            #ped /= 30.0
    #
    #            if not iChan in means:
    #                means[iChan] = []
    #                sumws[iChan] = 0
    #            for iBin in xrange(0, 99):
    #                #means[iChan] += event[link][iBin][chan] - ped
    #                means[iChan].append(event[link][iBin][chan])
    #            sumws[iChan] += 1.0
    #            iChan += 1
    #
    ##for i in means:
    ##    means[i] /= sumws[i]
    #rmeans = {}
    #for iChan in means:
    #    rmeans[iChan] = numpy.std(means[iChan])
    #return rmeans

def getTDCValues(f):
    link = 0
    iBin = 0
    event = 0
    valid = False
    totalValid = False
    totalData = []
    dataArray = {}
    tempDataArray = []
    for line in f:
        if "START EVENT" in line:
            if dataArray != {}:
                totalData.append(dataArray)
            event = int(line.split()[3].strip("-"))
            totalValid = True
            dataArray = {}
        if "N  RAW0  RAW1" in line:
            if valid:
                dataArray[int(link)] = tempDataArray
            link = int(line.split(":")[1])
            iBin = 0
            valid = True
            tempDataArray = []
        if "(Suspicious data format!)" in line:
            valid = False
            totalValid = False
        if "TDC:" in line:
            data = line.split(":")[1]
            datums = data.split()
            linDatum = []
            for datum in datums:
                linDatum.append(int(datum)/2.0)
            tempDataArray.append(linDatum)
            iBin += 1

    return totalData



#f2 = open("Monday_AMP_0p1_WID_10.txt")
#tdc = getTDCValues(f2)

#event = 0
link = 17 #3, 15,16,17,18,19, or 20
linkChannel = 5 # 0 - 5
#BX = 0







def Measure_Integral(AllRuns, Title, RootName):

    FNumber=len(AllRuns)
    
    xIntegral=array("d",xrange(0,FNumber))
    yIntegral=array("d",xrange(0,FNumber))
    yIntegralErrUp=array("d",xrange(0,FNumber))
    yIntegralErrDown=array("d",xrange(0,FNumber))
    xIntegral_RMS=array("d",xrange(0,FNumber))
    yIntegral_RMS=array("d",xrange(0,FNumber))
    yIntegral_RMSErrUp=array("d",xrange(0,FNumber))
    yIntegral_RMSErrDown=array("d",xrange(0,FNumber))
    xRatio=array("d",xrange(0,FNumber))
    yRatio=array("d",xrange(0,FNumber))
    xSingleEv=array("d",xrange(0,40))
    ySingleEv=array("d",xrange(0,40))
    
    OutFile=TFile(RootName,"RECREATE")
    num=-1
    iAmp=0
    for Fname in AllRuns:
        num+=1
        iAmp+=1

        f = open(Fname)
        data = getData(f)

        M=TH1F(Fname,Fname,600,0,120000)
        x = array("d", xrange(0,1001))
        y = array("d", xrange(0,1001))


        for event in xrange(0,995):
            pedSum=0
            sigSum=0
            Signal=0
            Pedestal=0
            for BX in xrange(0, 40):

                adcValue=data[event][link][BX][linkChannel]
                if BX < 15 : pedSum += adcValue
                if BX > 19 and  BX < 25: sigSum += adcValue
                xSingleEv[BX]=BX
                ySingleEv[BX]=adcValue
        
            scanvas = MakeCanvas("mm","nn",800,800)
            GrSingleEv=TGraph(len(xSingleEv),xSingleEv,ySingleEv)
            OutFile.WriteObject(GrSingleEv,"singleEv_"+str(iAmp)+"_"+str(event))
            SFit=TF1("fit", "gaus", 19,23)
            SFit.SetParameter(0, 4000)
            SFit.SetParameter(1, 20.9)
            SFit.SetParLimits(1, 20, 22)
            SFit.SetParameter(2, 1.5)
            GrSingleEv.Draw("AC*")
            GrSingleEv.Fit("fit","R0")
            SFit.Draw("same")
            FitParam=SFit.GetParameters()
            print "Gaus fit param 1, 2, 3= " , round(FitParam[0],4), round(FitParam[1],4), round(FitParam[2],4)
            scanvas.SaveAs("PLOT/singleEv_"+str(iAmp)+"_"+str(event)+".pdf")
            
            Pedestal=pedSum/15.
            y[event]= sigSum- Pedestal*5
            M.Fill(y[event])

        histMean= M.GetMean()
        histRMS= M.GetStdDev()

        highVal = histMean + 4 * histRMS
        lowVal = histMean - 4 * histRMS
        highValAx = histMean + 6 * histRMS
        lowValAx = histMean - 6 * histRMS

        canvas = MakeCanvas("asdf","asdf",800,800)
        canvas.Update()
        MyGr= TGraph(len(x), x,y)
        mfit=TF1("fit", "gaus", lowVal,highVal)
        M.Fit(mfit, "R0","")
        FitParam=mfit.GetParameters()
#        FitParErr=mfit.GetParError()
        integral= round(FitParam[1],4)
        integral_RMS= round(FitParam[2],4)
        integralErr= round(mfit.GetParError(1),4)
        integral_RMSErr= round(mfit.GetParError(2),4)
        print "iAmp=", iAmp, "   integral= ", integral,  "   integral_RMS=", integral_RMS


        M.SetMarkerStyle(22)
        M.GetXaxis().SetRangeUser(lowValAx,highValAx)
        
        M.SetTitle(Title+" = "+str(iAmp))
        M.Draw("pe")
        mfit.Draw("same")
        fitInfo  =TPaveText(.20,0.7,.60,0.9, "NDC");
        fitInfo.SetBorderSize(   0 );
        fitInfo.SetFillStyle(    0 );
        fitInfo.SetTextAlign(   12 );
        fitInfo.SetTextSize ( 0.03 );
        fitInfo.SetTextColor(    1 );
        fitInfo.SetTextFont (   62 );
        fitInfo.AddText("Mean of Fit=" + str(round(FitParam[1],1)))
        fitInfo.AddText("RMS of Fit =" + str(round(FitParam[2],1)))
        fitInfo.Draw()
        canvas.SaveAs("HistoSingleRun_"+str(iAmp)+"_"+Title+RootName+".pdf")



        xIntegral[num]=iAmp
        yIntegral[num]=integral
        yIntegralErrUp[num]=integral+integralErr
        yIntegralErrDown[num]=integral-integralErr

        xIntegral_RMS[num]=iAmp
        yIntegral_RMS[num]=integral_RMS
        yIntegral_RMSErrUp[num]=integral_RMS+integral_RMSErr
        yIntegral_RMSErrDown[num]=integral_RMS-integral_RMSErr
        
        xRatio[num]=iAmp
        yRatio[num]=integral_RMS/integral

#        xIntegral.append(iAmp)
#        yIntegral.append(integral)
#        xIntegral_RMS.append(iAmp)
#        yIntegral_RMS.append(integral_RMS)

    Graph_Integral= TGraph(len(xIntegral), xIntegral,yIntegral)
    Graph_IntegralErUp= TGraph(len(xIntegral), xIntegral,yIntegralErrUp)
    Graph_IntegralErDown= TGraph(len(xIntegral), xIntegral,yIntegralErrDown)
    
    canvas_Integral = MakeCanvas("can1","can1",800,800)
#    canvas_Integral.SetLogy()
    Graph_Integral.SetTitle("Pulse Integral Stability")
    Graph_Integral.SetMarkerStyle(22)
    Graph_Integral.SetMarkerColor(3)
    Graph_Integral.SetMarkerSize(2)
    Graph_Integral.GetXaxis().SetTitle("Day")
    Graph_Integral.GetYaxis().SetRangeUser(80000,85000)
    Graph_Integral.Draw()
#    Graph_IntegralErUp.Draw("same")
#    Graph_IntegralErDown.Draw("same")
    canvas_Integral.SaveAs("Integral_"+Title+RootName+".pdf")

    Graph_Integral_RMS= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMS)
    Graph_Integral_RMSErUp= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMSErrUp)
    Graph_Integral_RMSErDown= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMSErrDown)

    canvas_Integral_RMS = MakeCanvas("can2","can2",800,800)
    Graph_Integral_RMS.SetTitle("Pulse Integral RMS vs. Pulse  "+Title)
    Graph_Integral_RMS.SetMarkerStyle(23)
    Graph_Integral_RMS.SetMarkerColor(2)
    Graph_Integral_RMS.SetMarkerSize(2)
    Graph_Integral.GetXaxis().SetTitle("Day")
    Graph_Integral_RMS.Draw()
#    Graph_Integral_RMSErUp.Draw("same")
#    Graph_Integral_RMSErDown.Draw("same")
    canvas_Integral_RMS.SaveAs("Integral_RMS_"+Title+RootName+".pdf")


    Graph_Ratio= TGraph(len(xRatio), xRatio,yRatio)
    canvas_Ratio = MakeCanvas("can2","can2",800,800)
    Graph_Ratio.SetTitle("Ratio of Pulse Integral RMS and Pulse Integral  "+Title)
    Graph_Ratio.SetMarkerStyle(21)
    Graph_Ratio.SetMarkerColor(8)
    Graph_Ratio.SetMarkerSize(2)
    Graph_Integral.GetXaxis().SetTitle("Day")
    Graph_Ratio.Draw()
    canvas_Ratio.SaveAs("Ratio_"+Title+RootName+".pdf")

#    OutFile=TFile(RootName,"RECREATE")
    OutFile.WriteObject(Graph_Integral,"Graph_Integral")
    OutFile.WriteObject(Graph_Integral_RMS,"Graph_Integral_RMS")
    OutFile.WriteObject(Graph_Ratio,"Graph_Ratio")
    OutFile.Close()





Title="Height"

AllRuns=["DayTest/DayTest_Wednesday_Feb03_Shunt0_TDC8_WID10_AMP8.txt","DayTest/DayTest_Thursday_Feb04_Shunt0_TDC8_WID10_AMP8.txt","DayTest/DayTest_Friday_Feb05_Shunt0_TDC8_WID10_AMP8.txt"]
RootName="integralStab.root"
Measure_Integral(AllRuns, Title,RootName)






















    
    
