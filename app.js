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
app.use('/', express.static(__dirname + '/client'));
    
// a more complicated example
// app.get('/elephant', function(req, res){
//   res.sendfile(__dirname + '/elephant.html');
// });


// Start the Neurosky Connection

var nodeThinkGear = require('./server/node-neurosky');
var tgClient = nodeThinkGear.createClient({
	appName:'NodeThinkGear',
	appKey:'0fc4141b4b45c675cc8d3a765b8d71c5bde9390'
});
tgClient.connect();


// Create a WebSocket connection with a client browser
io.sockets.on('connection', function (socket) {

	// when think-gear sends data
	tgClient.on('data',function(data){
		
		// send it to the client browser
		socket.emit('mindEvent', data);
		//console.log(data);
		
	});
	// could do stuff like
	// socket.send('message')
	// socket.on('message', fn)
	// socket.on('disconnect', fn)

	// "connect" and "disconnect" events is how we keep track of different browsers

});