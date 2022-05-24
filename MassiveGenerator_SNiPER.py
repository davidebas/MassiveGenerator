##################################################################
# Generate instructions for massive SNiPER simulations
# Author: D. Basilico - davide.basilico@mi.infn.it - May 2022
##################################################################

import os
import random
import sys
import argparse

Threshold = str(200)

prs = argparse.ArgumentParser()           # parser name
prs.add_argument("-s","--Species", help="Which neutrino species (Be7, pep, CNO, pp, hep, N13, O15) \n or background species (Bi-210, Kr-85, Po-210, K-40, U-238, Th-232, C-11, C-10, He-6) or mono-energetic particles (mono) ")                 
prs.add_argument("-runs", "--HowMany", help="How many rootfiles",type=int)
prs.add_argument("-events", "--EventsPerRun", help="How many events per run",type=int)

prs.add_argument("-t","--threshold", default=300,help="NPMTs trigger threshold; default 300")
prs.add_argument("-volume-radius-min","--VolumeRadiusMin", default=0.0, type=float, help="min of the radius")
prs.add_argument("-volume-radius-max","--VolumeRadiusMax", default=17000, type=float, help="max of the radius")

prs.add_argument("-particle-energy", "--ParticleEnergy", help="Particle Kinetic energy (only if Species=mono); default 1.0", default=1.0, type=float)             
prs.add_argument("-particle-type", "--ParticleType", help="Particle type (only if Species=mono); default e-", default='e-')             

prs.add_argument("-elec2rec", "--elec2rec", help="is elec2rec used?; default true", default='true')             
prs.add_argument("-trigger-mode","--TriggerMode",help='Trigger Std or VFL; default Std',default='onlyStd')

args = prs.parse_args()

Species = str(args.Species)
HowMany = args.HowMany
EventsPerRun = str(args.EventsPerRun)
Threshold = str(args.threshold)
ParticleEnergy = str(args.ParticleEnergy)
ParticleType = str(args.ParticleType)
VolumeRadiusMax = str(int(args.VolumeRadiusMax))
elec2rec = str(args.elec2rec)
TriggerMode = str(args.TriggerMode)

CurrentFolder = os.getcwd()

print(os.getcwd())


if( Species == 'mono'):
    lineSpecies ='gun --particles ' + ParticleType + ' --momentums ' + ParticleEnergy + ' --momentums-interp KineticEnergy'
    Species = Species + '_' + ParticleType + '_' + ParticleEnergy + 'MeV'

if( (Species == 'Be7') or (Species == 'pep') or (Species == 'hep') or (Species == 'B8') or (Species == 'pp') or (Species =='N13') or (Species == 'O15')):
    lineSpecies = 'nusol --type ' + Species

if( (Species == 'Th-232') or (Species == 'Po-210') or (Species == 'Kr-85') or (Species == 'K-40') or (Species == 'C-11') or (Species == 'C-10') or (Species == 'He-6') or (Species == 'B-12') or (Species=='C-14')):
    lineSpecies = 'gendecay --nuclear ' + Species

if( Species == 'Bi-210' ):
    lineSpecies = 'gendecay --nuclear Bi-210 --stop-nuclear Po-210'

if( Species == 'U-238' ):
    lineSpecies = 'gendecay --nuclear U-238 --stop-nuclear Pb-210'

oo = open('CondorScriptToLaunch_' + Species + '_Thr' + Threshold + '.sh',"w")

if not os.path.exists(Species):
        os.makedirs(Species)

if not os.path.exists(Species + '/log'):
        os.makedirs(Species + '/log')

if not os.path.exists(Species + '/err'):
        os.makedirs(Species + '/err')

if not os.path.exists(Species + '/out'):
        os.makedirs(Species + '/out')

if not os.path.exists(Species + '/root'):
        os.makedirs(Species + '/root')

if not os.path.exists(Species + '/sh'):
        os.makedirs(Species + '/sh')

if not os.path.exists(Species + '/sub'):
        os.makedirs(Species + '/sub')


print('cd ' + Species)

os.chdir(os.getcwd() + '/' + Species)
VolumeRadiusString = "--volume-radius-max " + VolumeRadiusMax
RateSpecies = str(0.001)

for i in range(0,int(HowMany)):
    filename = 'sh/Launch_' + Species + '_' + str(i).zfill(4) + '_Thr' + Threshold + '.sh'
    print(filename)
    of = open(filename,"w")

    Output_DetSimEDM    = os.getcwd() + '/root/' + Species + '_detsim_r' + VolumeRadiusMax + '_' + str(i).zfill(4) + '.root'
    Output_DetSimUser   = os.getcwd() + '/root/' + Species + '_detsim_user_r' + VolumeRadiusMax + '_' + str(i).zfill(4) + '.root'
    Output_ElecEDM      = os.getcwd() + '/root/' + Species + '_elecsim_r' + VolumeRadiusMax + '_' + str(i).zfill(4) + '.root'
    Output_ElecUser     = os.getcwd() + '/root/' + Species + '_elecsim_user_r' + VolumeRadiusMax + '_' + str(i).zfill(4) + '.root'
    Output_CalibEDM     = os.getcwd() + '/root/' + Species + '_calib_r' + VolumeRadiusMax + '_' + str(i).zfill(4) + '.root'
    Output_CalibUser    = os.getcwd() + '/root/' + Species + '_calib_user_r' + VolumeRadiusMax + '_' + str(i).zfill(4) + '.root'
    Output_RecEDM       = os.getcwd() + '/root/' + Species + '_rec_r' + VolumeRadiusMax + '_' + str(i).zfill(4) + '.root'
    Output_RecUser      = os.getcwd() + '/root/' + Species + '_rec_user_r' + VolumeRadiusMax + '_' + str(i).zfill(4) + '.root'
    Output_Log          = os.getcwd() + '/log/'  + Species + '_rec_user_r' + VolumeRadiusMax + '_' + str(i).zfill(4) + '.log'
    

    if( Species == 'mono'):
            Species = 'mono_' + ParticleType + '_' + ParticleEnergy

    of.write('#!/bin/bash\n')
    of.write('export LC_ALL=C\n')
    of.write('export CMTCONFIG=amd64_linux26\n')
    of.write('source /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J22.1.0-rc1/setup.sh\n')
    of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J22.1.0-rc1/offline/Examples/Tutorial/share/tut_detsim.py --no-gdml --evtmax ' + EventsPerRun +' --seed ' + str(random.randint(1e6,1e7)) + ' --output ' + Output_DetSimEDM + " --user-output " + Output_DetSimUser + ' --anamgr-normal-hit ' + lineSpecies + ' --volume pTarget --material LS ' + VolumeRadiusString + ' >&  ' + Output_Log + ' \n')

    of.write('\nsleep 10\n')

    if( elec2rec == 'false'):
    	of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J22.1.0-rc1/offline/Examples/Tutorial/share/tut_det2elec.py --input ' + Output_DetSimEDM + ' --output ' + Output_ElecEDM + ' --user-output ' + Output_ElecUser + ' --evtmax -1 --Trigger_Mode ' + TriggerMode + ' --rate ' + RateSpecies + ' --seed ' + str(random.randint(1e6,1e7)) + '\n')

    	of.write('\nsleep 10\n')

    	of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J22.1.0-rc1/offline/Examples/Tutorial/share/tut_elec2calib.py --evtmax -1 --input ' + Output_ElecEDM + ' --output ' + Output_CalibEDM  + ' --user-output ' + Output_CalibUser +  '\n')
    	of.write('\nsleep 10\n')

    	of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J22.1.0-rc1/offline/Examples/Tutorial/share/tut_calib2rec.py --evtmax -1 --input '+ Output_CalibEDM + ' --output ' + Output_RecEDM  + ' --user-output ' + Output_RecUser + ' --elec yes --method energy-point --simfile ' + Output_DetSimUser + ' --enableReadTruth --enableUseTLHVertex --enableTimeInfo --enableLTSPEs >> ' + Output_Log  + ' \n')
    	of.write('\nsleep 10\n')
    
    if( elec2rec == 'true'):
    #    of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J22.1.0-rc1/offline/Examples/Tutorial/share/tut_elec2rec.py --input ' + Output_DetSimEDM + ' --output ' + Output_RecEDM + ' --user-output ' + Output_RecUser + ' --evtmax -1 --Trigger_Mode ' + TriggerMode + ' --rate ' + RateSpecies + ' --seed ' + str(random.randint(1e6,1e7)) + ' --elec yes --method energy-point --simfile ' + Output_DetSimUser + ' --enableReadTruth --enableUseTLHVertex --enableTimeInfo --enableLTSPEs --evtrec >& ' + Output_Log + '\n')
        of.write('python /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J22.1.0-rc1/offline/Examples/Tutorial/share/tut_elec2rec.py --input ' + Output_DetSimEDM + ' --output ' + Output_RecEDM + ' --user-output ' + Output_RecUser + ' --evtmax -1 --Trigger_Mode ' + TriggerMode + ' --rate ' + RateSpecies + ' --seed ' + str(random.randint(1e6,1e7)) + ' --elec yes --enableReadTruth --method energy-point --simfile ' + Output_DetSimUser + ' --enableUseTLHVertex --enableUseEkMap --enableLTSPEs --evtrec >& ' + Output_Log + '\n')

    of.close()
    os.system('chmod 774 ' + filename)


for i in range(0,int(HowMany)):
    filename = 'Launch_' + Species + '_' + str(i).zfill(4) + '_Thr' + Threshold + '.sub'
    print(filename)
    of = open('sub/' + filename,"w")
    of.write('universe = vanilla\n')
    of.write('getenv = true\n')
    of.write('executable = ' + os.getcwd() + '/sh/Launch_' + Species + '_' + str(i).zfill(4) + '_Thr' + Threshold + '.sh\n')
    of.write('log = ' + os.getcwd() + '/log/' + Species + '_' + str(i).zfill(4) + '_Thr' + Threshold + '.log\n')
    of.write('output = ' + os.getcwd() + '/out/' + Species + '_' + str(i).zfill(4) + '_Thr' + Threshold + '.out\n')
    of.write('error = ' + os.getcwd() + '/err/' + Species + '_' + str(i).zfill(4) + '_Thr' + Threshold + '.err\n')
    of.write('+MaxRuntime = 86400\n')
    of.write('ShouldTransferFiles = YES\n')
    of.write('WhenToTransferOutput = ON_EXIT\n')
    of.write('queue 1\n')
    of.close()
    oo.write('condor_submit -name sn-02.cr.cnaf.infn.it ' + Species + '/sub/' + filename + '\n')

oo.close()
