/**
 *  Transcription plugin
 *
 *  Copyright (c) 2010 Nikita Golov (goloniko@gmail.com)
 *  Dual licensed under the MIT and GPL licenses:
 *  http://www.opensource.org/licenses/mit-license.php
 *  http://www.gnu.org/licenses/gpl.html
 *
 */

/**
 *  Create sliding keyboard with 3 symbols in element with 'key-board' ID 
 *  and bind it to INPUT element with 'transcription' ID. 
 *  Also here we add new CSS style to symbols 
 *  and bind them hover event handler.
 *
 *	$('#transcription').transcription({
 *		keyboard: $('#keyboard'), 
 *		symbols: ['1459','1034','1958']
 *	}).css({
 *		'color': 'red'
 *	}).hover(function(){
 *		$(this).css({
 *			'color': 'blue'
 *		});
 *	}, function(){
 *		$(this).css({
 *			'color': 'red'
 *		});
 *	});
 *
 */

(function($) {

	$.fn.transcription = function(settings) {
		// define vars
		var input = (this.length > 1) ? this.eq(0) : this;
		var keyboard = settings['keyboard'];		
		var slideTime = (typeof settings['slideTime'] != 'undefined') ? parseInt(settings['slideTime']) : 1000;
		var chars = settings['symbols'] || ['593','594','596','230','601','604','618','650','652','643','679','658','676','331','952','240','712','716','720'];
		
		// to prevent hiding keyboard when clicking on symbols
		jQuery.data(input.get(0), 'keyboardMouseOver', false);
		keyboard.live('mouseover', function() {
			jQuery.data(input.get(0), 'keyboardMouseOver', true);
		}).live('mouseout', function() { 
			jQuery.data(input.get(0), 'keyboardMouseOver', false);
		});

		// show/hide keyboard when focus/blur
		input.live('focus', function(){
			if ($('.symbol', keyboard.get(0)).length == 0) {				
				// make symbols
				keyboard.empty();
				keyboard.slideUp(0);
				for (var ch in chars) {
					keyboard.append("<div class='symbol'>&#" + chars[ch] + ";</div>");
				}
				var symbols = $('.symbol', keyboard.get(0));
				keyboard.append("<div style='clear:both'></div>");
				// attach an event click 
				symbols.click(function(){
					input.attr('value', input.attr('value') + $(this).html());
					input.focus();
				});
				// decorate symbols
				if ((typeof settings['decorate'] != 'undefined') ? settings['decorate'] : true) {
					symbols.css({
						'border': '1px solid #000',
						'width': '30px',
						'height': '30px',
						'text-align': 'center',
						'float': 'left',
						'font-family': '"lucida sans unicode"',
						'font-size': '20px',
						'line-height': '25px',
						'margin': '1px',
						'-moz-border-radius': '5px',
						'text-shadow': '0 1px 0 #fff'
					});
				}
				// animate symbols
				if ((typeof settings['hoverAnimate'] != 'undefined') ? settings['hoverAnimate'] : true) {
					symbols.hover(function(){
							$(this).css({
								'cursor': 'pointer',
								'-moz-box-shadow': '0px 0px 5px #000'
							});
							$(this).fadeTo(100, 1.0);
						}, function(){
							$(this).css({
								'cursor': 'inherit',
								'-moz-box-shadow': 'inherit'
							});
							$(this).fadeTo(100, 0.4);
					}).fadeTo(0, 0.4);	
				}			
			}
			keyboard.slideDown(slideTime);
		}).live('blur', function(){
			if (Boolean(jQuery.data(input.get(0), 'keyboardMouseOver'))) return;
			keyboard.slideUp(slideTime);
		});
				
		
		// return symbols for following chain processing
		return $('.symbol', keyboard.get(0));
	};

})(jQuery);
