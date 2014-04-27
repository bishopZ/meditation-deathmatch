

#Node ThinkGear Visualizer v0.1

##Installation

First, you'll need one of [these](http://store.neurosky.com/products/mindwave-1):

![Fashion!](http://upload.wikimedia.org/wikipedia/en/f/f4/NeuroSky_MindWaveDiagram_Low.jpg)

Then install Node.js and install some packages (these may already be installed when you download this repo. not sure.)
```
$ npm install express
$ npm install socket.io@1
$ npm install node-thinkgear
```

then start the app by running
```
$ node app.js
```

You should see a message that says, "listening on port 3000." Then open a web browser and point it to http://localhost:3000. In most browsers, you do have to include the "http" part.



###node-thinkgear docs

Client library for the [ThinkGear Socket Protocol](http://developer.neurosky.com/docs/lib/exe/fetch.php?media=app_notes:thinkgear_socket_protocol.pdf) from [NeuroSky](http://neurosky.com/). 


###Data Model

The output objects look like this:

```javascript
{ 
	eSense: { 
		attention: 53, 
		meditation: 47 
	},
	eegPower: { 
		delta: 416474,
		theta: 33592,
		lowAlpha: 3877,
		highAlpha: 3142,
		lowBeta: 1569,
		highBeta: 3125,
		lowGamma: 3521,
		highGamma: 1451 
	},
	poorSignalLevel: 0,
	blinkStrength: 55
}
```
