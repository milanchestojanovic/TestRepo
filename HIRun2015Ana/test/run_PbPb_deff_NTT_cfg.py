import FWCore.ParameterSet.Config as cms

process = cms.Process('TRACKANA')
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.ReconstructionHeavyIons_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('TrackingCode.HIRun2015Ana.HITrackCorrectionAnalyzer_cfi')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('trk.root')
)

process.load("SimTracker.TrackAssociation.trackingParticleRecoTrackAsssociation_cfi")

process.tpRecoAssocGeneralTracks = process.trackingParticleRecoTrackAsssociation.clone()
process.tpRecoAssocGeneralTracks.label_tr = cms.InputTag("hiGeneralAndPixelTracks")

process.load("SimTracker.TrackAssociatorProducers.quickTrackAssociatorByHits_cfi")
process.quickTrackAssociatorByHits.SimToRecoDenominator = cms.string('reco')

process.load("SimTracker.TrackerHitAssociation.clusterTpAssociationProducer_cfi")

# Input source
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames =  cms.untracked.vstring(
#'/store/user/caber/RecoNewPixelTracks_EricValues_HitsCut0_758p5/Hydjet_Quenched_MinBias_5020GeV_750/RecoNewPixelTracks_EricValues_HitsCut0_758p5/160706_100506/0000/file_step3_1.root',
'/store/user/caber/RecoNewPixelTracks_EricValues_HitsCut0/Hydjet_Quenched_MinBias_5020GeV_750/RecoNewPixelTracks_EricValues_HitsCut0/160510_171012/0000/file_step3_1.root'
#'/store/user/dgulhan/PYTHIA_QCD_TuneCUETP8M1_cfi_GEN_SIM_5020GeV/Pythia8_Dijet80_pp_TuneCUETP8M1_Hydjet_MinBias_5020GeV_RECODEBUG_758_PrivMC/151217_175524/0000/step3_102.root'
#'/store/user/velicanu/Hydjet_Quenched_MinBias_5020GeV_750/Hydjet_Quenched_MinBias_5020GeV_750_RECODEBUG_v0/151117_112112/0000/step3_102.root'
),

#    eventsToProcess = cms.untracked.VEventRange('1:6652:352538')

)
### centrality ###
process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi") 
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")
process.centralityBin.nonDefaultGlauberModel = cms.string("HydjetDrum5")

### Track cuts ###
# input collections
process.HITrackCorrections.centralitySrc = cms.InputTag("centralityBin","HFtowers")
process.HITrackCorrections.trackSrc = cms.InputTag("hiGeneralAndPixelTracks")
process.HITrackCorrections.trackSrc1 = cms.InputTag("hiGeneralAndPixelTracks")
process.HITrackCorrections.qualityString = cms.string("highPurity")
process.HITrackCorrections.pfCandSrc = cms.untracked.InputTag("particleFlowTmp")
process.HITrackCorrections.jetSrc = cms.InputTag("akPu4CaloJets")
# options
process.HITrackCorrections.useCentrality = True
process.HITrackCorrections.applyTrackCuts = True
process.HITrackCorrections.fillNTuples = False
process.HITrackCorrections.applyVertexZCut = True
process.HITrackCorrections.doVtxReweighting = False
process.HITrackCorrections.doCaloMatched = False
# cut values
process.HITrackCorrections.dxyErrMax = 3.0
process.HITrackCorrections.dzErrMax = 3.0
process.HITrackCorrections.ptErrMax = 0.3
process.HITrackCorrections.nhitsMin = 0
process.HITrackCorrections.chi2nMax = 9999.0
process.HITrackCorrections.reso = 0.2
#process.HITrackCorrections.crossSection = 1.0 #1.0 is no reweigh
#algo 
process.HITrackCorrections.algoParameters = cms.vint32(1,2,3,4,5,6,7,8,9,10,11,12)
# vertex reweight parameters
process.HITrackCorrections.vtxWeightParameters = cms.vdouble(0.0306789, 0.427748, 5.16555, 0.0228019, -0.02049, 7.01258 )
###
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_mcRun2_HeavyIon_v11', '')
###
process.p = cms.Path(
                      process.tpClusterProducer *
                      process.quickTrackAssociatorByHits *
                      process.tpRecoAssocGeneralTracks *
                      process.centralityBin *
                      process.HITrackCorrections
)
