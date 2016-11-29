

#Meditation Deathmatch v0.4

[http://meditationdeathmat.ch/](http://meditationdeathmat.ch/)

For Meditation Deathmatch, two opponents face off to meditate. We use EEG to read their brain signals and determine who is staying in a meditative state better. Several other biometric factors are also monitored, and the information is visualized in a creative fashion on a projection screen. Various game rules may be used, but in one basic version, a health meter decreases when one opponent is not doing as well as the other.

Collaborators include: Matt Dorsey, Eric Carlin, Shanta Stevens, Joshua Jackson, and Bishop Zareh.

##Installation

Installation is not a smooth process.

You'll need the Muse Research Tools from http://developer.choosemuse.com/

See the Vagrantfile for info on other dependencies.

Pair your 2 Muse EEG headesets and edit the ?-run_muse_io.py files for your device IDs.

Run muse-io for both headsets and start the game server with standalone-server.py -- view the UI with Chrome.
