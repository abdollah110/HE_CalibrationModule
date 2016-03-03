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





def Make_TDC_Energy(Fname1,Fname2,Title, XaxisT,low,high,freq,RootName):
    
    f_fc=TFile(Fname1)
    f_tdc=TFile(Fname2)
    gr_Inregral_fc=f_fc.Get("Graph_Integral")
    gr_Inregral_tdc=f_tdc.Get("Graph_Integral")

    FNumber=int((high-low)/freq)
    
    xpoint=array("d",xrange(0,FNumber))
    ypoint=array("d",xrange(0,FNumber))




        
        
    num=-1
    for iAmp in range(low,high,freq):
        num+=1
        xpoint[num]=gr_Inregral_fc.Eval(iAmp)/3800;print xpoint[num]
        ypoint[num]= gr_Inregral_tdc.Eval(iAmp); print ypoint[num]

    TwoDGraph=TGraph(len(xpoint), xpoint,ypoint)
    canvas_Integral = MakeCanvas("can1","can1",800,800)
    TwoDGraph.SetTitle("Time [ns] vs. Energy [GeV]  ")
    TwoDGraph.SetMarkerStyle(22)
    TwoDGraph.SetMarkerColor(3)
    TwoDGraph.SetMarkerSize(2)
    TwoDGraph.GetXaxis().SetTitle("Energy [GeV]")
    TwoDGraph.GetYaxis().SetTitle("Time [ns]")
    TwoDGraph.GetYaxis().SetRangeUser(TMath.MinElement(len(xpoint),TwoDGraph.GetY())/1.3, TMath.MaxElement(len(xpoint),TwoDGraph.GetY()) * 1.2)
    TwoDGraph.Draw()
    canvas_Integral.SaveAs("Final_Time_Energy.pdf")



        
        
#        
#        Fname=Fname1+str(iAmp)+Fname2
#
#        f = open(Fname)
#        data = getData(f)
#
#        M=TH1F(Fname,Fname,2000,0,1000000)
#        x = array("d", xrange(0,1001))
#        y = array("d", xrange(0,1001))
#
#
#        for event in xrange(0,995):
#            pedSum=0
#            sigSum=0
#            Signal=0
#            Pedestal=0
#            for BX in xrange(0, 40):
##                print "[event][link][BX][linkChannel] = ", event,"  "  ,link,"  "  , BX ,"  "  ,linkChannel, "---->data[event][link][BX][linkChannel]", data[event][link][BX][linkChannel]
#    #            print BX
#    #            print event
#    #            print "data=", data[event][link][BX][linkChannel]
#    #            print "TDC=", tdc[event][link][BX][linkChannel]
#    #            print "\n"
#
#                adcValue=data[event][link][BX][linkChannel]
#                if BX < 15 : pedSum += adcValue
#                if BX > 19 and  BX < 25: sigSum += adcValue
##                if BX > 18 and BX < 26: print "[event][link][BX][linkChannel] = ", event,"  "  ,link,"  "  , BX ,"  "  ,linkChannel, "---->data[event][link][BX][linkChannel]", data[event][link][BX][linkChannel]
#
#            Pedestal=pedSum/15.
#            y[event]= sigSum- Pedestal*5
#            M.Fill(y[event])
#
#        histMean= M.GetMean()
#        histRMS= M.GetStdDev()
#
#        highVal = histMean + 4 * histRMS
#        lowVal = histMean - 4 * histRMS
#        highValAx = histMean + 6 * histRMS
#        lowValAx = histMean - 6 * histRMS
#
#        canvas = MakeCanvas("asdf","asdf",800,800)
#        canvas.Update()
#        MyGr= TGraph(len(x), x,y)
#        mfit=TF1("fit", "gaus", lowVal,highVal)
#        M.Fit(mfit, "R0","")
#        FitParam=mfit.GetParameters()
##        FitParErr=mfit.GetParError()
#        integral= round(FitParam[1],4)
#        integral_RMS= round(FitParam[2],4)
#        integralErr= round(mfit.GetParError(1),4)
#        integral_RMSErr= round(mfit.GetParError(2),4)
#        print "iAmp=", iAmp, "   integral= ", integral,  "   integral_RMS=", integral_RMS
#
#
#        M.SetMarkerStyle(22)
#        M.GetXaxis().SetRangeUser(lowValAx,highValAx)
#        
#        M.SetTitle(Title+" = "+str(iAmp))
#        M.Draw("pe")
#        mfit.Draw("same")
#        fitInfo  =TPaveText(.20,0.7,.60,0.9, "NDC");
#        fitInfo.SetBorderSize(   0 );
#        fitInfo.SetFillStyle(    0 );
#        fitInfo.SetTextAlign(   12 );
#        fitInfo.SetTextSize ( 0.03 );
#        fitInfo.SetTextColor(    1 );
#        fitInfo.SetTextFont (   62 );
#        fitInfo.AddText("Mean of Fit=" + str(round(FitParam[1],1)))
#        fitInfo.AddText("RMS of Fit =" + str(round(FitParam[2],1)))
#        fitInfo.Draw()
#        canvas.SaveAs("HistoSingleRun_"+str(iAmp)+"_"+Title+".pdf")
#
#
#
#        xIntegral[num]=iAmp
#        yIntegral[num]=integral
#        yIntegralErrUp[num]=integral+integralErr
#        yIntegralErrDown[num]=integral-integralErr
#
#        xIntegral_RMS[num]=iAmp
#        yIntegral_RMS[num]=integral_RMS
#        yIntegral_RMSErrUp[num]=integral_RMS+integral_RMSErr
#        yIntegral_RMSErrDown[num]=integral_RMS-integral_RMSErr
#        
#        xRatio[num]=iAmp
#        yRatio[num]=integral_RMS/integral
#
##        xIntegral.append(iAmp)
##        yIntegral.append(integral)
##        xIntegral_RMS.append(iAmp)
##        yIntegral_RMS.append(integral_RMS)
#
#    Graph_Integral= TGraph(len(xIntegral), xIntegral,yIntegral)
#    Graph_IntegralErUp= TGraph(len(xIntegral), xIntegral,yIntegralErrUp)
#    Graph_IntegralErDown= TGraph(len(xIntegral), xIntegral,yIntegralErrDown)
#    
#    canvas_Integral = MakeCanvas("can1","can1",800,800)
##    canvas_Integral.SetLogy()
#    Graph_Integral.SetTitle("Pulse Integral vs. Pulse  "+Title)
#    Graph_Integral.SetMarkerStyle(22)
#    Graph_Integral.SetMarkerColor(3)
#    Graph_Integral.SetMarkerSize(2)
#    Graph_Integral.GetXaxis().SetTitle(XaxisT)
#    Graph_Integral.Draw()
#    Graph_IntegralErUp.Draw("same")
#    Graph_IntegralErDown.Draw("same")
#    canvas_Integral.SaveAs("Integral_"+Title+".pdf")
#
#    Graph_Integral_RMS= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMS)
#    Graph_Integral_RMSErUp= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMSErrUp)
#    Graph_Integral_RMSErDown= TGraph(len(xIntegral_RMS), xIntegral_RMS,yIntegral_RMSErrDown)
#
#    canvas_Integral_RMS = MakeCanvas("can2","can2",800,800)
#    Graph_Integral_RMS.SetTitle("Pulse Integral RMS vs. Pulse  "+Title)
#    Graph_Integral_RMS.SetMarkerStyle(23)
#    Graph_Integral_RMS.SetMarkerColor(2)
#    Graph_Integral_RMS.SetMarkerSize(2)
#    Graph_Integral_RMS.GetXaxis().SetTitle(XaxisT)
#    Graph_Integral_RMS.Draw()
#    Graph_Integral_RMSErUp.Draw("same")
#    Graph_Integral_RMSErDown.Draw("same")
#    canvas_Integral_RMS.SaveAs("Integral_RMS_"+Title+".pdf")


#    Graph_Ratio= TGraph(len(xRatio), xRatio,yRatio)
#    canvas_Ratio = MakeCanvas("can2","can2",800,800)
#    Graph_Ratio.SetTitle("Ratio of Pulse Integral RMS and Pulse Integral  "+Title)
#    Graph_Ratio.SetMarkerStyle(21)
#    Graph_Ratio.SetMarkerColor(8)
#    Graph_Ratio.SetMarkerSize(2)
#    Graph_Ratio.GetXaxis().SetTitle(XaxisT)
#    Graph_Ratio.Draw()
#    canvas_Ratio.SaveAs("Ratio_"+Title+".pdf")
#
#    OutFile=TFile(RootName,"RECREATE")
#    OutFile.WriteObject(Graph_Integral,"Graph_Integral")
#    OutFile.WriteObject(Graph_Integral_RMS,"Graph_Integral_RMS")
#    OutFile.WriteObject(Graph_Ratio,"Graph_Ratio")
#    OutFile.Close()



Fname1="FC_TDC/fc_vs_amplitude.root"
Fname2="FC_TDC/tdc_vs_amplitude.root"
Title="Height"
XaxisT="height * 0.1"
low=2
high=11
freq=1
RootName="tdc_energy_amplitude.root"
Make_TDC_Energy(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)

    
Fname1="FC_TDC/tdc_vs_amplitude.root"
Fname2=".txt"
Title="Width"
XaxisT="Width"
low=4
high=26
freq=2
RootName="fc_vs_width.root"
#Make_TDC_Energy(Fname1,Fname2, Title, XaxisT,low,high,freq,RootName)






















    
    
