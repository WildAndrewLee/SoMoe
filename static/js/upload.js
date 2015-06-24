(function(window, undefined){
	if(window.FormData === undefined){
		Moe('#picker').show();
		return;
	}

	var upload = document.getElementById('upload');
	var picker = document.getElementById('picker');
	var progress = document.getElementById('progress');
	var bar = progress.getElementsByTagName('span')[0];

	var on_load = function(e){
		e = JSON.parse(e);

		Moe('body').removeClass('expanded');

		setTimeout(function(){
			Moe(bar).css('width', '0%');
		}, 300);

		if(e['mode'] === 'redirect')
			window.location = e['url'];
		else if(e['mode'] === 'message')
			show_message(e['message'], e['color']);
		else
			show_message('An unknown server error has occurred.', 'red');
	};

	var update_progress = function(e, file){
		if(file.percent){
			Moe(bar).css('width', file.percent + '%');
		}
	};

	var try_upload = function(file){
		var MAX_SIZE = MAX_PAYLOAD * 1024 * 1024;
		
		if(file.size > MAX_SIZE){
			show_message('You may only upload files up to ' + MAX_PAYLOAD + ' MB in size.', 'red');
			return;
		}

		file.on('load', on_load);
		file.on('progress', update_progress);

		Moe('body').addClass('expanded');

		setTimeout(function(){
			file.upload('upload', {
				'ajax': true
			});
		}, 300);
	};

	upload.addEventListener('click', function(e){
		e.preventDefault()
		document.getElementById('picker').click();
	});

	picker.addEventListener('change', function(e){
		if(!picker.files.length)
			return;

		// We only allow one file at the moment.
		var file = picker.files[0];
		
		try_upload(file);
	});

	var anchor_count = 0;

	document.body.addEventListener('dragenter', function(e){
		Moe('#anchor').addClass('hovered');
		
		if(e.target !== document.body)
			anchor_count++;
	});

	Moe('#anchor').ele().addEventListener('dragleave', function(e){
		anchor_count--;

		if(anchor_count === 0)
			Moe('#anchor').removeClass('hovered');
	});

	document.body.addEventListener('dragover', function(e){
		e.preventDefault();
	});

	document.body.addEventListener('drop', function(e){
		e.preventDefault();
		e.stopPropagation();

		Moe('#anchor').removeClass('hovered');

		// Only one file at the moment.
		var file = e.dataTransfer.files[0];

		try_upload(file);
	});
})(window)