(function(Firefly, undefined){
	Moe.extend(File, Firefly);
	Moe.extend(FileList, Firefly);

	Object.defineProperty(File.prototype, 'percent', {
		get: function(){
			return this.hasOwnProperty('_percent') ? this._percent : null;
		}
	});

	File.prototype.upload = function(url, options, file_input_name){
		var xhr = this.xhr = this.xhr || new XMLHttpRequest();
		var data = new FormData();
		var that = this;

		if(file_input_name === undefined)
			data.append('upload', this);
		else
			data.append(file_input_name, this);

		if(options !== undefined){
			for(key in options){
				data.append(key, options[key]);
			}
		}

		xhr.upload.addEventListener('progress', function(e){
			that._percent = (e.loaded / e.total) * 100;
			that.emit('progress', e, that);
		});

		xhr.addEventListener('error', function(e){
			that.emit('error', e, that);
		});

		xhr.addEventListener('load', function(e){
			that.emit('load', e.srcElement.response, that);
		});

		xhr.open('POST', url);
		xhr.send(data);
	}

	Object.defineProperty(FileList.prototype, 'percent', {
		get: function(){
			if(this.length === 0)
				return null;

			var total = 0;

			for(var n = 0; n < this.length; n++){
				total += this[n].percent;
			}

			return total / this.length;
		}
	});

	FileList.prototype.upload = function(url, options){
		var that = this;

		for(var n = 0; n < this.length; n++){
			var file = this[n];

			file.on('load', function(e){
				that.emit('load', e, this);
			});

			file.on('progress', function(e){
				that.emit('progress', e, this);
			});

			this[n].upload(url, options);
		}
	};
})(Firefly)
