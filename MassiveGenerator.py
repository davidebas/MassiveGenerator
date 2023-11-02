##################################################################
# Generate instructions for massive SNiPER simulations (version J23.1.0-rc0)
# Authors: D. Basilico - davide.basilico@mi.infn.it 
#          M. Malabarba - marco.malabarba@mi.infn.it
##################################################################

import os
import random
import sys
import argparse

prs = argparse.ArgumentParser()           # parser name

prs.add_argument("-name","--NameRun",help="Name of the run",required=True)
prs.add_argument("-s","--Species", help="Which solar neutrino species \n or background species (Bi-210, Kr-85, Po-210, K-40, U-238, Th-232, C-11, C-10, He-6) \n or mono-energetic particles (mono) or reactor anti-neutrinos (antinu) \n or calib source (usage: calib_isotope_ACU/CLS/GT_coordinates. Example: calib_Sr85_ACU_0_0_0 )")                 
prs.add_argument("-isotope", "--Isotope", help="Isotope decaying")
prs.add_argument("-runs", "--HowMany", help="How many rootfiles",type=int)
prs.add_argument("-events", "--EventsPerRun", help="How many events per run",type=int)

prs.add_argument("-t","--threshold", default=300,help="NPMTs trigger threshold; default 300")

prs.add_argument("-generate-center","--GenerateCenter",default="false",help="To generate all the primary particles exactly in the center of the detector; default=false")

prs.add_argument("-volume-radius-min","--VolumeRadiusMin", default=0.0, type=float, help="min of the radius (only if GenerateCenter=false); default=0")
prs.add_argument("-volume-radius-max","--VolumeRadiusMax", default=17000, type=float, help="max of the radius (only if GenerateCenter=false); default=17000mm")

prs.add_argument("-particle-energy", "--ParticleEnergy", help="Particle Kinetic energy (only if Species=mono); default 1.0MeV", default=1.0, type=float)
prs.add_argument("-energy-mode","--EnergyMode",help="If you want to generate energy with smear (only if Species=mono), Possibilities: Range, Gaus, delta; default=delta",default="delta")
prs.add_argument("-energy-extra-parameter","--EnergyExtraParameter",help="Only if EnergyMode is Range or Gaus. If EnergyMode=Range -> particles energy is uniformely distributed between [ParticleEnergy; EnergyExtraParameter]. If EnergyMode=Gaus -> particles energy is gaussianly distributed with mu=ParticleEnergy and sigma=EnergyExtraParameter",default=0.)             
prs.add_argument("-particle-type", "--ParticleType", help="Particle type (only if Species=mono); default e-", default='e-')             
prs.add_argument("-mass-ordering", "--MassOrdering", help="Neutrino mass ordering for simulations (only if Species=antinu); Possibilities: normal or inverted; default: normal",default='normal')
prs.add_argument("-elec2rec", "--elec2rec", help="is elec2rec used?; default true", default='true')             
prs.add_argument("-trigger-mode","--TriggerMode",help='Trigger Std or VFL; default Std',default='onlyStd')
prs.add_argument("-light-yield","--LightYield", help='LS light yield; default: 9846/MeV (see doc-db 8400)',default=9846,type=int)

prs.add_argument("-cherenkov-yield","--CherenkovYieldFactor", help='Cherenkov yield factor; default: 0.517 (see doc-db 8400); set to zero to disable the Cherenkov effect',default=0.517,type=float)
prs.add_argument("-birks-constant1","--BirksConstant1", help='First Birks constant; default: 12.05e-3g/cm2/MeV (see doc-db 8400)',default=12.05e-3,type=float)
prs.add_argument("-birks-constant2","--BirksConstant2", help='Second Birks constant; default: 0 (see doc-db 8400)',default=0,type=float)
prs.add_argument("-enable-quenching","--EnableQuenching", help='Activate/De-activate the quenching effect; default: true',default='true')
prs.add_argument("-enable-scattering","--EnableScattering", help='Activate/De-activate Rayleigh scattering; default: true',default='true')
prs.add_argument("-enable-absorption","--EnableAbsorption", help='Activate/De-activate the absorption; default: true',default='true')
prs.add_argument("-enable-reemission","--EnableReEmission", help='Activate/De-activate the re-emission; default: true',default='true')
prs.add_argument("-use-sheldon-emission-spectrum","--UseSheldonEmissionSpectrum", help='Use Sheldons emission spectrum or not; default: false',default='false')
prs.add_argument("-use-sheldon-fluorescence-times","--UseSheldonFluorescenceTimes", help='Use Sheldons fluorescence times or not; default: false',default='false')

prs.add_argument("-SPMT","--ActivationSmallPMTs",help="Enable the small PMTs; default: true",default="true",choices=["true","false"])
prs.add_argument("-LPMT","--ActivationLargePMTs",help="Enable the large PMTs; default: true",default="true",choices=["true","false"])
prs.add_argument("-TTS","--TTSActivation",help="Activate the Transit Time Spread of the PMTs; default: true",default="true",choices=["true","false"])
prs.add_argument("-noise","--NoiseActivation",help="Activate the white noise of the PMTs; default: true",default="true",choices=["true","false"])

args = prs.parse_args()

NameRun = str(args.NameRun) #name of the run, required

Species = str(args.Species)
Isotope = str(args.Isotope)
HowMany = args.HowMany
EventsPerRun = str(args.EventsPerRun)
Threshold = str(args.threshold)
ParticleEnergy = str(args.ParticleEnergy)
EnergyMode = str(args.EnergyMode)
EnergyExtraParameter = str(float(args.EnergyExtraParameter))
ParticleType = str(args.ParticleType)
GenerateCenter = str(args.GenerateCenter)
VolumeRadiusMax = str(int(args.VolumeRadiusMax))
VolumeRadiusMin = str(int(args.VolumeRadiusMin))
elec2rec = str(args.elec2rec)
TriggerMode = str(args.TriggerMode)
MassOrdering = str(args.MassOrdering)
LightYield = str(int(args.LightYield))
CherenkovYieldFactor = str(float(args.CherenkovYieldFactor))
BirksConstant1 = str(float(args.BirksConstant1))
BirksConstant2 = str(float(args.BirksConstant2))
EnableQuenching = str(args.EnableQuenching)
EnableScattering = str(args.EnableScattering)
EnableAbsorption = str(args.EnableAbsorption)
EnableReEmission = str(args.EnableReEmission)
UseSheldonEmissionSpectrum = str(args.UseSheldonEmissionSpectrum)
UseSheldonFluorescenceTimes = str(args.UseSheldonFluorescenceTimes)

SPMTsActivation=str(args.ActivationSmallPMTs)
LPMTsActivation=str(args.ActivationLargePMTs)
TTSActivation=str(args.TTSActivation)
NoiseActivation=str(args.NoiseActivation)

if os.path.exists(NameRun) :
	print("WARNING : A run named " + NameRun + " already exists, want to continue anyway?")
	response = input("Print y/n: ")
	if(response == 'n'):
		print("Aborted.")
		sys.exit()
	else:
		print("Not interrupted.")


if (SPMTsActivation == "false" and LPMTsActivation == "false") :
    print("WARNING: Are you sure you want to deactivate both large and small PMTs ?")
    ManageWarning()

if (int(Threshold) < 200) :
    print("WARNING: Lowering the threshold to " + str(Threshold) + " could raise issues in the simulation, especially if you did not disactivate white noise, want to continue anyway?")

CurrentFolder = os.getcwd()

print(os.getcwd())


if( Species == 'mono'):
    lineSpecies ='gun --particles ' + ParticleType + ' --momentums ' + ParticleEnergy 
    Species = Species + '_' + ParticleType + '_' + ParticleEnergy + 'MeV'
    
    if (EnergyMode!="delta" and EnergyExtraParameter!="0"):

        if (EnergyMode!="Gaus" and EnergyMode!="Range"):
            sys.exit("Unrecognized EnergyMode, please choose between Range, Gaus, delta")

        lineSpecies+=(" --momentums-mode "+EnergyMode+" --momentums-extra-params "+EnergyExtraParameter)
        Species+=("-"+EnergyExtraParameter+"MeV-"+EnergyMode)

    lineSpecies+= ' --momentums-interp KineticEnergy'

if( Species == 'nuclear'):
	lineSpecies = 'gendecay --nuclear ' + Isotope

if( Species.startswith('calib') ):
	calib_parts = Species.split("_", 6)
	if(calib_parts[2] == 'ACU'):
		InsertionSystem = "--ACU_source_weight_QC "
	if(calib_parts[2] == 'CLS'):
		InsertionSystem = "--CLS_source_weight_QC "
	if(calib_parts[2] == 'ROV'):
		InsertionSystem = "--submarine "

	lineSpecies = InsertionSystem + ' --OffsetInX ' + calib_parts[3] + ' --OffsetInY ' + calib_parts[4] + ' --OffsetInZ ' + calib_parts[5] + ' gun --particles /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J22.1.0-rc4/offline/Examples/Tutorial/share/mac/config/' + calib_parts[1] + '.conf '  

if( (Species == 'Be7') or (Species == 'pep') or (Species == 'hep') or (Species == 'B8') or (Species == 'pp') or (Species =='N13') or (Species == 'O15')):
    lineSpecies = 'nusol --type ' + Species

if( (Species == 'Th-232') or (Species == 'Po-210') or (Species == 'Kr-85') or (Species == 'K-40') or (Species == 'C-11') or (Species == 'C-10') or (Species == 'He-6') or (Species == 'B-12') or (Species=='C-14')):
    lineSpecies = 'gendecay --nuclear ' + Species

if( Species == 'Bi-210' ):
    lineSpecies = 'gendecay --nuclear Bi-210 --stop-nuclear Po-210'

if( Species == 'U-238' ):
    lineSpecies = 'gendecay --nuclear U-238 --stop-nuclear Pb-210'

if (Species == 'antinu'):
    if (MassOrdering!="normal" and MassOrdering!="inverted"):
        sys.exit("Unrecognized mass ordering, please choose between normal and inverted")
    if (MassOrdering=="normal"):
        lineSpecies = 'hepevt --exe IBD-NH'
    if (MassOrdering=="inverted"):
        lineSpecies = 'hepevt --exe IBD-IH'


oo = open('CondorScriptToLaunch_' + NameRun + '.sh',"w")

#making the required directories

if not os.path.exists(NameRun):
    os.makedirs(NameRun)

if not os.path.exists(NameRun + '/log'):
    os.makedirs(NameRun + '/log')

if not os.path.exists(NameRun + '/err'):
    os.makedirs(NameRun + '/err')

if not os.path.exists(NameRun + '/out'):
    os.makedirs(NameRun + '/out')

if not os.path.exists(NameRun + '/root'):
    os.makedirs(NameRun + '/root')

if not os.path.exists(NameRun + '/sh'):
    os.makedirs(NameRun + '/sh')

if not os.path.exists(NameRun + '/sub'):
    os.makedirs(NameRun + '/sub')

if not os.path.exists(NameRun + '/match'):
    os.makedirs(NameRun + '/match')


print('cd ' + NameRun)

os.chdir(os.getcwd() + '/' + NameRun)

if GenerateCenter=="false":
    if Species.startswith('calib'):
    	VolumeRadiusString = " --material LS --volume pSource --material Analcime "
    
    else:
    	VolumeRadiusString = " --volume pTarget --material LS --volume-radius-max " + VolumeRadiusMax
	
    if (VolumeRadiusMin!="0"): 
        VolumeRadiusString += " --volume-radius-min " + VolumeRadiusMin
else:
    VolumeRadiusString=""
    VolumeRadiusMax="0"

	

CherenkovString=" "
if CherenkovYieldFactor=="0.0":
	CherenkovString+="--no-cerenkov"
else:
	CherenkovString+=("--cerenkov-yield-factor "+CherenkovYieldFactor)

if EnableQuenching=="false":
	CherenkovString+=" --no-quenching"

ReplaceString=" --replace-param Material.LS.ConstantProperty.ScintillationYield:"+LightYield+"/MeV,Material.LS.scale.LSLY_NewPMTModelScale:1.0"
if EnableQuenching=="true":
	ReplaceString+=(",Material.LS.ConstantProperty.BirksConstant1:"+BirksConstant1+"*g/cm2/MeV,Material.LS.ConstantProperty.BirksConstant2:"+BirksConstant2)


if EnableScattering=="false":
	ReplaceString+=(",Material.LS.RAYLEIGH:/storage/gpfs_data/juno/junofs/users/mmalabarba/modified_LS_properties/RAYLEIGH")

if EnableAbsorption=="false":
	ReplaceString+=(",Material.LS.ABSLENGTH_v1:/storage/gpfs_data/juno/junofs/users/mmalabarba/modified_LS_properties/ABSLENGTH_v1")

if EnableReEmission=="false":
	ReplaceString+=(",Material.LS.REEMISSIONPROB:/storage/gpfs_data/juno/junofs/users/mmalabarba/modified_LS_properties/REEMISSIONPROB")

if UseSheldonEmissionSpectrum=="true":
	ReplaceString+=(",Material.LS.FASTCOMPONENT:/storage/gpfs_data/juno/junofs/users/mmalabarba/modified_LS_properties/EMISSION_SHELDON,Material.LS.SLOWCOMPONENT:/storage/gpfs_data/juno/junofs/users/mmalabarba/modified_LS_properties/EMISSION_SHELDON")

if UseSheldonFluorescenceTimes=="true":
	ReplaceString+=(",Material.LS.NeutronCONSTANT:/storage/gpfs_data/juno/junofs/users/mmalabarba/modified_LS_properties/NeutronCONSTANT,Material.LS.AlphaCONSTANT:/storage/gpfs_data/juno/junofs/users/mmalabarba/modified_LS_properties/AlphaCONSTANT,Material.LS.GammaCONSTANT:/storage/gpfs_data/juno/junofs/users/mmalabarba/modified_LS_properties/GammaCONSTANT")

RateSpecies = str(0.001)

DetsimPathsFile=open("match/detsim_paths.txt","w")
RecPathsFile=open("match/rec_paths.txt","w")

for i in range(0,int(HowMany)):
    filename = 'sh/Launch_' + NameRun + '_' + str(i).zfill(4) + '.sh'
    print(filename)
    of = open(filename,"w")

    Output_DetSimEDM    = os.getcwd() + '/root/' + NameRun + '_detsim_'  + str(i).zfill(4) + '.root'
    Output_DetSimUser   = os.getcwd() + '/root/' + NameRun + '_detsim_user_' + str(i).zfill(4) + '.root'
    Output_ElecEDM      = os.getcwd() + '/root/' + NameRun + '_elecsim_' + str(i).zfill(4) + '.root'
    Output_ElecUser     = os.getcwd() + '/root/' + NameRun + '_elecsim_user_' + str(i).zfill(4) + '.root'
    Output_CalibEDM     = os.getcwd() + '/root/' + NameRun + '_calib_' + str(i).zfill(4) + '.root'
    Output_CalibUser    = os.getcwd() + '/root/' + NameRun + '_calib_user_' + str(i).zfill(4) + '.root'
    Output_RecEDM       = os.getcwd() + '/root/' + NameRun + '_rec_' + str(i).zfill(4) + '.root'
    Output_RecUser      = os.getcwd() + '/root/' + NameRun + '_rec_user_' + str(i).zfill(4) + '.root'
    Output_DetSim_Log   = os.getcwd() + '/log/' + NameRun + '_detsim_user_' + str(i).zfill(4) + '.log'
    Output_Log          = os.getcwd() + '/log/'  + NameRun + '_rec_user_' + str(i).zfill(4) + '.log'
    
    if i!=0:
        DetsimPathsFile.write("\n")
        RecPathsFile.write("\n")

    DetsimPathsFile.write(Output_DetSimUser)
    RecPathsFile.write(Output_RecUser)

    if( Species == 'mono'):
            Species = 'mono_' + ParticleType + '_' + ParticleEnergy

    of.write('#!/bin/bash\n')
    of.write('export LC_ALL=C\n')
    of.write('export CMTCONFIG=amd64_linux26\n')
    of.write('source /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc1120/Pre-Release/J23.1.0-rc0/setup.sh\n')
    of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc1120/Pre-Release/J23.1.0-rc0/junosw/Examples/Tutorial/share/tut_detsim.py --no-gdml --evtmax ' + EventsPerRun +' --seed ' + str(random.randint(1e6,1e7)) + ' --output ' + Output_DetSimEDM + " --user-output " + Output_DetSimUser + ' --anamgr-normal-hit ' + lineSpecies + VolumeRadiusString + ' >&  ' + Output_DetSim_Log + ' \n')

    of.write('\nsleep 10\n')

    if( elec2rec == 'false'):
    	of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc1120/Pre-Release/J23.1.0-rc0/junosw/Examples/Tutorial/share/tut_det2elec.py --input ' + Output_DetSimEDM + ' --output ' + Output_ElecEDM + ' --user-output ' + Output_ElecUser + ' --evtmax -1 --Trigger_Mode ' + TriggerMode + ' --rate ' + RateSpecies + ' --seed ' + str(random.randint(1e6,1e7)) + '\n')

    	of.write('\nsleep 10\n')

    	of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc1120/Pre-Release/J23.1.0-rc0/junosw/Examples/Tutorial/share/tut_elec2calib.py --evtmax -1 --input ' + Output_ElecEDM + ' --output ' + Output_CalibEDM  + ' --user-output ' + Output_CalibUser +  '\n')
    	of.write('\nsleep 10\n')

    	of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc1120/Pre-Release/J23.1.0-rc0/junosw/Examples/Tutorial/share/tut_calib2rec.py --evtmax -1 --input '+ Output_CalibEDM + ' --output ' + Output_RecEDM  + ' --user-output ' + Output_RecUser + ' --elec yes --method energy-point --simfile ' + Output_DetSimUser + ' --enableReadTruth --enableTimeInfo --enableTimeInfo --enableLTSPEs >> ' + Output_Log  + ' \n')
    	of.write('\nsleep 10\n')
    
    if( elec2rec == 'true'):
        of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc1120/Pre-Release/J23.1.0-rc0/junosw/Examples/Tutorial/share/tut_elec2rec.py --input ' + Output_DetSimEDM + ' --output ' + Output_RecEDM + ' --user-output ' + Output_RecUser + ' --evtmax -1 --Trigger_Mode ' + TriggerMode + ' --rate ' + RateSpecies + ' --seed ' + str(random.randint(1e6,1e7)) + ' --elec yes --enableReadTruth --method energy-point --simfile ' + Output_DetSimUser + ' --enableTimeInfo --enableUseEkMap --enableLTSPEs >& ' + Output_Log + '\n')

    of.close()
    os.system('chmod 774 ' + filename)

DetsimPathsFile.close()
RecPathsFile.close()

for i in range(0,int(HowMany)):
    filename = 'Launch_' + NameRun + '_' + str(i).zfill(4) + '.sub'
    print(filename)
    of = open('sub/' + filename,"w")
    of.write('universe = vanilla\n')
    of.write('getenv = true\n')
    of.write('executable = ' + os.getcwd() + '/sh/Launch_' + NameRun + '_' + str(i).zfill(4) + '.sh\n')
    of.write('log = ' + os.getcwd() + '/log/' + NameRun + '_' + str(i).zfill(4) + '.log\n')
    of.write('output = ' + os.getcwd() + '/out/' + NameRun + '_' + str(i).zfill(4)  + '.out\n')
    of.write('error = ' + os.getcwd() + '/err/' + NameRun + '_' + str(i).zfill(4) + '.err\n')
    of.write('+MaxRuntime = 86400\n')
    of.write('ShouldTransferFiles = YES\n')
    of.write('WhenToTransferOutput = ON_EXIT\n')
    of.write('queue 1\n')
    of.close()
    oo.write('condor_submit -name sn-02.cr.cnaf.infn.it ' + NameRun + '/sub/' + filename + '\n')
    
oo.close()