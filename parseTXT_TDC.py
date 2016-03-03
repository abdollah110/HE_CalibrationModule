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

    LINK=[19]
#    LINK=[15,16,17,18,19]
#    LINKkChannel=[0,1,2,3,4,5]
    LINKkChannel=[2]
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
                    tdcValue=0
                    for BX in xrange(0, 40):

                        if (iAmp <= 10 and BX==20 and tdc[event][link][BX][linkChannel] !=31.5) : tdcValue=tdc[event][link][BX][linkChannel]
                        if (iAmp > 10  and BX==21 and tdc[event][link][BX][linkChannel] !=31.5) : tdcValue=tdc[event][link][BX][linkChannel]

                    y[event]= tdcValue
                    M.Fill(y[event])

                histMean= M.GetMean()
                histRMS= M.GetStdDev()

                highVal = histMean + 4 * histRMS
                lowVal = histMean - 4 * histRMS
                highValAx = histMean + 6 * histRMS
                lowValAx = histMean - 6 * histRMS

                canvas = MakeCanvas("can","can",800,800)
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
                canvas.SaveAs("outHistoSingleRun_"+RootName+str(iAmp)+"_link"+str(link)+"_ch_"+str(linkChannel)+".pdf")



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

            Graph_TDC= TGraph(len(xIntegral), xIntegral,yIntegral)
            Graph_TDCErUp= TGraph(len(xIntegral), xIntegral,yIntegralErrUp)
            Graph_TDCErDown= TGraph(len(xIntegral), xIntegral,yIntegralErrDown)
            
            canvas_TDC = MakeCanvas("can1","can1",800,800)
            Graph_TDC.SetTitle("TDC vs. Pulse  "+Title)
            Graph_TDC.SetMarkerStyle(22)
            Graph_TDC.SetMarkerColor(3)
            Graph_TDC.SetMarkerSize(2)
            Graph_TDC.GetXaxis().SetTitle(XaxisT)
            Graph_TDC.GetYaxis().SetRangeUser(0, 30)
            Graph_TDC.Draw()
            Graph_TDCErUp.Draw("same")
            Graph_TDCErDown.Draw("same")
            canvas_TDC.SaveAs("outHisto_"+RootName+"_link"+str(link)+"_ch_"+str(linkChannel)+".pdf")

            Graph_TDC_RMS= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMS)
            Graph_TDC_RMSErUp= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMSErrUp)
            Graph_TDC_RMSErDown= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMSErrDown)

            canvas_TDC_RMS = MakeCanvas("can2","can2",800,800)
            Graph_TDC_RMS.SetTitle("TDC RMS vs. Pulse  "+Title)
            Graph_TDC_RMS.SetMarkerStyle(23)
            Graph_TDC_RMS.SetMarkerColor(2)
            Graph_TDC_RMS.SetMarkerSize(2)
            Graph_TDC_RMS.GetXaxis().SetTitle(XaxisT)
            Graph_TDC_RMS.GetYaxis().SetRangeUser(0,2)
            Graph_TDC_RMS.Draw()
            Graph_TDC_RMSErUp.Draw("same")
            Graph_TDC_RMSErDown.Draw("same")
            canvas_TDC_RMS.SaveAs("outHistoRMS_"+RootName+"_link"+str(link)+"_ch_"+str(linkChannel)+".pdf")


            OutFile=TFile("outFile_"+RootName+"_link"+str(link)+"_ch_"+str(linkChannel)+".root","RECREATE")
            OutFile.WriteObject(Graph_TDC,"Graph_TDC")
            OutFile.WriteObject(Graph_TDC_RMS,"Graph_TDC_RMS")
            OutFile.Close()




##########################################################################################
# This part is used for the computation of the Time vs Amplitude for different TDC Values
##########################################################################################
Do_TDC=0
if Do_TDC:
    
    #Fname1="FullDec8/Dec8_TDC8_AMP/TU_tdc8_amp"
    Fname1="_MON_Feb29_TDCvsAPM_Shunt_TDCTHR/MON_Feb29_WID10_Delay3_Sunt1_TDCThre8_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=11
    freq=1
    RootName="WID10_Delay3_Sunt1_TDCThre8_AMP"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)

    #Fname1="FullDec8/Dec8_TDC128_AMP/TU_tdc128_amp"
    Fname1="_MON_Feb29_TDCvsAPM_Shunt_TDCTHR/MON_Feb29_WID10_Delay3_Sunt1_TDCThre128_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=11
    freq=1
    RootName="WID10_Delay3_Sunt1_TDCThre128_AMP"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)

    #Fname1="FullDec8/Dec8_TDC248_AMP/TU_tdc248_amp"
    Fname1="_MON_Feb29_TDCvsAPM_Shunt_TDCTHR/MON_Feb29_WID10_Delay3_Sunt1_TDCThre200_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=11
    freq=1
    RootName="WID10_Delay3_Sunt1_TDCThre200_AMP"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)


##########################################################################################
# This part is used for the computation of the Time vs Amplitude for different Shunt Values
##########################################################################################
Do_Shunt=1
if Do_Shunt:
    Fname1="_MON_Feb29_TDCvsAPM_Shunt_TDCTHR/MON_Feb29_WID10_Delay3_TDCThre8_Sunt1_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=10
    freq=1
    RootName="WID10_Delay3_TDCThre8_Sunt1_AMP"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)



    Fname1="_MON_Feb29_TDCvsAPM_Shunt_TDCTHR/MON_Feb29_WID10_Delay3_TDCThre8_Sunt1Over6_AMP"
    Fname2=".txt"

    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=10
    freq=1
    RootName="WID10_Delay3_TDCThre8_Sunt1Over6_AMP"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)


    #Fname1="FullDec8/Dec8_Shunt30_AMP/TU_Shunt30_amp"
    Fname1="_MON_Feb29_TDCvsAPM_Shunt_TDCTHR/MON_Feb29_WID10_Delay3_TDCThre8_Sunt1Over11_AMP"
    Fname2=".txt"
    Title="Height"
    XaxisT="height * 0.1"
    low=4
    high=10
    freq=1
    RootName="WID10_Delay3_TDCThre8_Sunt1Over11_AMP"
    Measure_Integral(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)


    ##########################################################################################
    # This part is used for the computation of the Time vs Amplitude for different for different delay setting
    ##########################################################################################
Do_Delay=0
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











    
