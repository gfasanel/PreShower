# this makes histograms of variables
import array
import math, os, string
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)

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

#sample_names = ['ZprimeM1000' , 'DYEE' , 'ttbar' , 'QCD_Pt_170_300' , 'QCD_Pt_300_470' , 'QCD_Pt_470_600' , 'QCD_Pt_600_800' , 'QCD_Pt_800_1000' , 'QCD_Pt_1000_1400' , 'QCD_Pt_1400_1800' , 'QCD_Pt_1800']
sample_names = ['ZprimeToEE_M1000_v5', 'QCD_Pt_170_300' , 'QCD_Pt_300_470' , 'QCD_Pt_470_600' , 'QCD_Pt_600_800' , 'QCD_Pt_800_1000' , 'QCD_Pt_1000_1400' , 'QCD_Pt_1400_1800' , 'QCD_Pt_1800']
eta_cut = 1.43
m_window_cut = 10
#ET_labels = {'','_Et-0-100','_Et-100-200','_Et-200'}
ET_labels = {''} #just all ET range 

if not os.path.exists('plots'):
    os.makedirs('plots')
for sname in sample_names:
    if not os.path.exists('plots/%s'%sname):
        os.makedirs('plots/%s'%sname)
    if not os.path.exists('plots/2D/%s'%sname):
        os.makedirs('plots/2D/%s'%sname)
    if not os.path.exists('plots/2D/%s/Profile/'%sname):
        os.makedirs('plots/2D/%s/Profile/'%sname)

class electron_object:
    def __init__(self, p4_in, charge, preshowerEnergy, hovere, sixix, siyiy, sirir, index):
        self.charge = charge
        self.p4 = p4_in
        self.PSE = preshowerEnergy
        self.index = index
        self.region = 'B'
        self.hovere = hovere
        self.sixix = sixix
        self.siyiy = siyiy
        self.sirir = sirir
        if abs(self.p4.Eta())>eta_cut:
            self.region = 'F'
        if (self.p4.Pt()>0)*(self.p4.Pt()<100):
            self.ET_label = '_Et-0-100'
        elif (self.p4.Pt()>100)*(self.p4.Pt()<200):
            self.ET_label = '_Et-100-200'
        elif (self.p4.Pt()>200):
            self.ET_label = '_Et-200'

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
sample_labels['data'            ] = ROOT.TLatex(x, 0.82, '2012 Run D')
sample_labels['Zee'             ] = ROOT.TLatex(x, 0.82, 'Z/#gamma*#rightarrow ee')
sample_labels['singlePhoton'    ] = ROOT.TLatex(x, 0.82, 'SinglePhoton')
sample_labels['ZprimeM1000'     ] = ROOT.TLatex(x, 0.82, 'Z\' (M=1TeV)')
sample_labels['DYEE'            ] = ROOT.TLatex(x, 0.82, 'Z/#gamma*#rightarrowee')
sample_labels['QCD_Pt_170_300'  ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[100-370]')
sample_labels['QCD_Pt_300_470'  ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[300-470]')
sample_labels['QCD_Pt_470_600'  ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[470-600]')
sample_labels['QCD_Pt_600_800'  ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[600-800]')
sample_labels['QCD_Pt_800_100'  ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[800-1000]')
sample_labels['QCD_Pt_1000_1400'] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[1000-1400]')
sample_labels['QCD_Pt_1400_1800'] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[1400-1800]')
sample_labels['QCD_Pt_1800'     ] = ROOT.TLatex(x, 0.82, 'QCD p_{T}[1800+]')

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
        
        self.h = {}
        for sname in sample_names:
            for ET in ET_labels:
                hName = 'h_%s_%s%s'%(self.name, sname, ET)
                h = self.hBase.Clone(hName)
                style_histogram(h)
                self.h[sname,ET] = h
    def fill_histogram(self,value,sname,ET):
            self.h[sname,ET].Fill(value)
    
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
        
        self.h = {}
        for sname in sample_names:
            hName = 'h_%s_%s'%(self.name, sname)
            h = self.hBase.Clone(hName)
            style_histogram(h)
            self.h[sname] = h
    def fill_histogram(self,x,y,sname):
        self.h[sname].Fill(x,y)
        
vars = {}
vars['ET'         ] = var_object('ET'         , 100, 0, 1000, 'E_{T}(e)'            , 'electrons', 'GeV')
vars['PSE'        ] = var_object('PSE'        , 100, 0,  100, 'E_{PS}(e)'           , 'electrons', 'GeV')
vars['PSE_meeCut' ] = var_object('PSE_meeCut' , 100, 0,  100, 'E_{PS}(e)'           , 'electrons', 'GeV')
vars['mee'        ] = var_object('mee'        , 100, 0, 2000, 'm(ee)'               , 'Z bosons' , 'GeV')
vars['mee_wide'   ] = var_object('mee_wide'   , 100, 0, 4000, 'm(ee)'               , 'Z bosons' , 'GeV')
vars['PSEOverEt'  ] = var_object('PSEOverEt'  , 100, 0,  0.6, 'E_{PS}(e)/E_{T}(e)'  , 'electrons', '')
vars['PSEOverE'   ] = var_object('PSEOverE'   , 100, 0,  0.2, 'E_{PS}(e)/E(e)'      , 'electrons', '')
vars['PSEOverEz'  ] = var_object('PSEOverEz'  , 100, 0,  0.2, 'E_{PS}(e)/E_{z}(e)'  , 'electrons', '')
vars['sixix'      ] = var_object('sixix'      , 100, 0,   10, '#sigma_{eff}^{xx}(e)', 'electrons', '')
vars['siyiy'      ] = var_object('siyiy'      , 100, 0,   10, '#sigma_{eff}^{yy}(e)', 'electrons', '')
vars['sirir'      ] = var_object('sirir'      , 100, 0,   12, '#sigma_{eff}^{rr}(e)', 'electrons', '')
vars['sixixOSiyiy'] = var_object('sixixOSiyiy', 100, 0,  2.5, '#sigma_{eff}^{xx}(e)/#sigma_{eff}^{yy}(e)', 'electrons', '')
vars['sixixOSirir'] = var_object('sixixOSirir', 100, 0,  1.5, '#sigma_{eff}^{xx}(e)/#sigma_{eff}^{rr}(e)', 'electrons', '')
vars['siyiyOSirir'] = var_object('siyiyOSirir', 100, 0,  1.5, '#sigma_{eff}^{yy}(e)/#sigma_{eff}^{rr}(e)', 'electrons', '')
vars['sixixMSiyiy'] = var_object('sixixMSiyiy', 100, 0,   50, '#sigma_{eff}^{xx}(e)#times#sigma_{eff}^{yy}(e)', 'electrons', '')

vars2 = {} #2D histos
vars2['PSEVsEta'  ] = var2_object('PSEVsEta'  , 100, 1.4, 3.0 , 100, 0, 25.0, '|#eta| (e)', 'E_{PS}(e)' , '', ' GeV')
vars2['PSEVsHoe'  ] = var2_object('PSEVsHoe'  , 100, 0.0, 0.05, 100, 0, 25.0, 'H(e)/E(e)' , 'E_{PS}(e)' , '', ' GeV')
vars2['sixixSiyiy'] = var2_object('sixixSiyiy', 100, 0.0,   10, 100, 0,   10, '#sigma_{eff}^{xx}(e)' , '#sigma_{eff}^{yy}(e)' , '', '')

vars2['PSEVsET'        ] = var2_object('PSEVsET'        ,100, 0, 1000 , 100, 0, 100, 'E_{T} (e)', 'E_{PS}(e)' , ' GeV', ' GeV')
#vars2['PSE_meeCutVsET' ] = var2_object('PSE_meeCutVsET' ,100, 0, 1000 , 100, 0, 25.0, 'E_{T} (e)', 'E_{PS}(e)' , 'GeV', '')
vars2['PSEOverEtVsET'  ] = var2_object('PSEOverEtVsET'  ,100, 0, 1000 , 100, 0, 0.2, 'E_{T} (e)', 'E_{PS}(e)/E_{T}(e)' , ' GeV', '')
vars2['PSEOverEVsET'   ] = var2_object('PSEOverEVsET'   ,100, 0, 1000 , 100, 0, 0.2, 'E_{T} (e)', 'E_{PS}(e)/E(e)' , ' GeV', '')
vars2['PSEOverEzVsET'  ] = var2_object('PSEOverEzVsET'  ,100, 0, 1000 , 100, 0, 0.2, 'E_{T} (e)', 'E_{PS}(e)/E_{z}(e)' , ' GeV', '')
vars2['sixixVsET'      ] = var2_object('sixixVsET'      ,100, 0, 1000 , 100, 0, 10 , 'E_{T} (e)', '#sigma_{eff}^{xx}(e)' , ' GeV', '')
vars2['siyiyVsET'      ] = var2_object('siyiyVsET'      ,100, 0, 1000 , 100, 0, 10 , 'E_{T} (e)', '#sigma_{eff}^{yy}(e)' , ' GeV', '')
vars2['sirirVsET'      ] = var2_object('sirirVsET'      ,100, 0, 1000 , 100, 0, 12 , 'E_{T} (e)', '#sigma_{eff}^{irir}(e)' , ' GeV', '')
vars2['sixixOSiyiyVsET'] = var2_object('sixixOSiyiyVsET',100, 0, 1000 , 100, 0, 2.5 , 'E_{T} (e)', '#sigma_{eff}^{xx}(e)/#sigma_{eff}^{yy}(e)' , ' GeV', '')
vars2['sixixOSirirVsET'] = var2_object('sixixOSirirVsET',100, 0, 1000 , 100, 0, 1.4 , 'E_{T} (e)', '#sigma_{eff}^{xx}/(e)#sigma_{eff}^{rr}(e)' , ' GeV', '')
vars2['siyiyOSirirVsET'] = var2_object('siyiyOSirirVsET',100, 0, 1000 , 100, 0, 1.4, 'E_{T} (e)', '#sigma_{eff}^{yy}(e)/#sigma_{eff}^{rr}(e)' , ' GeV', '')
vars2['sixixMSiyiyVsET'] = var2_object('sixixMSiyiyVsET',100, 0, 1000 , 100, 0, 50 , 'E_{T} (e)', '#sigma_{eff}^{xx}(e)*#sigma_{eff}^{yy}(e)' , ' GeV', '')

events = {}
for sname in sample_names:#loop over samples
    for ET in ET_labels:#loop over Et slices
        print "ET region: ",ET
        print "sample: ",sname
        file = ROOT.TFile('ntuples/outfile_%s_skimmed_slimmed.root'%sname,'READ')
        tree = file.Get('IIHEAnalysis')
        tree.SetBranchStatus('*',0)
        tree.SetBranchStatus('gsf_pt',1)
        tree.SetBranchStatus('gsf_eta',1)
        tree.SetBranchStatus('gsf_phi',1)
        tree.SetBranchStatus('gsf_energy',1)
        tree.SetBranchStatus('gsf_eseffsirir',1)
        tree.SetBranchStatus('gsf_eseffsixix',1)
        tree.SetBranchStatus('gsf_eseffsiyiy',1)
        tree.SetBranchStatus('gsf_charge',1)
        tree.SetBranchStatus('gsf_hadronicOverEm',1)
        tree.SetBranchStatus('gsf_preshowerEnergy',1)
        tree.SetBranchStatus('gsf_n',1)
        tree.SetBranchStatus('HEEP_*',1)
        
        events[sname] = []
        nEntries = tree.GetEntries()
        nSuccess = 0
        print "for over entries"
        for i in range(0,nEntries):
            electrons = []
            tree.GetEntry(i)
            if i%10000==0:
                print i , '/' , nEntries , ' (' , nSuccess , ')'
            success = False
            for j in range(0,tree.gsf_n):
                if not tree.HEEP_gsfpass_HEEP[j]:
                    continue
                success = True
                p4 = ROOT.TLorentzVector()
                p4.SetPtEtaPhiE(tree.gsf_pt[j], tree.gsf_eta[j], tree.gsf_phi[j], tree.gsf_energy[j])
                sixix = tree.gsf_eseffsixix[j]
                siyiy = tree.gsf_eseffsiyiy[j]
                sirir = tree.gsf_eseffsirir[j]
                electrons.append(electron_object(p4, tree.gsf_charge[j], tree.gsf_preshowerEnergy[j], tree.gsf_hadronicOverEm[j], sixix, siyiy, sirir, j))
            if success:
                nSuccess = nSuccess + 1
                events[sname].append(electrons)
        
        #it closes for i in range(0,nEntries): all electrons taken 
        print len(events[sname]) , ' events with electrons'
        for ev in events[sname]:
            for el in ev:
                if el.PSE<1e-3:
                    continue
                if ET!='':#I want to fill histos regardless of Et
                    if el.ET_label!=ET:#in this case I want to fill in Et slide
                        continue
                vars['ET'].fill_histogram(el.p4.Pt(),sname,ET)
                vars['PSE'].fill_histogram(el.PSE,sname,ET)
                vars['PSEOverEt'].fill_histogram(el.PSE/el.p4.Pt(),sname,ET)
                vars['PSEOverE' ].fill_histogram(el.PSE/el.p4.E() ,sname,ET)
                vars['PSEOverEz'].fill_histogram(el.PSE/el.p4.Z() ,sname,ET)
                if el.sixix>1e-3:
                    vars['sixix'      ].fill_histogram(el.sixix,sname,ET)
                    vars['sixixOSirir'].fill_histogram(el.sixix/el.sirir,sname,ET)
                    vars2['sixixOSirirVsET'].fill_histogram(el.p4.Pt(), el.sixix/el.sirir, sname)
                if el.siyiy>1e-3:
                    vars['siyiy'      ].fill_histogram(el.siyiy,sname,ET)
                    vars['siyiyOSirir'].fill_histogram(el.siyiy/el.sirir,sname,ET)
                    vars['sixixOSiyiy'].fill_histogram(el.sixix/el.siyiy,sname,ET)
                    vars2['siyiyOSirirVsET'].fill_histogram(el.p4.Pt(), el.siyiy/el.sirir, sname)
                if el.sirir>1e-3:
                    vars['sirir'].fill_histogram(el.sirir,sname,ET)
                if el.sixix>1e-3 and el.siyiy>1e-3:
                    vars['sixixMSiyiy'].fill_histogram(el.sixix*el.siyiy,sname,ET)
                    vars2['sixixSiyiy'].fill_histogram(el.sixix,el.siyiy,sname)
                    vars2['sixixOSiyiyVsET'].fill_histogram(el.p4.Pt(), el.sixix/el.siyiy, sname)

                #2D histos
                vars2['PSEVsEta'       ].fill_histogram(el.p4.Eta(), el.PSE, sname)
                vars2['PSEVsHoe'       ].fill_histogram(el.hovere  , el.PSE, sname)
                vars2['PSEVsET'        ].fill_histogram(el.p4.Pt(), el.PSE, sname)
                vars2['PSEOverEtVsET'  ].fill_histogram(el.p4.Pt(), el.PSE/el.p4.Pt(), sname)
                vars2['PSEOverEVsET'   ].fill_histogram(el.p4.Pt(), el.PSE/el.p4.E(), sname)
                vars2['PSEOverEzVsET'  ].fill_histogram(el.p4.Pt(), el.PSE/el.p4.Z(), sname)
                vars2['sixixVsET'      ].fill_histogram(el.p4.Pt(), el.sixix, sname)
                vars2['siyiyVsET'      ].fill_histogram(el.p4.Pt(), el.siyiy, sname)
                vars2['sirirVsET'      ].fill_histogram(el.p4.Pt(), el.sirir, sname)
                vars2['sixixMSiyiyVsET'].fill_histogram(el.p4.Pt(), el.sixix*el.siyiy, sname)

            
        #Saving histos, containing the useful variables
        for vname in vars:#it closes for ev in events[sname]
            h = vars[vname].h[sname,ET]    
            if h.GetSumOfWeights()>1e-3:
                h.Draw('pe')
                canvas.Print('plots/%s/h_%s%s.eps'%(sname, vname,ET))
                canvas.Print('plots/%s/h_%s%s.png'%(sname, vname,ET))
            
        for vname in vars2:#2D histo
            h = vars2[vname].h[sname]
            if h.GetSumOfWeights()>1e-3:
                h.Draw('colz')
                if 'Eta' in vname:
                    line1 = ROOT.TLine(1.653, 0, 1.653, 25)
                    line2 = ROOT.TLine(2.6  , 0, 2.6  , 25)
                    line1.SetLineColor(ROOT.kRed)
                    line2.SetLineColor(ROOT.kRed)
                    line1.Draw()
                    line2.Draw()
                canvas.Print('plots/2D/%s/%s.eps'%(sname, h.GetName()))
                canvas.Print('plots/2D/%s/%s.png'%(sname, h.GetName()))
                profiled=h.ProfileX()
                profiled.GetYaxis().SetTitle(h.GetYaxis().GetTitle())
                style_histogram(profiled)
                profiled.Draw("ep")
                canvas.Print('plots/2D/%s/Profile/%s.eps'%(sname, h.GetName()))
                canvas.Print('plots/2D/%s/Profile/%s.png'%(sname, h.GetName()))
            
file_out.Write()           
