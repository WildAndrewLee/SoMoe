var show_message = function(msg, color){
	color = color || '';

	var container = Moe('#message');
	var message = Moe.create('ul').append(
		Moe.create('li').text(msg)
	);

	if(container.success){
		container.attr('class', '')
			.addClass(color)
			.html(message);
	}
	else{
		Moe('#main').prepend(
			Moe.create('aside')
				.attr('id', 'message')
				.addClass('alert')
				.addClass(color)
				.append(message)
		);
	}
};