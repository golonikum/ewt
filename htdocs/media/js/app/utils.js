EWT.namespace('utils');

EWT.utils.getActiveTab = function() {
	return $('.ui-tabs-panel').not('.ui-tabs-hide').get(0);
};

EWT.utils.toggleItems = function(showId, hideId){
	$('#'+showId).css('display', 'inline');	
	$('#'+hideId).css('display', 'none');	
};

EWT.utils.getNoun = function (number, one, two, five) {
    number = Math.abs(number);
    number %= 100;
    if (number >= 5 && number <= 20) {
        return five;
    }
    number %= 10;
    if (number == 1) {
        return one;
    }
    if (number >= 2 && number <= 4) {
        return two;
    }
    return five;
};

EWT.utils.showAlert = function(title, content, buttons, width, height, style){
	title = title || 'Ошибка';
	content = content || '';
	buttons = buttons || {};
	$('#alert').remove();
	$("body").append("<div id='alert' title='" + title + "' style='" + style + "'>" + content + "</div>");
	$("#alert").dialog({
		modal: true,
		height: height || 140,
		width: width || 200,
		buttons: buttons
	});
};

EWT.utils.getHeight = function() {
	var y = 0;
    if (self.innerHeight)
    	y = self.innerHeight;
    else if (document.documentElement && document.documentElement.clientHeight)
		y = document.documentElement.clientHeight;
	else if (document.body)
		y = document.body.clientHeight;
	return y;
};

EWT.utils.invertCheckboxes = function(inverse) {
	$('input:checkbox', EWT.utils.getActiveTab()).each(function(){
		if (inverse && $(this).attr('checked')) {
			$(this).removeAttr('checked');
		} else {
			$(this).attr('checked', '1');
		}	
	});
	return true;
};

EWT.utils.normalizeTabHeight = function(tabSelector) {
	$(tabSelector).css('height', EWT.utils.getHeight() - $('.ui-tabs-nav').height() - 180 + 'px');
};

EWT.utils.getGlobal = function(name) {
	return jQuery.data(document.body, name);
};

EWT.utils.setGlobal = function(name, value) {
	jQuery.data(document.body, name, value);
};

/**
 * show/hide animated loading image
 */ 
EWT.utils.showLoadingAnimation = function(show) {
	if (show)
		$('#content').mask('Загрузка...');
	else
		$('#content').unmask();
};
