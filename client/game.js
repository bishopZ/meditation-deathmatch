require(
	['typecast', 'frame', 'model', 'socket.io', 'lscache', 'moment',
	    'css!/base/bootstrap/bootstrap.min.css',
        'css!stylist/style.css',
        //    /bootstrap/bootstrap-responsive.min.css
		//    /stylist/layout.css
		//    /stylist/forms.css
		//    /bootstrap/font-awesome.min.css
	], 
	function(type, Frame, Model, io, lscache, moment) {

	// Create a data model for the data coming in
	var MindEvent = Model({ 
		eSense: { 
			attention: 0, 
			meditation: 0 
		},
		eegPower: { 
			delta: 0,
			theta: 0,
			lowAlpha: 0,
			highAlpha: 0,
			lowBeta: 0,
			highBeta: 0,
			lowGamma: 0,
			highGamma: 0 
		},
		poorSignalLevel: 0,
		blinkStrength: 0 
	});

	var Profile = Model({
		id: 123,
		name: '',
		color: '',
		quest: '',
		history: [],
		date: 'date'
	});

	// Basic Application
	// socket working!
	var socket = io.connect();

	socket.on('connect', function (data) {
		console.log("web socket connected");
	});

	var app = Frame('MeditationDeathmatch').start();

	// Display a card on screen
	$('body').append('<div id="screen"></div>');
	
	var $screen = $('#screen');

	$screen
		.css({
			height: $(window).height() -100,
			width: $(window).width() -50,
			border: '3px solid black',
			'border-radius': 15,
			background: '#eee',
			padding: '20px 30px',
			margin: 'auto',
			'margin-top': 50
		})
		.html('<div class="display full scroll"></div>');


	// setup the game modes
	// TODO: make these into modules

	var titleScreen = function(){
		// Meditation Death Match
		// Upgrade Studios
	}

	var deviceSetup = function(){
		// wait till device has 10 good signals in under 20 seconds
	}

	var modeSelect = function(){
		// Single or Multiplayer
		// Display Mode
	}

	var singlePlayerMode = function(){}
	var multiPlayerMode = function(){
		// Player 1 Connected
		// Player 2 Connected
		// Start Countdown?
	}
	var displayMode = function(){}

	var newPlayer = function(){
		var sessionId = Math.floor(Math.random() * 1000); 
		var profile = Profile({
			id: sessionId
		});
		
		// Intro Tunnel
	    app(function(done){
	    	var name = prompt('What is your name?', cached.name);
	    	profile.name = name;
			done();
		});

		app(function(done){
	    	var color = prompt('What is favorite color?', cached.color);
	    	profile.color = color;
			done();
		});

		app(function(done){
	    	var quest = prompt('What is your quest?', cached.quest);
	    	profile.quest = quest;

	    	// save to local storage
			lscache.set('medath', profile);
			playAgain();

			done();
		});
	}


	var getReady = function(){}

	var deathmatch = function(){}
	var deathmatchDisplay = function(){}
	
	var scorecard = function(){}
	var scorecardMulti = function(){}
	
	var highScores = function(){}


	var playAgain = function(){
		
		// Game variables
		var meditationLevel = 0;
		var attentionLevel = 0;
		var spaceyLevel = 0;
		var droppedFrames = 0;

		// Start Game Loop
		var startGameLoop = function(){

			// reset the history
			profile.history = [];

			socket.on('mindEvent', function (data) {
				
				// validate the data object
				//console.log(data);
				data = MindEvent(data);

				// Put the data into an array
				profile.history.push(data);
			
				// TODO: save that array to local storage
				// should we save dropped frames?
				//lscache.set('medath', profile);

				// start the game
				updateDisplay();

			});
		}

		var prevMedScore = 0;
		var prevAttScore = 0;

		// Game Loop
		var updateDisplay = function(){

			// add a function to the framed application
			// safe multi-threaded & animation safe
			// prevents client from becoming overwhelmed
			app(function(done){ 

				var data = _.last(profile.history) || MindEvent();
				var output = [];
				var $display = $screen.find('.full');
				
				// TODO: Start Timer
					// display a clock

				// update the display
				$screen.css({
					height: $(window).height() - 100,
					width: $(window).width() - 50
				});

				// Buffs
				if (data.blinkStrength > 50) {

					$display.append('<p>Blink!</p>');
					droppedFrames++;
				
				} else if (data.poorSignalLevel === 200 || data.eSense.attention === 0) {

					$display.append('<p>No Signal from Headset</p>');
					droppedFrames++;
				
				} else {
					
					// Bumps
					if (data.eSense.attention < 20 && data.eSense.meditation < 20) {
						spaceyLevel += 12;
					}
					else if (data.eSense.attention < 20 || data.eSense.meditation < 20) {
						spaceyLevel += 1;
					}

					if (data.eSense.attention > 90) {
						attentionLevel += 12;
					}
					else if (data.eSense.attention > 80) {
						attentionLevel += 1;
					}
					
					if (data.eSense.meditation > 90) {
						meditationLevel += 12;
					}
					else if (data.eSense.meditation > 80) {
						meditationLevel += 1;
					}
					
					var signalToNoise = Math.floor(((profile.history.length - droppedFrames) / profile.history.length) *100)

					// Stats
					output.push('Name: '+ profile.name + ' ... Color: '+ profile.color + ' ... Quest: '+ profile.quest);
					output.push('<hr />');
					output.push('Signal to Noise: ' + signalToNoise + "%");
					output.push('Attention Now: ' + data.eSense.attention + '<div class="score attention"><div class="inner"></div></div>');						
					output.push('Meditation Now: ' + data.eSense.meditation + '<div class="score meditation"><div class="inner"></div></div>');
					output.push('<hr />');
					output.push('Attention Score: ' + attentionLevel);
					output.push('Meditation Score: ' + meditationLevel);
					output.push('Spacey Score: ' + spaceyLevel);
					output.push('<hr />');

					// output main display to the browser
					if (_.compact(output).length > 0) {
						output = _.map(output, function(value){
							return '<p>'+ value +'</p>'
						});
						$display.html(output.join(''));
					}
				
					// show the raw eeg data
					$display.append(JSON.stringify(data.eegPower));
			
					$display.find('.score.attention .inner').css({'width': (prevAttScore) + "%"});
					$display.find('.score.meditation .inner').css({'width': (prevMedScore) + "%"});


					$display.find('.score.attention .inner').animate({'width': (data.eSense.attention) + "%"}, 900);
					$display.find('.score.meditation .inner').animate({'width': (data.eSense.meditation) + "%"}, 900);

					prevMedScore = data.eSense.meditation;
					prevAttScore = data.eSense.attention;

				}	
				
				// TODO: if Timer = 3 min
					// endGameLoop()

				done();
			});
		}
		
		// Make the Game loop work
		$(window).on('resize', _.throttle(updateDisplay, 33));
	
		startGameLoop();

		// End Game Loop
		var endGameLoop = function(){

			// TODO: Display restart Message

			// TODO: Save game with persons name in local storage

			// TODO: display high scores from local storage

			// TODO: turn off $window.resize

		}

	}

	// Create a user profile
	var cached = lscache.get('medath');
	console.log(cached);
	if (type.def(cached)) {

		var profile = Profile(cached); // enforce the data model

		// if not a new player
		if (cached.name !== ''
			&& cached.color !== ''
			&& cached.quest !== ''
			){
			// TODO: show play again button
			playAgain();
		} else {
			// TODO: display new player button
			newPlayer();
		}
	}
		
		
});