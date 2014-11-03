import math, os, string
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine('.L Loader.C+') 

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetFillStyle(ROOT.kWhite)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetFrameBorderMode(ROOT.kWhite)
ROOT.gStyle.SetFrameFillColor(ROOT.kWhite)
ROOT.gStyle.SetCanvasBorderMode(ROOT.kWhite)
ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
ROOT.gStyle.SetPadBorderMode(ROOT.kWhite)
ROOT.gStyle.SetPadColor(ROOT.kWhite)
ROOT.gStyle.SetStatColor(ROOT.kWhite)
ROOT.gStyle.SetErrorX(0)

canvas = ROOT.TCanvas('canvas','',100,100,600,600)
canvas.SetGridx()
canvas.SetGridy()

pse_r = 0.75 # threshold for looking at preshower width
weight_names = ['raw','E','phi','EPhi']

file_out = ROOT.TFile("histograms.root","RECREATE")

def style_histogram(h):
    h.GetXaxis().SetLabelSize(0.025)
    h.GetXaxis().SetTitleOffset(1.25)
    h.GetYaxis().SetLabelSize(0.025)
    h.GetYaxis().SetTitleOffset(1.25)

    color = ROOT.kBlack
    marker = 20
    
    h.SetMarkerStyle(marker)
    h.SetMarkerColor(color)
    h.SetLineColor(color)

sample_names = ['ZprimeToEE_M1000_v5','QCD_v5']
signal_samples = ['ZprimeToEE_M1000_v5']

eta_cut = 1.43
m_window_cut = 10
pi = 3.14159

if not os.path.exists('plots'):
    os.makedirs('plots')
for sname in sample_names:
    if not os.path.exists('plots/%s'%sname):
        os.makedirs('plots/%s'%sname)

# Make legend, labels
def make_legend(x1, y1, x2, y2):
    legend = ROOT.TLegend(x1,y1,x2,y2)
    legend.SetShadowColor(ROOT.kWhite)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetBorderSize(0)
    return legend

region_labels = {}
for regions in ['BB','BF','FF']:
    label = ROOT.TLatex(0.6, 0.75, regions)
    label.SetNDC()
    region_labels[regions] = label

topology_labels = {}
for regions in ['neutral','cis','trans']:
    label = ROOT.TLatex(0.6, 0.7, regions)
    label.SetNDC()
    topology_labels[regions] = label

CMS_label_texts = {}
CMS_label_texts['normal'        ] = 'CMS'
CMS_label_texts['internal'      ] = 'CMS internal'
CMS_label_texts['workInProgress'] = 'CMS work in progress'
CMS_labels = {}
for t in CMS_label_texts:
    CMS_labels[t] = ROOT.TLatex(0.65, 0.945, CMS_label_texts[t])
    CMS_labels[t].SetNDC()
CMS_label = CMS_labels['internal']

sample_labels = {}
x = 0.6
sample_labels['data'            ] = ROOT.TLatex(x, 0.82, '2012 Run D'               )
sample_labels['Zee'             ] = ROOT.TLatex(x, 0.82, 'Z/#gamma*#rightarrow ee'  )
sample_labels['singlePhoton'    ] = ROOT.TLatex(x, 0.82, 'SinglePhoton'             )
sample_labels['ZprimeToEE_M1000'] = ROOT.TLatex(x, 0.82, 'Z\'#rightarrowee (M=1TeV)')
sample_labels['DYEE'            ] = ROOT.TLatex(x, 0.82, 'Z/#gamma*#rightarrowee'   )
sample_labels['WW'              ] = ROOT.TLatex(x, 0.82, 'W^{+}W^{-}'               )
sample_labels['QCD_170_300'     ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[100-370]'       )
sample_labels['QCD_300_470'     ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[300-470]'       )
sample_labels['QCD_470_600'     ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[470-600]'       )
sample_labels['QCD_600_800'     ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[600-800]'       )
sample_labels['QCD_800_100'     ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[800-1000]'      )
sample_labels['QCD_1000_1400'   ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[1000-1400]'     )
sample_labels['QCD_1400_1800'   ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[1400-1800]'     )
sample_labels['QCD_1800'        ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[1800+]'         )
sample_labels['QCD'             ] = ROOT.TLatex(x, 0.82, 'QCD'                      )

for sl in sample_labels:
    sample_labels[sl].SetNDC()

OSSS_labels = {}
for OSSS in ['OS','SS']:
    label = ROOT.TLatex(0.6, 0.65, OSSS)
    label.SetNDC()
    OSSS_labels[OSSS] = label

trigger_label = ROOT.TLatex(0.05,0.95,'HLT_Ele33_Ele33_v7')
trigger_label.SetNDC()

def draw_labels(regions, topology, sname, draw_legend, OSSS):
    if draw_legend:
        legend.Draw()
    else:
        OSSS_labels[OSSS].Draw()
    CMS_label.Draw()
    region_labels[regions].Draw()
    if regions=='FF':
        topology_labels[topology].Draw()
    #if sname!='singlePhoton':
    #    trigger_label.Draw()
    sample_labels[sname].Draw()


class electron_object:
    def __init__(self, p4_in, charge, preshowerEnergy, hovere, sixix, siyiy, sirir, eshitsixix, eshitsiyiy, crystals, e1x5, e2x5, fBrem, index):
        self.charge = charge
        self.p4 = p4_in
        self.PSE = preshowerEnergy
        self.index = index
        self.region = 'B'
        self.hovere = hovere
        self.sixix = sixix
        self.siyiy = siyiy
        self.sirir = sirir
        self.eshitsixix = eshitsixix
        self.eshitsiyiy = eshitsiyiy
        self.crystals = crystals
        self.e1x5 = e1x5
        self.e2x5 = e2x5
        self.fBrem = fBrem
        
        self.sixix_calc = eseffsiwiw(self.eshitsixix)
        self.siyiy_calc = eseffsiwiw(self.eshitsiyiy)
        
        self.rxy = 0
        self.Ex  = 0
        self.Ey  = 0
        sumx = sum(self.eshitsixix)
        sumy = sum(self.eshitsiyiy)
        if sumy > 0:
            self.rxy = sumx/sumy
        if sumx+sumy > 0:
            self.Ex = sumx*self.PSE/(sumx+sumy)
            self.Ey = sumy*self.PSE/(sumx+sumy)
        
        # Find the hottest eshitsixix and eshitsiyiy hits
        self.ordered_eshitsixix = ordered_hits(self.eshitsixix)
        self.ordered_eshitsiyiy = ordered_hits(self.eshitsiyiy)
        
        self.ps_ix0 = 0
        self.ps_iy0 = 0
        maxX = 0
        maxY = 0
        for i in range(0,len(self.ordered_eshitsixix)):
            if self.ordered_eshitsixix[i] > maxX:
                maxX = self.ordered_eshitsixix[i]
                self.ps_ix0 = i
            if self.ordered_eshitsiyiy[i] > maxY:
                maxY = self.ordered_eshitsiyiy[i]
                self.ps_iy0 = i
        # Arrange the hits in (arbitrary) positive and negative sides around the central value
        self.sumeshitsixix = sum(self.ordered_eshitsixix)
        self.sumeshitsiyiy = sum(self.ordered_eshitsiyiy)
        self.sumeshit      = self.sumeshitsixix + self.sumeshitsiyiy
        self.eshitsixix_0  = self.ordered_eshitsixix[self.ps_ix0]
        self.eshitsiyiy_0  = self.ordered_eshitsiyiy[self.ps_iy0]
        self.eshit_0       = self.eshitsixix_0 + self.eshitsiyiy_0
        self.eshitsixix_p  = self.ordered_eshitsixix[self.ps_ix0+1:]
        self.eshitsixix_m  = self.ordered_eshitsixix[:self.ps_ix0-1]
        self.eshitsiyiy_p  = self.ordered_eshitsiyiy[self.ps_iy0+1:]
        self.eshitsiyiy_m  = self.ordered_eshitsiyiy[:self.ps_iy0-1]
        
        # Find how many steps we need to take to include at least 50% of the preshower energy
        # Sum over x and y simultaneously first then separately second
        # First seek from the highest energy hit
        pse_sum = self.eshit_0
        ixp = 0
        ixm = 0
        iyp = 0
        iym = 0
        while pse_sum < pse_r*self.sumeshit:
            if ixp < len(self.eshitsixix_p):
                pse_sum += self.eshitsixix_p[ixp]
                ixp += 1
            if ixm < len(self.eshitsixix_m):
                pse_sum += self.eshitsixix_m[ixm]
                ixm += 1
            if iyp < len(self.eshitsiyiy_p):
                pse_sum += self.eshitsiyiy_p[iyp]
                iyp += 1
            if iym < len(self.eshitsiyiy_m):
                pse_sum += self.eshitsiyiy_m[iym]
                iym += 1
            if ixp==len(self.eshitsixix_p) and ixm==len(self.eshitsixix_m) and iyp==len(self.eshitsiyiy_p) and iym==len(self.eshitsiyiy_m):
                break
        self.ps_ir = max([ixp,ixm,iyp,iym])
        
        pse_sum = self.eshitsixix_0
        ixp = 0
        ixm = 0
        while pse_sum < pse_r*self.sumeshitsixix:
            if ixp < len(self.eshitsixix_p):
                pse_sum += self.eshitsixix_p[ixp]
                ixp += 1
            if ixm < len(self.eshitsixix_m):
                pse_sum += self.eshitsixix_m[ixm]
                ixm += 1
            if ixp==len(self.eshitsixix_p) and ixm==len(self.eshitsixix_m):
                break
        self.ps_ix = max([ixp,ixm])
        
        pse_sum = self.eshitsiyiy_0
        iyp = 0
        iym = 0
        while pse_sum < pse_r*self.sumeshitsiyiy:
            if iyp < len(self.eshitsiyiy_p):
                pse_sum += self.eshitsiyiy_p[iyp]
                iyp += 1
            if iym < len(self.eshitsiyiy_m):
                pse_sum += self.eshitsiyiy_m[iym]
                iym += 1
            if iyp==len(self.eshitsiyiy_p) and iym==len(self.eshitsiyiy_m):
                break
        self.ps_iy = max([iyp,iym])
        
        if abs(self.p4.Eta())>eta_cut:
            self.region = 'F'
        
        self.r9  = 0
        self.r25 = 0
        for i1 in range(0,len(self.crystals)):
            for i2 in range(0,len(self.crystals[i1])):
                self.r25 += self.crystals[i1][i2]
                if i1!=0 and i1!=4 and i2!=0 and i2!=4:
                    self.r9 += self.crystals[i1][i2]
        if self.r25 > 0:
            self.r9  = self.r9 /self.r25
            self.r25 = self.r25/self.r25

# Create variables and histograms
class var_object:
    def __init__(self, name, nBins, lower, upper, xaxis, yaxis, units):
        file_out.cd()
        self.name  = name
        self.nBins = nBins
        self.lower = lower
        self.upper = upper
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.units = units
        self.hBase = ROOT.TH1F('hBase_%s'%self.name, '', self.nBins, self.lower, self.upper)
        self.hBase.Sumw2()
        perUnit = (self.upper-self.lower)/self.nBins
        unit = '' if self.units=='' else '[%s]'%self.units
        self.hBase.GetXaxis().SetTitle('%s %s'%(self.xaxis,unit))
        self.hBase.GetYaxis().SetTitle('%s per %.2f %s'%(self.yaxis, perUnit, self.units))
        
        file_out.cd()
        self.h = {}
        for sname in sample_names:
            for wname in weight_names:
                hName = 'h_%s_%s_%s'%(self.name, sname, wname)
                h = self.hBase.Clone(hName)
                style_histogram(h)
                self.h['%s_%s'%(sname,wname)] = h
    def fill_histogram(self,value,weights,sname):
        for wname in weight_names:
            self.h['%s_%s'%(sname,wname)].Fill(value,weights[wname])
    
class var2_object:
    def __init__(self, name, nBinsX, lowerX, upperX, nBinsY, lowerY, upperY, xaxis, yaxis, unitsX, unitsY):
        self.name  = name
        self.nBinsX = nBinsX
        self.lowerX = lowerX
        self.upperX = upperX
        self.nBinsY = nBinsY
        self.lowerY = lowerY
        self.upperY = upperY
        self.xaxis =  xaxis
        self.yaxis  = yaxis
        self.unitsX = unitsX
        self.unitsY = unitsY
        self.hBase = ROOT.TH2F('hBase_%s'%self.name, '', self.nBinsX, self.lowerX, self.upperX, self.nBinsY, self.lowerY, self.upperY)
        unitX = '' if self.unitsX=='' else ' [%s]'%self.unitsX
        unitY = '' if self.unitsY=='' else ' [%s]'%self.unitsY
        self.hBase.GetXaxis().SetTitle('%s%s'%(self.xaxis,self.unitsX))
        self.hBase.GetYaxis().SetTitle('%s%s'%(self.yaxis,self.unitsY))
        
        file_out.cd()
        self.h = {}
        for sname in sample_names:
            for wname in weight_names:
                hName = 'h_%s_%s_%s'%(self.name, sname, wname)
                h = self.hBase.Clone(hName)
                style_histogram(h)
                self.h['%s_%s'%(sname,wname)] = h
    def fill_histogram(self,x,y,weights,sname):
        for wname in weight_names:
            self.h['%s_%s'%(sname,wname)].Fill(x,y,weights[wname])
        
vars = {}
#100 -> 50
vars['eta'         ] = var_object('eta'         , 100,   -3,   3, '#eta(e)'             , 'electrons', '')
vars['phi'         ] = var_object('phi'         , 100, -180, 180, '#phi(e)'             , 'electrons', '')
vars['phi_cut'     ] = var_object('phi_cut'     , 100, -180, 180, '#phi(e) (PSE>5 GeV)' , 'electrons', '')
vars['phi_cut_etap'] = var_object('phi_cut_etap', 100, -180, 180, '#phi(e) (PSE>5 GeV , #eta>0)' , 'electrons', '')
vars['phi_cut_etam'] = var_object('phi_cut_etam', 100, -180, 180, '#phi(e) (PSE>5 GeV , #eta<0)' , 'electrons', '')
vars['E'           ] = var_object('E'           , 100, 0, 4000, 'E(e)'                  , 'electrons', 'GeV')# not 21000
vars['E_w'         ] = var_object('E_w'         , 100, 0, 4000, 'E(e) <weighted>'       , 'electrons', 'GeV')
vars['E_cut'       ] = var_object('E_cut'       , 100, 0, 4000, 'E(e) (PSE>5 GeV)'      , 'electrons', 'GeV')
vars['ET'          ] = var_object('ET'          , 100, 0, 1000, 'E_{T}(e)'              , 'electrons', 'GeV')
vars['PSE'         ] = var_object('PSE'         , 100, 0,  100, 'E_{PS}(e)'             , 'electrons', 'GeV')
vars['PSE_meeCut'  ] = var_object('PSE_meeCut'  , 100, 0,  100, 'E_{PS}(e)'             , 'electrons', 'GeV')
vars['mee'         ] = var_object('mee'         , 100, 0, 2000, 'm(ee)'                 , 'Z bosons' , 'GeV')
vars['mee_wide'    ] = var_object('mee_wide'    , 100, 0, 4000, 'm(ee)'                 , 'Z bosons' , 'GeV')
vars['rxy'         ] = var_object('rxy'         , 100, 0,    1, '#sumE_{x}/#sumE_{y}(e)', 'electrons',    '')
vars['r9'          ] = var_object('r9'          , 100, 0,    1, 'r_{9}(e)'              , 'electrons',    '')
vars['fBrem'       ] = var_object('fBrem'       , 100, 0,    1, 'f_{Brem}(e)'           , 'electrons',    '')
vars['Ex'          ] = var_object('Ex'          , 100, 0,  100, '#SigmaE_{x}(e)'        , 'electrons', 'GeV')
vars['Ey'          ] = var_object('Ey'          , 100, 0,  100, '#SigmaE_{y}(e)'        , 'electrons', 'GeV')
vars['e1x5'        ] = var_object('e1x5'        , 100, 0, 3000, 'e_{1x5}(e)'            , 'electrons', 'GeV')
vars['e2x5'        ] = var_object('e2x5'        , 100, 0, 3000, 'e_{2x5}(e)'            , 'electrons', 'GeV')
vars['PSEOverEt'   ] = var_object('PSEOverEt'   , 100, 0,  0.6, 'E_{PS}(e)/E_{T}(e)'    , 'electrons',    '')
vars['PSEOverE'    ] = var_object('PSEOverE'    , 100, 0,  0.2, 'E_{PS}(e)/E(e)'        , 'electrons',    '')
vars['PSEOverEz'   ] = var_object('PSEOverEz'   , 100, 0,  0.2, 'E_{PS}(e)/E_{z}(e)'    , 'electrons',    '')
vars['sixix'       ] = var_object('sixix'       , 100, 0,   10, '#sigma_{eff}^{xx}(e)'  , 'electrons',    '')
vars['siyiy'       ] = var_object('siyiy'       , 100, 0,   10, '#sigma_{eff}^{yy}(e)'  , 'electrons',    '')
vars['sirir'       ] = var_object('sirir'       , 100, 0,   12, '#sigma_{eff}^{rr}(e)'  , 'electrons',    '')
vars['sixixOSiyiy' ] = var_object('sixixOSiyiy' , 100, 0,  2.5, '#sigma_{eff}^{xx}(e)/#sigma_{eff}^{yy}(e)', 'electrons', '')
vars['sixixOSirir' ] = var_object('sixixOSirir' , 100, 0,  1.5, '#sigma_{eff}^{xx}(e)/#sigma_{eff}^{rr}(e)', 'electrons', '')
vars['siyiyOSirir' ] = var_object('siyiyOSirir' , 100, 0,  1.5, '#sigma_{eff}^{yy}(e)/#sigma_{eff}^{rr}(e)', 'electrons', '')
vars['sixixMSiyiy' ] = var_object('sixixMSiyiy' , 100, 0,   100, '#sigma_{eff}^{xx}(e)#times#sigma_{eff}^{yy}(e)', 'electrons', '')
vars['DR_mc'       ] = var_object('DR_mc'       , 100, 0,    5, '#DeltaR_{MC}(e)'       , 'electrons', '')

# How far do need to extend the shower to get 50% of the PS energy?
vars['ps_ix0'      ] = var_object('ps_ix0', 22, -0.5, 21.5, 'ix_{0}(e)'  , 'electrons', '')
vars['ps_iy0'      ] = var_object('ps_iy0', 22, -0.5, 21.5, 'iy_{0}(e)'  , 'electrons', '')
vars['ps_ix'       ] = var_object('ps_ix' , 22, -0.5, 21.5, 'ix^{50}(e)' , 'electrons', '')
vars['ps_iy'       ] = var_object('ps_iy' , 22, -0.5, 21.5, 'iy^{50}(e)' , 'electrons', '')
vars['ps_ir'       ] = var_object('ps_ir' , 22, -0.5, 21.5, 'ir^{50}(e)' , 'electrons', '')
vars['ps_ixy'      ] = var_object('ps_ixy', 22, -0.5, 21.5, 'ixy^{50}(e)', 'electrons', '')

# Weights
#100
vars['w'           ] = var_object('w'     , 100,  0.0,  1.0, 'weight (e)', 'electrons', '')

vars2 = {}
vars2['PSEVsEta'    ] = var2_object('PSEVsEta'  , 100, 1.4,  3.0, 100, 0, 100.0, '|#eta| (e)', 'E_{PS}(e)' , 'GeV', '')
vars2['PSEVsHoe'    ] = var2_object('PSEVsHoe'  , 100, 0.0, 0.05, 100, 0, 100.0, 'H(e)/E(e)' , 'E_{PS}(e)' , 'GeV', '')
vars2['sixixSiyiy'  ] = var2_object('sixixSiyiy', 100, 0.0,   10, 100, 0,    10, '#sigma_{eff}^{xx}(e)' , '#sigma_{eff}^{yy}(e)' , '', '')
vars2['rxyVsPhi'    ] = var2_object('rxyVsPhi'  ,  50,-180,  180,  50, 0,     2, '#phi(e)' , '#sumE_{x}/#sumE_{y}(e)' , '', '')
vars2['sixixVsPhi'  ] = var2_object('sixixVsPhi',  50,-180,  180,  50, 0,    10, '#phi(e)' , '#sigma_{eff}^{xx}(e)'   , '', '')
vars2['siyiyVsPhi'  ] = var2_object('siyiyVsPhi',  50,-180,  180,  50, 0,    10, '#phi(e)' , '#sigma_{eff}^{yy}(e)'   , '', '')
vars2['ExVsPhi'     ] = var2_object('ExVsPhi'   ,  50,-180,  180,  50, 0,   100, '#phi(e)' , '#sigma_E{x}(e)'         , '', '')
vars2['EyVsPhi'     ] = var2_object('EyVsPhi'   ,  50,-180,  180,  50, 0,   100, '#phi(e)' , '#sigma_E{y}(e)'         , '', '')

vars2['sixixVsPhiEp'] = var2_object('sixixVsPhiEp',  50,-180,  180,  50, 0,    10, '#phi(e^{+})' , '#sigma_{eff}^{xx}(e^{+})' , '', '')
vars2['siyiyVsPhiEp'] = var2_object('siyiyVsPhiEp',  50,-180,  180,  50, 0,    10, '#phi(e^{-})' , '#sigma_{eff}^{yy}(e^{-})' , '', '')
vars2['sixixVsPhiEm'] = var2_object('sixixVsPhiEm',  50,-180,  180,  50, 0,    10, '#phi(e^{+})' , '#sigma_{eff}^{xx}(e^{+})' , '', '')
vars2['siyiyVsPhiEm'] = var2_object('siyiyVsPhiEm',  50,-180,  180,  50, 0,    10, '#phi(e^{-})' , '#sigma_{eff}^{yy}(e^{-})' , '', '')

vars2['ExVsPhiEp'   ] = var2_object('ExVsPhiEp'   ,  50,-180,  180,  50, 0,   100, '#phi(e^{+})' , '#SigmaE_{x}(e^{+})' , '', '')
vars2['EyVsPhiEp'   ] = var2_object('EyVsPhiEp'   ,  50,-180,  180,  50, 0,   100, '#phi(e^{-})' , '#SigmaE_{y}(e^{-})' , '', '')
vars2['ExVsPhiEm'   ] = var2_object('ExVsPhiEm'   ,  50,-180,  180,  50, 0,   100, '#phi(e^{+})' , '#SigmaE_{x}(e^{+})' , '', '')
vars2['EyVsPhiEm'   ] = var2_object('EyVsPhiEm'   ,  50,-180,  180,  50, 0,   100, '#phi(e^{-})' , '#SigmaE_{y}(e^{-})' , '', '')

vars2['EVsPhi'      ] = var2_object('EVsPhi'      ,  50,-180,  180,  50, 0,  2500, '#phi(e)' , 'E (e)'         , 'GeV', '')
vars2['EVsPhi_cut'  ] = var2_object('EVsPhi_cut'  ,  50,-180,  180,  50, 0,  2500, '#phi(e)' , 'E (e)'         , 'GeV', '')

def ordered_hits(hits):
    if hits==0:
        return -1
    nBIN = 21
    esRH = [0]*nBIN
    for ibin in range(0,(nBIN+1)/2):
        if ibin==0:
            esRH[(nBIN-1)/2] = hits[ibin]
        else:
            esRH[(nBIN-1)/2+ibin] = hits[ibin]
            esRH[(nBIN-1)/2-ibin] = hits[ibin+15]
    return esRH

def eseffsiwiw(hits):
    if hits==0:
        return -1
    nBIN = 21
    esRH = [0]*nBIN
    for ibin in range(0,(nBIN+1)/2):
        if ibin==0:
            esRH[(nBIN-1)/2] = hits[ibin]
        else:
            esRH[(nBIN-1)/2+ibin] = hits[ibin]
            esRH[(nBIN-1)/2-ibin] = hits[ibin+15]
   
    EffWidthSigmaISIS = 0.0
    totalEnergyISIS   = 0.0
    EffStatsISIS      = 0.0
    for id_X in range(0,21):
        totalEnergyISIS  += esRH[id_X]
        EffStatsISIS     += esRH[id_X]*(id_X-10)*(id_X-10)
    EffWidthSigmaISIS = 0 if totalEnergyISIS<1e-6 else math.sqrt(abs(EffStatsISIS/totalEnergyISIS))
    return EffWidthSigmaISIS

events = {}
for sname in sample_names:
    print sname
    file = ROOT.TFile('ntuples/outfile_%s_skimmed_slimmed.root'%sname,'READ')
    tree = file.Get('IIHEAnalysis')
    if not tree:
        continue
    tree.SetBranchStatus('*'     ,0)
    tree.SetBranchStatus('mc_*'  ,1)
    tree.SetBranchStatus('gsf_*' ,1)
    tree.SetBranchStatus('HEEP_*',1)
    
    events[sname] = []
    nEntries = tree.GetEntries()
    #nEntries = 1000
    nSuccess = 0
    for i in range(0,nEntries):
        success = False
        #if nSuccess > 50:
        #    break
        electrons = []
        tree.GetEntry(i)
        if i%10000==0:
            print i , '/' , nEntries , ' (' , nSuccess , ')'
        for j in range(0,tree.gsf_n):
            if not tree.HEEP_cutflow50_25ns_total[j]:
                continue
            sixix = 0
            siyiy = 0
            sirir = 0
            eshitsixix = 0
            eshitsiyiy = 0
            PSE = 0
            
            sixix = tree.HEEP_eseffsixix[j]
            siyiy = tree.HEEP_eseffsiyiy[j]
            sirir = tree.HEEP_eseffsirir[j]
            PSE = tree.HEEP_preshowerEnergy[j]
            eshitsixix = tree.HEEP_eshitsixix[j]
            eshitsiyiy = tree.HEEP_eshitsiyiy[j]
            e1x5 = tree.gsf_e1x5[j]
            e2x5 = tree.gsf_e2x5Max[j]
            fBrem = tree.gsf_fBrem[j]
            
            crystals = tree.HEEP_crystal_energy
            
            p4 = ROOT.TLorentzVector()
            eta = tree.gsf_eta[j]
            phi = tree.gsf_phi[j]
            p4.SetPtEtaPhiE(tree.gsf_pt[j], eta, phi, tree.gsf_energy[j])
            el = electron_object(p4, tree.gsf_charge[j], PSE, tree.gsf_hadronicOverEm[j], sixix, siyiy, sirir, eshitsixix, eshitsiyiy, crystals, e1x5, e2x5, fBrem, j)
            
            best_DR = 1e6
            best_Eratio = -1
            for k in range(0,len(tree.mc_index)):
                if abs(tree.mc_pdgId[k])!=11:
                    continue
                mcp4 = ROOT.TLorentzVector()
                mcp4.SetPtEtaPhiE(tree.mc_pt[k], tree.mc_eta[k], tree.mc_phi[k], tree.mc_energy[k])
                DR = p4.DeltaR(mcp4)
                if DR < best_DR:
                    best_DR = DR
                    best_Eratio = p4.E()/mcp4.E()
            el.DR = best_DR
            

            #if el.DR > 0.5:#
            #    continue

            # Cut on energy ratio
            if sname in signal_samples and best_Eratio < 0.9:
                continue
            
            electrons.append(el)
                
            success = True
        if success:
            nSuccess = nSuccess + 1
            events[sname].append(electrons)
    
    print len(events[sname]) , ' events with electrons'
    counter = 0

for sname in sample_names:
    for ev in events[sname]:
        for el in ev:
            phi = 180*el.p4.Phi()/3.1459
            E  = el.p4.E()
            
            w = {}
            w['phi'] = 0
            w['E'  ] = 0
            w['raw'] = 1
            w['EPhi'] = w['E']*w['phi']
            vars['E'  ].fill_histogram(E  , w, sname)
            vars['phi'].fill_histogram(phi, w, sname)
            
            vars2['EVsPhi'].fill_histogram(phi,E,w,sname)
            
            if el.PSE >= 5:
                vars['E_cut'  ].fill_histogram(E  , w, sname)
                vars['phi_cut'].fill_histogram(phi, w, sname)
                vars2['EVsPhi_cut'].fill_histogram(phi,E,w,sname)
    
    for ev in events[sname]:
        for el in ev:
            phi = 180*el.p4.Phi()/3.1459
            E   = el.p4.E()
            counter = counter + 1
            
            hname = '%s_%s'%(sname,'raw')
            xaxis_phi = vars['phi'  ].h[hname].GetXaxis()
            xaxis_E   = vars['E_cut'].h[hname].GetXaxis()
            bin_phi   = xaxis_phi.FindBin(phi)
            bin_E     = xaxis_E.FindBin(E)
            
            w = {}
            w['phi'] = 0
            w['E'  ] = 0
            
            phi_bin_numer = vars['phi'    ].h[hname].GetBinContent(bin_phi)
            phi_bin_denom = vars['phi_cut'].h[hname].GetBinContent(bin_phi)
            if phi_bin_denom > 0:
                w['phi'] = phi_bin_numer/phi_bin_denom
            
            E_bin_denom = vars['E_cut'].h[hname].GetBinContent(bin_E)
            if E_bin_denom  >0:
                w['E'] = 1.0/E_bin_denom
            
            w['raw' ] = 1
            w['EPhi'] = 0
            
            bin_phi_x = vars2['EVsPhi_cut'].h[hname].GetXaxis().FindBin(phi)
            bin_E_y   = vars2['EVsPhi_cut'].h[hname].GetYaxis().FindBin(E  )
            value = vars2['EVsPhi_cut'].h[hname].GetBinContent(bin_phi_x,bin_E_y)
            if value > 0:
                w['EPhi']  = 1.0/value
            
            w_w = {}
            w_w['phi' ] = 1
            w_w['E'   ] = 1
            w_w['raw' ] = 1
            w_w['EPhi'] = 1
            
            vars['w'].fill_histogram(w['EPhi'] , w_w, sname)
            
            if el.p4.Eta()>0:
                vars['phi_cut_etap'].fill_histogram(phi , w_w, sname)
            if el.p4.Eta()<0:
                vars['phi_cut_etam'].fill_histogram(phi , w_w, sname)
            
            if el.PSE < 5:
                continue
            
            vars['eta'].fill_histogram(el.p4.Eta(), w, sname)
            vars['E_w'].fill_histogram(el.p4.E()  , w, sname)
            vars['ET' ].fill_histogram(el.p4.Pt() , w, sname)
            vars['PSE'].fill_histogram(el.PSE     , w, sname)
            vars2['PSEVsEta'].fill_histogram(el.p4.Eta(), el.PSE, w, sname)
            vars2['PSEVsHoe'].fill_histogram(el.hovere  , el.PSE, w, sname)
            vars['PSEOverEt'].fill_histogram(el.PSE/el.p4.Pt(), w, sname)
            vars['PSEOverE' ].fill_histogram(el.PSE/el.p4.E() , w, sname)
            vars['PSEOverEz'].fill_histogram(el.PSE/el.p4.Z() , w, sname)
            if el.sixix>1e-3:
                vars['sixix'      ].fill_histogram(el.sixix         , w, sname)
                vars['sixixOSirir'].fill_histogram(el.sixix/el.sirir, w, sname)
                vars2['sixixVsPhi'].fill_histogram(phi,el.sixix, w, sname)
                vars2['ExVsPhi'   ].fill_histogram(phi,el.Ex   , w, sname)
                if el.charge>0:
                    vars2['sixixVsPhiEp'].fill_histogram(phi,el.sixix, w, sname)
                    vars2['ExVsPhiEp'   ].fill_histogram(phi,el.Ex   , w, sname)
                else:
                    vars2['sixixVsPhiEm'].fill_histogram(phi,el.sixix, w, sname)
                    vars2['ExVsPhiEm'   ].fill_histogram(phi,el.Ex   , w, sname)
            if el.siyiy>1e-3:
                vars['siyiy'      ].fill_histogram(el.siyiy         , w, sname)
                vars['siyiyOSirir'].fill_histogram(el.siyiy/el.sirir, w, sname)
                vars['sixixOSiyiy'].fill_histogram(el.sixix/el.siyiy, w, sname)
                vars2['siyiyVsPhi'].fill_histogram(phi,el.siyiy, w, sname)
                vars2['EyVsPhi'   ].fill_histogram(phi,el.Ey   , w, sname)
                if el.charge>0:
                    vars2['siyiyVsPhiEp'].fill_histogram(phi,el.siyiy, w, sname)
                    vars2['EyVsPhiEp'   ].fill_histogram(phi,el.Ey   , w, sname)
                else:
                    vars2['siyiyVsPhiEm'].fill_histogram(phi,el.siyiy, w, sname)
                    vars2['EyVsPhiEm'   ].fill_histogram(phi,el.Ey   , w, sname)
            if el.sirir>1e-3:
                vars['sirir'].fill_histogram(el.sirir, w, sname)
            if el.sixix>1e-3 and el.siyiy>1e-3:
                vars['sixixMSiyiy'].fill_histogram(el.sixix*el.siyiy, w, sname)
                vars2['sixixSiyiy'].fill_histogram(el.sixix,el.siyiy, w, sname)
            vars['ps_ixy'].fill_histogram(max([el.ps_ix,el.ps_iy]), w, sname)
            vars['ps_ix0'].fill_histogram(el.ps_ix0, w, sname)
            vars['ps_iy0'].fill_histogram(el.ps_iy0, w, sname)
            vars['ps_ix' ].fill_histogram(el.ps_ix , w, sname)
            vars['ps_iy' ].fill_histogram(el.ps_iy , w, sname)
            vars['ps_ir' ].fill_histogram(el.ps_ir , w, sname)
            vars['rxy'   ].fill_histogram(el.rxy   , w, sname)
            vars['Ex'    ].fill_histogram(el.Ex    , w, sname)
            vars['Ey'    ].fill_histogram(el.Ey    , w, sname)
            vars['r9'    ].fill_histogram(el.r9    , w, sname)
            vars['e1x5'  ].fill_histogram(el.e1x5  , w, sname)
            vars['e2x5'  ].fill_histogram(el.e2x5  , w, sname)
            vars['fBrem' ].fill_histogram(el.fBrem , w, sname)
            vars['DR_mc' ].fill_histogram(el.DR    , w, sname)
            vars2['rxyVsPhi'].fill_histogram(phi,el.rxy, w, sname)
            
    for vname in vars:
        for wname in weight_names:
            h = vars[vname].h['%s_%s'%(sname,wname)]
            if h.GetSumOfWeights()>1e-3:
                h.Draw('pe')
                canvas.Print('plots/%s/h_%s_%s.eps'%(sname, vname, wname))
                canvas.Print('plots/%s/h_%s_%s.png'%(sname, vname, wname))
            
    for vname in vars2:
        for wname in weight_names:
            h = vars2[vname].h['%s_%s'%(sname,wname)]
            if h.GetSumOfWeights()>1e-3:
                h.Draw('colz')
                if 'Eta' in vname:
                    line1 = ROOT.TLine(1.653, 0, 1.653, 100)
                    line2 = ROOT.TLine(2.6  , 0, 2.6  , 100)
                    line1.SetLineColor(ROOT.kRed)
                    line2.SetLineColor(ROOT.kRed)
                    line1.Draw()
                    line2.Draw()
                canvas.Print('plots/%s/%s.eps'%(sname, h.GetName()))
                canvas.Print('plots/%s/%s.png'%(sname, h.GetName()))
file_out.Write()           
