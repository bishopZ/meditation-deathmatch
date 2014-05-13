/*
node-neurosky
Copyright 2012 Daniel Luxemburg
All rights reserved.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
*/

var net = require('net'),
	events = require('events'),
	util = require('util');

function NodeThinkGearError(message){
  Error.call(this);
  Error.captureStackTrace(this, arguments.callee);
  this.message = message;
  this.name = 'NodeThinkGearError';
};

NodeThinkGearError.prototype.__proto__ = Error.prototype;

var ThinkGearClient = function(opts){
	opts || (opts = {});

	this.port = opts.port || 13854;
	this.host = opts.host || 'localhost';

	if(typeof(opts.appName) !== 'string') throw new NodeThinkGearError('Must specify appName');
	if(typeof(opts.appKey) !== 'string') throw new NodeThinkGearError('Must specify appKey');
	
	this.auth = {
		appName:opts.appName,
		appKey:opts.appKey
	};

	this.config = {
		enableRawOutput: false,
		format: "Json"
	};

	events.EventEmitter.call(this);
};

util.inherits(ThinkGearClient, events.EventEmitter);

ThinkGearClient.prototype.connect = function(){
	var self = this;
	
	var client = this.client = net.connect(this.port,this.host,function(){
		client.write(JSON.stringify(self.auth));
	});

	client.on('data',function(data){
		if(!self.configSent){
			self.configSent = true;
			client.write(JSON.stringify(self.config));
		} else {
			try{
				self.emit('data',JSON.parse(data.toString()));
			}catch(e){
				self.emit('parse_error',data.toString());
			}
		}
	});

    client.on('error', function(err) {
        console.log('Error connecting to ThinkGear client. Try starting the ThinkGear Connector app.\n', err);
        //process.exit(1);
    });
};

exports.ThinkGearClient = ThinkGearClient;

exports.createClient = function(opts){
	return new ThinkGearClient(opts || {});
};