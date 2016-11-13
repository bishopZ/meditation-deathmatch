// ModelAgent v0.1
// Beta 4/9/14

define('model', ['typecast'], function(type){

	/** Modeler */
	function Model(schema){

		schema = type.obj.to(schema); // ensure that it is an object

		var typeSchema = _.reduce(schema, function(m, v, k) {
			if (type.def(type[v])) { m[k] = v; } // if v is a type, then use v
			else { m[k] = type(v); } // else get the type of v and use that
			return m;
		}, {});

		var valueSchema = _.reduce(schema, function(m, v, k) {
			if (type.def(type[v])) { m[k] = type[v].a(); } // if v is a type, then use type.a()
			else if (type(v) === 'object') { m[k] = $.extend(true, {}, v); }
			else if (type(v) === 'array') { m[k] = $.extend(true, [], v); }
			else { m[k] = v; } // else use v
			return m;
		}, {});

		// interface
		var model = function(obj) { // produces an object that follows the schema
			return $.extend(true, {}, valueSchema, obj); 
			// TODO: implement a backbone interface?
		}; 
		
		model.is = function(canidate) { // tests to see if model is valid
			return _.all(canidate, function(val, key){ return type(val) === typeSchema[key]; });
		};
		
		model.schema = function() { // gives produces an object with default values
			return typeSchema;
		}
		model.defaults = function() { // gives produces an object with default values
			return valueSchema;
		}
		
		return model;
	};


	window.Model = Model;
	return Model;
});

