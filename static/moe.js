/**
 * Moe is a lightweight subset of jQuery functions
 * that only cares about the bleeding-edge (so take
 * a hike IE).
 *
 * Moe is designed with the intention of working with
 * single DOM elements only.
 *
 * If you know how to use jQuery you basically already
 * know how to use Moe. The only difference is that
 * the Moe __success__ property is used to check for
 * matching selectors instead of jQuery.length.
 *
 * Also Moe.create is used to create new DOM elements.
 * Also also, Moe does returns a Moe object not a NodeList
 * like jQuery. kthnxbye.
 */

(function(window, undefined){
	var Moe = function(ele){
		if(this === window)
			return new Moe(ele);

		if(ele instanceof HTMLElement)
			this._ele = ele;
		else
			this._ele = document.querySelector(ele);
	};

	Object.defineProperty(Moe.prototype, 'success', {
		get: function(){
			return this._ele instanceof HTMLElement;
		}
	});

	Moe.extend = function(obj_a, obj_b){
		for(key in obj_b.prototype)
			obj_a.prototype[key] = obj_b.prototype[key];
	};

	Moe.create = function(ele){
		ele = document.createElement(ele);

		return Moe(ele);
	};

	Moe.prototype.prepend = function(ele){
		if(ele instanceof Moe)
			ele = ele._ele;

		var first = this._ele.firstChild;

		this._ele.insertBefore(ele, first);

		return this;
	};

	Moe.prototype.append = function(ele){
		if(ele instanceof Moe)
			ele = ele._ele;

		this._ele.appendChild(ele);

		return this;
	};

	Moe.prototype.text = function(text){
		if(text === undefined)
			return this._ele.textContent;

		this._ele.textContent = text;

		return this;
	};

	Moe.prototype.html = function(html){
		if(html === undefined)
			return this._ele.innerHTML;

		if(html instanceof Moe)
			this.html('').append(html);

		return this;
	};

	Moe.prototype.attr = function(attr, val){
		if(val === undefined)
			return this._ele.getAttribute(attr);
		else
			this._ele.setAttribute(attr, val);

		return this;
	};

	Moe.prototype.addClass = function(c){
		var classes = c.split(' ');

		for(var n = 0; n < classes.length; n++)
			this._ele.classList.add(classes[n]);

		return this;
	};

	Moe.prototype.removeClass = function(c){
		var classes = c.split(' ');
		
		for(var n = 0; n < classes.length; n++)
			this._ele.classList.remove(classes[n]);

		return this;
	};

	Moe.prototype.css = function(style, val){
		if(val === undefined){
			var s = window.getComputedStyle(this._ele)
			return s.getPropertyValue(style);
		}

		this._ele.style[style] = val;

		return this;
	};

	Moe.prototype.hide = function(){
		this.css('display', 'none');

		return this;
	};

	Moe.prototype.show = function(){
		this.css('display', 'block');

		return this;
	};

	Moe.prototype.hasParent = function(ele){
		if(ele instanceof Moe)
			ele = ele.ele();

		// We don't want this to be a parent of
		// itself.
		var child = this._ele.parentElement;

		while(child && child !== ele)
			child = child.parentElement;

		return child === ele;
	};

	Moe.prototype.ele = function(){
		return this._ele;
	}

	window.ↀωↀ = window.Moe = Moe;
})(window)