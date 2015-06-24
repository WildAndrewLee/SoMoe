(function(window, undefined){
	Firefly = function(){};

	Firefly.prototype._events = {};

	Firefly.prototype.on = function(evt, fn){
		this._events[evt] = this._events[evt] || [];
		this._events[evt].push(fn);
	};

	Firefly.prototype.off = function(evt, fn){
		if(!evt || evt in this._events === false)
			return;

		if(fn === undefined){
			delete this._events[evt];
			return;
		}

		var index = this._events[evt].indexOf(fn);
		this._events[evt].splice(index, 1);
	}

	Firefly.prototype.emit = function(evt){
		if(!evt || evt in this._events === false)
			return;

		for(var n = 0; n < this._events[evt].length; n++){
			var func = this._events[evt][n];
			var real_args = Array.prototype.slice.call(arguments, 1);

			func.apply(this, real_args);
		}
	};

	window.Firefly = Firefly;
})(window)