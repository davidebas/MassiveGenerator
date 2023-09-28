# MassiveGenerator
MassiveGenerator

Script for SNiPER submission jobs.
Generation of all the folder and files required:
- CondorScriptToLaunch script (.sh) to be launched to start the submission (source CondoScriptToLaunch_Something.sh)
- root, err, log, sh, sub folders
- .sub file (in /sub folder) handling the submission to CNAF nodes
- .sh file (in /sh folder) including the SNiPER instructions (based on detsim and elec2rec) 

usage: MassiveGenerator.py [-h] -name NAMERUN [-s SPECIES] [-runs HOWMANY] [-events EVENTSPERRUN] [-t THRESHOLD] [-generate-center GENERATECENTER] [-volume-radius-min VOLUMERADIUSMIN] [-volume-radius-max VOLUMERADIUSMAX]
                           [-particle-energy PARTICLEENERGY] [-energy-mode ENERGYMODE] [-energy-extra-parameter ENERGYEXTRAPARAMETER] [-particle-type PARTICLETYPE] [-mass-ordering MASSORDERING] [-elec2rec ELEC2REC]
                           [-trigger-mode TRIGGERMODE] [-light-yield LIGHTYIELD] [-cherenkov-yield CHERENKOVYIELDFACTOR] [-birks-constant1 BIRKSCONSTANT1] [-birks-constant2 BIRKSCONSTANT2] [-enable-quenching ENABLEQUENCHING]
                           [-enable-scattering ENABLESCATTERING] [-enable-absorption ENABLEABSORPTION] [-enable-reemission ENABLEREEMISSION] [-use-sheldon-emission-spectrum USESHELDONEMISSIONSPECTRUM]
                           [-use-sheldon-fluorescence-times USESHELDONFLUORESCENCETIMES] [-SPMT {true,false}] [-LPMT {true,false}] [-TTS {true,false}] [-noise {true,false}]

optional arguments:
  -h, --help            show this help message and exit
  -name NAMERUN, --NameRun NAMERUN
                        Name of the run
  -s SPECIES, --Species SPECIES
                        Which solar neutrino species (Be7, pep, CNO, pp, hep, N13, O15) or background species (Bi-210, Kr-85, Po-210, K-40, U-238, Th-232, C-11, C-10, He-6) or mono-energetic particles (mono) or reactor anti-
                        neutrinos (antinu)
  -runs HOWMANY, --HowMany HOWMANY
                        How many rootfiles
  -events EVENTSPERRUN, --EventsPerRun EVENTSPERRUN
                        How many events per run
  -t THRESHOLD, --threshold THRESHOLD
                        NPMTs trigger threshold; default 300
  -generate-center GENERATECENTER, --GenerateCenter GENERATECENTER
                        To generate all the primary particles exactly in the center of the detector; default=false
  -volume-radius-min VOLUMERADIUSMIN, --VolumeRadiusMin VOLUMERADIUSMIN
                        min of the radius (only if GenerateCenter=false); default=0
  -volume-radius-max VOLUMERADIUSMAX, --VolumeRadiusMax VOLUMERADIUSMAX
                        max of the radius (only if GenerateCenter=false); default=17000mm
  -particle-energy PARTICLEENERGY, --ParticleEnergy PARTICLEENERGY
                        Particle Kinetic energy (only if Species=mono); default 1.0MeV
  -energy-mode ENERGYMODE, --EnergyMode ENERGYMODE
                        If you want to generate energy with smear (only if Species=mono), Possibilities: Range, Gaus, delta; default=delta
  -energy-extra-parameter ENERGYEXTRAPARAMETER, --EnergyExtraParameter ENERGYEXTRAPARAMETER
                        Only if EnergyMode is Range or Gaus. If EnergyMode=Range -> particles energy is uniformely distributed between [ParticleEnergy; EnergyExtraParameter]. If EnergyMode=Gaus -> particles energy is
                        gaussianly distributed with mu=ParticleEnergy and sigma=EnergyExtraParameter
  -particle-type PARTICLETYPE, --ParticleType PARTICLETYPE
                        Particle type (only if Species=mono); default e-
  -mass-ordering MASSORDERING, --MassOrdering MASSORDERING
                        Neutrino mass ordering for simulations (only if Species=antinu); Possibilities: normal or inverted; default: normal
  -elec2rec ELEC2REC, --elec2rec ELEC2REC
                        is elec2rec used?; default true
  -trigger-mode TRIGGERMODE, --TriggerMode TRIGGERMODE
                        Trigger Std or VFL; default Std
  -light-yield LIGHTYIELD, --LightYield LIGHTYIELD
                        LS light yield; default: 9846/MeV (see doc-db 8400)
  -cherenkov-yield CHERENKOVYIELDFACTOR, --CherenkovYieldFactor CHERENKOVYIELDFACTOR
                        Cherenkov yield factor; default: 0.517 (see doc-db 8400); set to zero to disable the Cherenkov effect
  -birks-constant1 BIRKSCONSTANT1, --BirksConstant1 BIRKSCONSTANT1
                        First Birks constant; default: 12.05e-3g/cm2/MeV (see doc-db 8400)
  -birks-constant2 BIRKSCONSTANT2, --BirksConstant2 BIRKSCONSTANT2
                        Second Birks constant; default: 0 (see doc-db 8400)
  -enable-quenching ENABLEQUENCHING, --EnableQuenching ENABLEQUENCHING
                        Activate/De-activate the quenching effect; default: true
  -enable-scattering ENABLESCATTERING, --EnableScattering ENABLESCATTERING
                        Activate/De-activate Rayleigh scattering; default: true
  -enable-absorption ENABLEABSORPTION, --EnableAbsorption ENABLEABSORPTION
                        Activate/De-activate the absorption; default: true
  -enable-reemission ENABLEREEMISSION, --EnableReEmission ENABLEREEMISSION
                        Activate/De-activate the re-emission; default: true
  -use-sheldon-emission-spectrum USESHELDONEMISSIONSPECTRUM, --UseSheldonEmissionSpectrum USESHELDONEMISSIONSPECTRUM
                        Use Sheldons emission spectrum or not; default: false
  -use-sheldon-fluorescence-times USESHELDONFLUORESCENCETIMES, --UseSheldonFluorescenceTimes USESHELDONFLUORESCENCETIMES
                        Use Sheldons fluorescence times or not; default: false
  -SPMT {true,false}, --ActivationSmallPMTs {true,false}
                        Enable the small PMTs; default: true
  -LPMT {true,false}, --ActivationLargePMTs {true,false}
                        Enable the large PMTs; default: true
  -TTS {true,false}, --TTSActivation {true,false}
                        Activate the Transit Time Spread of the PMTs; default: true
  -noise {true,false}, --NoiseActivation {true,false}
                        Activate the white noise of the PMTs; default: true
