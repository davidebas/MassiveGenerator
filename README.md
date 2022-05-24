# MassiveGenerator
MassiveGenerator

Script for SNiPER submission jobs.
Generation of all the folder and files required:
- CondorScriptToLaunch script (.sh) to be launched to start the submission (source CondoScriptToLaunch_Something.sh)
- root, err, log, sh, sub folders
- .sub file (in /sub folder) handling the submission to CNAF nodes
- .sh file (in /sh folder) including the SNiPER instructions (based on detsim and elec2rec) 

usage: MassiveGenerator_SNiPER.py [-h] [-s SPECIES] [-runs HOWMANY]
                                  [-events EVENTSPERRUN] [-t THRESHOLD]
                                  [-volume-radius-min VOLUMERADIUSMIN]
                                  [-volume-radius-max VOLUMERADIUSMAX]
                                  [-particle-energy PARTICLEENERGY]
                                  [-particle-type PARTICLETYPE]
                                  [-elec2rec ELEC2REC]
                                  [-trigger-mode TRIGGERMODE]

optional arguments:
  -h, --help            show this help message and exit
  -s SPECIES, --Species SPECIES
                        Which neutrino species (Be7, pep, CNO, pp, hep, N13,
                        O15) or background species (Bi-210, Kr-85, Po-210,
                        K-40, U-238, Th-232, C-11, C-10, He-6) or mono-
                        energetic particles (mono)
  -runs HOWMANY, --HowMany HOWMANY
                        How many rootfiles
  -events EVENTSPERRUN, --EventsPerRun EVENTSPERRUN
                        How many events per run
  -t THRESHOLD, --threshold THRESHOLD
                        NPMTs trigger threshold; default 300
  -volume-radius-min VOLUMERADIUSMIN, --VolumeRadiusMin VOLUMERADIUSMIN
                        min of the radius
  -volume-radius-max VOLUMERADIUSMAX, --VolumeRadiusMax VOLUMERADIUSMAX
                        max of the radius
  -particle-energy PARTICLEENERGY, --ParticleEnergy PARTICLEENERGY
                        Particle Kinetic energy (only if Species=mono);
                        default 1.0
  -particle-type PARTICLETYPE, --ParticleType PARTICLETYPE
                        Particle type (only if Species=mono); default e-
  -elec2rec ELEC2REC, --elec2rec ELEC2REC
                        is elec2rec used?; default true
  -trigger-mode TRIGGERMODE, --TriggerMode TRIGGERMODE
                        Trigger Std or VFL; default Std
