// No need to use jQuery for something so trivial.
document.getElementsByTagName('input')[0].addEventListener('click', function(){
	this.select();
});