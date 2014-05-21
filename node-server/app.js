/* Theater */


// So I guess this is where we would connect several node servers 
// via some LAN. 

// A single socket.io server can serve many clients (projectors), 
// but there must be a different node server for each headset.

// Maybe each headset looks for a game and combines it's information
// with the information coming from "Player B" 

// if both nodes follow the same game mechanics, then they should arrive
// at the same conclusion about who has won.


// Create the Webserver

global.PORT = 3000;

var express = require('express')
  , app = express()
  , webserver = app.listen(global.PORT)
  , io = require('socket.io').listen(webserver);

console.log('Listening on port %d', webserver.address().port);


// setup static file handling
app.use(express.json());
app.use(express.urlencoded());
app.use('/', express.static(__dirname + '/../client'));
    
// a more complicated example
// app.get('/elephant', function(req, res){
//   res.sendfile(__dirname + '/elephant.html');
// });


// Start the Neurosky Connection

var nodeThinkGear = require('./node-neurosky');
var running = false;
var connected = false;

var startGame = function(){
	running = true;
	console.log('start')
}
var stopGame = function(){
	running = false;
	console.log('stop')
}
var startConnector = function(){
	try {
		if (!connected) {
			var tgClient = nodeThinkGear.createClient({
				appName:'NodeThinkGear',
				appKey:'0fc4141b4b45c675cc8d3a765b8d71c5bde9390'
			});
			tgClient.connect();	
			// when think-gear sends data
			tgClient.on('data',function(data){
				// send it to the client browser
				if (running) { 
					// send it twice in an array
					// to simulate two player mode!!!!
					io.emit('mindEvent', [data, data]); 
				}
				//console.log(data);		
			});
		}
		console.log('device connected');
	} catch(e){
		console.log('device not connected');
	}

}
io.sockets.on('connection', function (socket) {
	startConnector();
	socket.on('game:start', startGame);
	socket.on('game:stop', stopGame);
});


