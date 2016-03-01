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
from ROOT import TMath




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
#link = 19 #3, 15,16,17,18,19, or 20
#linkChannel = 5 # 0 - 5
#BX = 0







def Measure_Integral(Fname1,Fname2,Title, XaxisT,low,high,freq,RootName):

    FNumber=int((high-low)/freq)
    print "*************  -> initiating      The ", Fname1 , " and number of files exist= ", FNumber



#    xIntegral=[]
#    yIntegral=[]
#    xIntegral_RMS=[]
#    yIntegral_RMS=[]

    LINK=[15]
#    LINK=[15,16,17,18,19]
#    LINKkChannel=[0,1,2,3,4,5]
    LINKkChannel=[4]
    for linkChannel in LINKkChannel:
        for link in LINK:
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
            num=-1
            for iAmp in range(low,high,freq):
                num+=1
                Fname=Fname1+str(iAmp)+Fname2
                print "*************  -> initiating      The ", Fname , " and number of files exist= ", FNumber
                print "-------------------->  Now is doing ....  ", low, "  ____ ", Fname
                
                

                

                f = open(Fname)
        #        data = getData(f)
                tdc = getTDCValues(f)

                M=TH1F(Fname,Fname,200,0,100)
                x = array("d", xrange(0,1001))
                y = array("d", xrange(0,1001))


                for event in xrange(0,995):
                    pedSum=0
                    sigSum=0
                    Signal=0
                    Pedestal=0
                    for BX in xrange(0, 40):
        #                print "[event][link][BX][linkChannel] = ", event,"  "  ,link,"  "  , BX ,"  "  ,linkChannel, "---->data[event][link][BX][linkChannel]", tdc[event][link][BX][linkChannel]
            #            print BX
            #            print event
            #            print "data=", data[event][link][BX][linkChannel]
        #                print "TDC=", tdc[event][link][BX][linkChannel]
            #            print "\n"
        #                print "@@@@@@@@------->     [event] ", event
                        tdcValue=tdc[event][link][BX][linkChannel]
        #                print "@@@@@@@@------->     [event] ", event
                        if (iAmp <= 10 and BX==20 and tdc[event][link][BX][linkChannel] !=31.5) : sigSum += tdcValue ;
                        if (iAmp > 10 and BX==21 and tdc[event][link][BX][linkChannel] !=31.5) : sigSum += tdcValue ;
        #                    print "[event][link][BX][linkChannel] = ", event,"  "  ,link,"  "  , BX ,"  "  ,linkChannel, "---->data[event][link][BX][linkChannel]", tdc[event][link][BX][linkChannel]
        #                if BX > 19 and  BX < 25: sigSum += adcValue
        #                if BX > 18 and BX < 26: print "[event][link][BX][linkChannel] = ", event,"  "  ,link,"  "  , BX ,"  "  ,linkChannel, "---->data[event][link][BX][linkChannel]", data[event][link][BX][linkChannel]


                    print "---------------------> sigSum= ",sigSum
                    y[event]= sigSum
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

                integral= histMean
                if FitParam[1] < 1.5 * histMean: integral= round(FitParam[1],4)

                integral_RMS= histRMS
                if round(FitParam[2],4) < 2 * histRMS : integral_RMS= round(FitParam[2],4)
                    
                integralErr= round(mfit.GetParError(1),4)
                integral_RMSErr= round(mfit.GetParError(2),4)
                print "iAmp=", iAmp, "   integral= ", integral,  "   integral_RMS=", integral_RMS


                M.SetMarkerStyle(22)
                M.GetXaxis().SetRangeUser(0,30)
        #        M.GetXaxis().SetRangeUser(lowValAx,highValAx)

                M.SetTitle("TDC v.s. Delay Setting (ns)")
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
                fitInfo.AddText("Delay Setting =" + str(iAmp))
                fitInfo.AddText("link  =" + str(link) +"  channel="+str(linkChannel))
                fitInfo.Draw()
                canvas.SaveAs("HistoSingleRun_"+str(iAmp)+"_"+Title+"_TDC"+str(link)+"_ch_"+str(linkChannel)+".pdf")



                XVAL=low+num*freq
                xIntegral[num]=XVAL
                yIntegral[num]=integral
                yIntegralErrUp[num]=integral+integralErr
                yIntegralErrDown[num]=integral-integralErr

                xIntegral_RMS[num]=XVAL
                yIntegral_RMS[num]=integral_RMS
                yIntegral_RMSErrUp[num]=integral_RMS+integral_RMSErr
                yIntegral_RMSErrDown[num]=integral_RMS-integral_RMSErr
                
                
                print "iAmp, integral=  "  , iAmp, "  " ,integral, "  XVAL= ", XVAL
#                xRatio[num]=XVAL
#                yRatio[num]=integral_RMS/integral

        #        xIntegral.append(iAmp)
        #        yIntegral.append(integral)
        #        xIntegral_RMS.append(iAmp)
        #        yIntegral_RMS.append(integral_RMS)

            Graph_Integral= TGraph(len(xIntegral), xIntegral,yIntegral)
            Graph_IntegralErUp= TGraph(len(xIntegral), xIntegral,yIntegralErrUp)
            Graph_IntegralErDown= TGraph(len(xIntegral), xIntegral,yIntegralErrDown)
            
            canvas_Integral = MakeCanvas("can1","can1",800,800)
        #    canvas_Integral.SetLogy()
            Graph_Integral.SetTitle("TDC vs. Pulse  "+Title)
            Graph_Integral.SetMarkerStyle(22)
            Graph_Integral.SetMarkerColor(3)
            Graph_Integral.SetMarkerSize(2)
            Graph_Integral.GetXaxis().SetTitle(XaxisT)
            Graph_Integral.GetYaxis().SetRangeUser(0, 30)
            print "%%%%%%%% Graph_Integral.GetMaximum()= ", TMath.MaxElement(len(xIntegral_RMS),Graph_Integral.GetY())
        #    Graph_Integral.SetMaximum(1.5)
            Graph_Integral.Draw()
            Graph_IntegralErUp.Draw("same")
            Graph_IntegralErDown.Draw("same")
            canvas_Integral.SaveAs("Integral_"+Title+"_TDC"+str(link)+"_ch_"+str(linkChannel)+".pdf")

#            Graph_Integral_RMS= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMS)
#            Graph_Integral_RMSErUp= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMSErrUp)
#            Graph_Integral_RMSErDown= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMSErrDown)

#            canvas_Integral_RMS = MakeCanvas("can2","can2",800,800)
#            Graph_Integral_RMS.SetTitle("TDC RMS vs. Pulse  "+Title)
#            Graph_Integral_RMS.SetMarkerStyle(23)
#            Graph_Integral_RMS.SetMarkerColor(2)
#            Graph_Integral_RMS.SetMarkerSize(2)
#            Graph_Integral_RMS.GetXaxis().SetTitle(XaxisT)
#            Graph_Integral_RMS.GetYaxis().SetRangeUser(0,2)
#            Graph_Integral_RMS.Draw()
#            Graph_Integral_RMSErUp.Draw("same")
#            Graph_Integral_RMSErDown.Draw("same")
#            canvas_Integral_RMS.SaveAs("Integral_RMS_"+Title+"_TDC"+str(link)+"_ch_"+str(linkChannel)+".pdf")
#
#
#            Graph_Ratio= TGraph(len(xRatio), xRatio,yRatio)
#            canvas_Ratio = MakeCanvas("can2","can2",800,800)
#            Graph_Ratio.SetTitle("Ratio of TDC RMS and TDC  "+Title)
#            Graph_Ratio.SetMarkerStyle(21)
#            Graph_Ratio.SetMarkerColor(4)
#            Graph_Ratio.SetMarkerSize(2)
#            Graph_Ratio.GetXaxis().SetTitle(XaxisT)
#            Graph_Ratio.GetYaxis().SetRangeUser(TMath.MinElement(len(xIntegral_RMS),Graph_Ratio.GetY())/2, TMath.MaxElement(len(xIntegral_RMS),Graph_Ratio.GetY()) * 1.5)
#            Graph_Ratio.Draw()
#            canvas_Ratio.SaveAs("Ratio_"+Title+"_TDC"+str(link)+"_ch_"+str(linkChannel)+".pdf")
#
            OutFile=TFile(RootName,"RECREATE")
            OutFile.WriteObject(Graph_Integral,"Graph_Integral")
#            OutFile.WriteObject(Graph_Integral_RMS,"Graph_Integral_RMS")
#            OutFile.WriteObject(Graph_Ratio,"Graph_Ratio")
            OutFile.Close()



#OutFile.WriteObject(M,"MMM")
#OutFile.WriteObject(MyGr,"gr")



#Fname1="TuesdayDec1st_AMP/TU_0p"
#Fname2="_10.txt"
#Title="Height"
#XaxisT="height * 0.1"
#low=2
#high=11
#freq=1
#RootName="tdc_vs_amplitude.root"
#Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)

    
#Fname1="TuesdayDec1st_WID/TU_WID_0p5_"
#Fname2=".txt"
#Title="Width"
#XaxisT="Width"
#low=4
#high=26
#freq=2
#RootName="tdc_vs_width.root"
#Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)


##########################################################################################
# This part is used for the computation of the Time vs Amplitude for different TDC Values
##########################################################################################
Do_TDC=0
if Do_TDC:
    
    #Fname1="FullDec8/Dec8_TDC8_AMP/TU_tdc8_amp"
    Fname1="Friday18Dec_TDCtest/FR_Dec18_WID10_Shunt0_TDC8_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=10
    freq=2
    RootName="outRoot_TDC8.root"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)

    #Fname1="FullDec8/Dec8_TDC128_AMP/TU_tdc128_amp"
    Fname1="Friday18Dec_TDCtest/FR_Dec18_WID10_Shunt0_TDC128_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=10
    freq=2
    RootName="outRoot_TDC128.root"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)

    #Fname1="FullDec8/Dec8_TDC248_AMP/TU_tdc248_amp"
    Fname1="Friday18Dec_TDCtest/FR_Dec18_WID10_Shunt0_TDC200_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=10
    freq=2
    RootName="outRoot_TDC200.root"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)


##########################################################################################
# This part is used for the computation of the Time vs Amplitude for different Shunt Values
##########################################################################################
Do_Shunt=0
if Do_Shunt:
    Fname1="Friday18Dec_TDCtest/FR_Dec18_WID10_Shunt0_TDC8_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=10
    freq=1
    RootName="outRoot_Shunt0.root"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)



    Fname1="Friday18Dec_TDCtest/FR_Dec18_WID10_Shunt16_TDC8_AMP"
    Fname2=".txt"

    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=10
    freq=1
    RootName="outRoot_Shunt16.root"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)


    #Fname1="FullDec8/Dec8_Shunt30_AMP/TU_Shunt30_amp"
    Fname1="Friday18Dec_TDCtest/FR_Dec18_WID10_Shunt30_TDC8_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=10
    freq=1
    RootName="outRoot_Shunt30.root"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)


    ##########################################################################################
    # This part is used for the computation of the Time vs Amplitude for different for different delay setting
    ##########################################################################################
Do_Delay=1
if Do_Delay:
    Fname1="_FRI_Feb26_TDC_vs_Delay/FRI_Feb26_TDCThre8_Sunt1_AMP8_WID10_Delay"
    Fname2=".txt"
    Title="TDC"
    XaxisT="delay [ns]"
    low=3
    high=23
    freq=2
    RootName="outRoot_TDCvsDelay.root"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)

##########################################################################################
#      NEW    DATA     FEB   2016   This part is used for the computation of the Time vs Amplitude for different delay setting
##########################################################################################
Do_Delay=0
if Do_Delay:
    Fname1="MondayFeb08/Mon_Feb08_Shun0_TDC128_AMP8_WID10_delay"
    Fname2=".txt"
    Title="TDC"
    XaxisT="delay [ns]"
    low=1
    high=23
    freq=2
    RootName="outRoot_TDCvsDelay.root"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)











    
