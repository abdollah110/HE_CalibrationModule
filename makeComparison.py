import numpy
import ROOT
from ROOT import TCanvas
from ROOT import TFile
from ROOT import TH1F
from ROOT import TF1
from ROOT import TGraph
from ROOT import TLegend
from ROOT import TPaveText
from array import array
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas
from ROOT import TMath



def SupreImpose3Objects(File, Graph,rangelow,rangehigh,Xaxis,Yaxis,Title,leg0,leg1,leg2,RoootName):
    
    
    
#    gr_Int={}

    gr0=File[0].Get(Graph)
    gr1=File[1].Get(Graph)
    gr2=File[2].Get(Graph)
    
    print gr1.GetName()

#    num=0
#    for itdc in File:
#        gr_Int[num]=itdc.Get(Graph)
#        num+=1

    canvas_tdc=MakeCanvas("TDC","TDC",800,800)
    gr0.SetTitle("")
    gr0.GetYaxis().SetRangeUser(rangelow,rangehigh)
    gr0.GetYaxis().SetLabelSize(0.035)
    gr0.GetYaxis().SetTitleOffset(2)
    gr0.GetYaxis().SetTitle(Yaxis)
    gr0.SetLineColor(1)
    gr0.SetLineWidth(3)
    gr0.SetMarkerColor(1)
    gr0.SetMarkerSize(1.5)
    gr0.SetMarkerStyle(23)
    gr0.Draw()
    
    gr1.SetLineColor(2)
    gr1.SetLineWidth(2)
    gr1.SetMarkerColor(2)
    gr1.SetMarkerSize(1.5)
    gr1.SetMarkerStyle(23)
#    gr1.Draw("sameLP")

    gr2.SetLineColor(4)
    gr2.SetMarkerSize(1.5)
    gr2.SetMarkerColor(4)
    gr2.SetMarkerStyle(23)
    gr2.SetLineWidth(2)
    gr2.Draw("sameLP")


    leg=TLegend(0.6, 0.7, 0.9, 0.9)

    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(.03)

    leg.AddEntry(gr0,leg0,"l")
#    leg.AddEntry(gr1,leg1,"l")
    leg.AddEntry(gr2,leg2,"l")
    leg.Draw()


    canvas_tdc.SaveAs(RoootName)








FileNames={}



######################################################################################################################################
# This is used to make the   Time VS   Height for different values of TDC (8,128,200)  
#The input files come from the cide parseTXT_TDC.py
######################################################################################################################################

Do_TDC=0
if Do_TDC:
    #tdc8 = TFile("Shunt_TDCThreshold/outRoot_TDC8.root")
    #tdc128 = TFile("Shunt_TDCThreshold/outRoot_TDC128.root")
    #tdc248 = TFile("Shunt_TDCThreshold/outRoot_TDC248.root")
    tdc8 = TFile("ROOT_Compare/outFile_WID10_Delay3_Sunt1_TDCThre8_AMP_link15_ch_5.root")
    tdc128 = TFile("ROOT_Compare/outFile_WID10_Delay3_Sunt1_TDCThre128_AMP_link15_ch_5.root")
    tdc248 = TFile("ROOT_Compare/outFile_WID10_Delay3_Sunt1_TDCThre200_AMP_link15_ch_5.root")

    FileNames["TDC"]=[tdc8,tdc128,tdc248]

    Title="Time v.s. Pulse Amplitude Setting"
    Xaxis="Aplitude * 0.1"
    Yaxis="Time [ns]"
    leg0="TDC Threshold = 8"
    leg1="TDC Threshold = 128"
    leg2="TDC Threshold = 200"
    SupreImpose3Objects(FileNames["TDC"],"Graph_TDC",0,40,Xaxis,Yaxis,Title,leg0,leg1,leg2,"TDC_Amplitude_TDCTHreshold.pdf")
    Yaxis="RMS Time [ns]"
    Title="Time RMS v.s. Pulse Amplitude Setting"
    SupreImpose3Objects(FileNames["TDC"],"Graph_TDC_RMS",0,2,Xaxis,Yaxis,Title,leg0,leg1,leg2,"TDC_RMS_Amplitude_TDCTHreshold.pdf")
#    Yaxis="RMS / Time"
#    Title="Ratio Time RMS and Time v.s. Pulse Amplitude Setting"
#    SupreImpose3Objects(FileNames["TDC"],"Graph_Ratio",0,.1,Xaxis,Yaxis,Title,leg0,leg1,leg2,"TDC_Ratio_Amplitude_TDCTHreshold.pdf")

######################################################################################################################################
# This is used to make the   Time VS   Height for different values of Shunt (0,16,30)  --> equivalent to (1, 1/6 and 1/11)
#The input files come from the cide parseTXT_TDC.py
######################################################################################################################################

Do_Shunt=0
if Do_Shunt:
    shunt0 = TFile("ROOT_Compare/outFile_WID10_Delay3_TDCThre8_Sunt1_AMP_link19_ch_2.root")
    shunt16 = TFile("ROOT_Compare/outFile_WID10_Delay3_TDCThre8_Sunt1Over6_AMP_link19_ch_2.root")
    shunt30 = TFile("ROOT_Compare/outFile_WID10_Delay3_TDCThre8_Sunt1Over11_AMP_link19_ch_2.root")
    FileNames["Shunt"]=[shunt0,shunt16,shunt30]



    Title="Time v.s. Pulse Amplitude Setting"
    Xaxis="Aplitude * 0.1"
    Yaxis="Time [ns]"
    leg0="Shunt = 1"
    leg1="Shunt = 1/6"
    leg2="Shunt = 1/11"
    SupreImpose3Objects(FileNames["Shunt"],"Graph_TDC",0,40,Xaxis,Yaxis,Title,leg0,leg1,leg2,"TDC_Amplitude_Shunt.pdf")
    Yaxis="RMS Time [ns]"
    Title="Time RMS v.s. Pulse Amplitude Setting"
    SupreImpose3Objects(FileNames["Shunt"],"Graph_TDC_RMS",0,2,Xaxis,Yaxis,Title,leg0,leg1,leg2,"TDC_RMS_Amplitude_Shunt.pdf")
#    Yaxis="RMS / Time"
#    Title="Ratio Time RMS and Time v.s. Pulse Amplitude Setting"
#    SupreImpose3Objects(FileNames["Shunt"],"Graph_Ratio",0,.08,Xaxis,Yaxis,Title,leg0,leg1,leg2,"TDC_Ratio_Amplitude_Shunt.pdf")


#####################################################################################################
#####################################################################################################
#####################################################################################################
Do_SuperImpose_PulseIntegral_AMP=0
if Do_SuperImpose_PulseIntegral_AMP:
    tdc8 = TFile("ROOT_Compare/fc_vs_width_AMP5.root")
    tdc128 = TFile("ROOT_Compare/fc_vs_width_AMP5.root")
    tdc248 = TFile("ROOT_Compare/fc_vs_width_AMP9.root")
    FileNames["TDC"]=[tdc8,tdc128,tdc248]

    Title="Charge v.s. Pulse Width Setting"
    Xaxis="Width [ns]"
    Yaxis="Charge [fc]"
    leg0="Amplitude = 0.5"
    leg1="Amplitude = 0.5"
    leg2="Amplitude = 0.9"
    SupreImpose3Objects(FileNames["TDC"],"Graph_Integral",14,350000,Xaxis,Yaxis,Title,leg0,leg1,leg2,"fc_WIDTH_Integral.pdf")
    Yaxis="Charge RMS [fc]"
    Title="Charge RMS v.s. Pulse Width Setting"
    SupreImpose3Objects(FileNames["TDC"],"Graph_Integral_RMS",0,16000,Xaxis,Yaxis,Title,leg0,leg1,leg2,"fc_WIDTH_Integral_RMS.pdf")
    Yaxis="RMS/Charge"
    Title="Ratio CHarge RMS and Charge v.s. Pulse Width Setting"
    SupreImpose3Objects(FileNames["TDC"],"Graph_Ratio",0,.5,Xaxis,Yaxis,Title,leg0,leg1,leg2,"fc_WIDTH_Ratio.pdf")

#####################################################################################################
Do_SuperImpose_PulseIntegral_WID=0
if Do_SuperImpose_PulseIntegral_WID:

    tdc8 = TFile("ROOT_Compare/fc_vs_amplitude_WID4.root")
    tdc128 = TFile("ROOT_Compare/fc_vs_amplitude_WID10.root")
    tdc248 = TFile("ROOT_Compare/fc_vs_amplitude_WID22.root")
    FileNames["TDC"]=[tdc8,tdc128,tdc248]

    Title="Charge v.s. Pulse Amplitude Setting"
    Xaxis="Width [ns]"
    Yaxis="Charge [fc]"
    leg0="Width = 4 ns"
    leg1="Width = 10 ns"
    leg2="Width = 22 ns"
    SupreImpose3Objects(FileNames["TDC"],"Graph_Integral",14,400000,Xaxis,Yaxis,Title,leg0,leg1,leg2,"fc_AMP_Integral.pdf")
    Yaxis="Charge RMS [fc]"
    Title="Charge RMS v.s. Pulse Amplitude Setting"
    SupreImpose3Objects(FileNames["TDC"],"Graph_Integral_RMS",0,12000,Xaxis,Yaxis,Title,leg0,leg1,leg2,"fc_AMP_Integral_RMS.pdf")
    Yaxis="RMS/Charge"
    Title="Ratio CHarge RMS and Charge v.s. Pulse Amplitude Setting"
    SupreImpose3Objects(FileNames["TDC"],"Graph_Ratio",0,.5,Xaxis,Yaxis,Title,leg0,leg1,leg2,"fc_AMP_Ratio.pdf")

####################################################################################################
#   Comapring the pulse Width v.s. width
#####################################################################################################
Do_SuperImpose_PulseIntegral_WIDTH=1
if Do_SuperImpose_PulseIntegral_WIDTH:
    tdc8 = TFile("ROOT_Compare/outFile__PulseWidth_Delay3_AMP5_WID_link19_ch_2.root")
    tdc128 = TFile("ROOT_Compare/outFile__PulseWidth_Delay3_AMP5_WID_link19_ch_2.root")
    tdc248 = TFile("ROOT_Compare/outFile__PulseWidth_Delay3_AMP9_WID_link19_ch_2.root")
    
    
    FileNames["TDC"]=[tdc8,tdc128,tdc248]
    
    Title="Pulse Width v.s. Pulse Width Setting"
    Xaxis="Width [ns]"
    Yaxis="Pulse Width [(BX) x 25 ns]"
    leg0="Amplitude = 0.5"
    leg1="Amplitude = 0.5"
    leg2="Amplitude = 0.9"
    SupreImpose3Objects(FileNames["TDC"],"Graph_PulseWidth",0,1,Xaxis,Yaxis,Title,leg0,leg1,leg2,"PulseWidth_Delay3_AMP_WID_link19_ch_2.pdf")
    Yaxis="Pulse Width [(BX) x 25 ns]"
    Title="Charge RMS v.s. Pulse Width Setting"
    SupreImpose3Objects(FileNames["TDC"],"Graph_PulseWidth_RMS",0,.2,Xaxis,Yaxis,Title,leg0,leg1,leg2,"PulseWidth_RMS_Delay3_AMP_WID_link19_ch_2.pdf")
    Yaxis="RMS Width / Width"
    Title="Ratio CHarge RMS and Charge v.s. Pulse Width Setting"
    SupreImpose3Objects(FileNames["TDC"],"Graph_Ratio",0,.2,Xaxis,Yaxis,Title,leg0,leg1,leg2,"PulseWidth_Ratio_Delay3_AMP_WID_link19_ch_2.pdf")

####################################################################################################
#   Comapring the pulse Width  v.s. Integral
#####################################################################################################
Do_SuperImpose_PulseIntegral_AMP=0
if Do_SuperImpose_PulseIntegral_AMP:
    tdc8 = TFile("ROOT_Compare/outFile__PulseWidth_Delay3_WID4_AMP_link19_ch_2.root")
    tdc128 = TFile("ROOT_Compare/outFile__PulseWidth_Delay3_WID10_AMP_link19_ch_2.root")
    tdc248 = TFile("ROOT_Compare/outFile__PulseWidth_Delay3_WID22_AMP_link19_ch_2.root")
    
    
    FileNames["TDC"]=[tdc8,tdc128,tdc248]
    
    Title="Pulse Width v.s. Pulse Width Setting"
    Xaxis="Width [ns]"
    Yaxis="Pulse Width [(BX) x 25 ns]"
    leg0="Width = 4 ns"
    leg1="Width = 10 ns"
    leg2="Width = 22 ns"
    SupreImpose3Objects(FileNames["TDC"],"Graph_PulseWidth",0,1,Xaxis,Yaxis,Title,leg0,leg1,leg2,"PulseWidth_Delay3_WID_AMP_link19_ch_2.pdf")
    Yaxis="Pulse Width RMS [(BX) x 25 ns]"
    Title="Charge RMS v.s. Pulse Width Setting"
    SupreImpose3Objects(FileNames["TDC"],"Graph_PulseWidth_RMS",0,.2,Xaxis,Yaxis,Title,leg0,leg1,leg2,"PulseWidth_RMS_Delay3_WID_AMP_link19_ch_2.pdf")
    Yaxis="RMS Width / Width"
    Title="Ratio CHarge RMS and Charge v.s. Pulse Width Setting"
    SupreImpose3Objects(FileNames["TDC"],"Graph_Ratio",0,.2,Xaxis,Yaxis,Title,leg0,leg1,leg2,"PulseWidth_Ratio_Delay3_WID_AMP_link19_ch_2.pdf")






    
    
