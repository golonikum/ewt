EWT.namespace('ajax.listeners');

/* INTERFACE FUNCTIONS */

/**  
 * makes GET request to server
 */ 
EWT.ajax.get = function(href) {
	if (EWT.utils.getGlobal('Ctrl')) 
		EWT.tabs.createNewTab(href);
	else
		EWT.tabs.changeTabTitle(href); 
	EWT.ajax._doAjax(href, 'GET', null);
};

/**
 * removes an item with confirmation dialog
 */ 
EWT.ajax.remove = function(href) {
	buttons = {
		'Удалить': function() {
			$(this).dialog('close');
			EWT.ajax._doAjax(href, 'GET', null);
		},
		'Отмена': function() {
			$(this).dialog('close');
		}
	};
	EWT.utils.showAlert('Подтверждение', 'Вы действительно хотите удалить?', buttons, 300, 240);
};

/**
 * removes some items with confirmation dialog (TODO: refactoring)
 */ 
EWT.ajax.removeSome = function(href, is_update) {
	var num = $('input:checked', EWT.utils.getActiveTab()).length;
	if (num > 0) {
		var buttons = {};
		var p_name = is_update ? 'Изменить' : 'Удалить';
		buttons[p_name] = function(){
			$(this).dialog('close');
			EWT.ajax.post(href);
		};
	    buttons['Отмена'] = function(){
			$(this).dialog('close');
		};
		EWT.utils.showAlert('Подтверждение', "Вы действительно хотите " + p_name.toLowerCase() + " " + num + " " + EWT.utils.getNoun(num, 'элемент', 'элемента', 'элементов') + "?", buttons, 330, 240);
	} else {
		EWT.utils.showAlert('Ошибка', 'Вы не выбрали ни одного элемента.', null, 250, 140);
	}	
};

/**
 * makes POST request to server
 */ 
EWT.ajax.post = function(href) {
	EWT.ajax._doAjax(href, 'POST', $('form', EWT.utils.getActiveTab()).serializeArray());
};

/** 
 * creates new tab and do GET request
 */
EWT.ajax.newTab = function(href) {
	// add new tab
	EWT.tabs.createNewTab(href);

	// do ajax requests
	EWT.ajax._doAjax(href, 'GET', null);
};

/** 
 * writes word answer in exercises
 */
EWT.ajax.writeWordAnswer = function(href) {
	var content = ($('input[name=real]', EWT.utils.getActiveTab()).val() == $('input[name=test-sign]', EWT.utils.getActiveTab()).val()) ? 'Верно' : 'Неверно';
	EWT.utils.showAlert('Вы ответили', content, null, null, null, (content == 'Верно') ? 'color:green' : 'color:red');
	EWT.ajax.post(href);
};

/**
 * makes GET request to server for saving some value
 */ 
EWT.ajax.setValue = function(href, data) {
	EWT.ajax._doAjax(href, 'GET', data);
};

/**
 * makes GET request to server and insert the result into the certain element
 */ 
EWT.ajax.getInto = function(url, elem_id) {
	EWT.ajax._doAjax(url, 'GET', null, null, function(html){
		EWT.utils.showLoadingAnimation(false);
		$('#'+elem_id, EWT.utils.getActiveTab()).empty().append(html);
		EWT.ajax._afterAjaxLoad();
	});	
};


/* EVENTS HANDLERS */

/*
 * common success function
 */
EWT.ajax.listeners.success = function(html) {
	EWT.utils.showLoadingAnimation(false);
	// check if server returned error message
	if (String(html).indexOf('ajax-error') != -1) {
		return EWT.ajax.listeners.error(null, 'error', html);
	}
	var selected = EWT.utils.getGlobal('tabManager').tabs('option', 'selected');
	$("div[id^='tabs-']").eq(selected).empty().append(html);
	// do need actions after loading data
	EWT.ajax._afterAjaxLoad();
};

/*
 * common error function
 */
EWT.ajax.listeners.error = function(request, status, e) {
	EWT.utils.showLoadingAnimation(false);
	EWT.utils.showAlert('Ошибка', e, null, 250, 140);
};

/* 
 * success file uploading (TODO: this function is called from HTML)
 */ 
EWT.ajax.listeners.fileupload = function(file, response) {
	EWT.utils.showLoadingAnimation(false);
	EWT.utils.showAlert('Результат загрузки', response, null, 250, 140);
};


/* INTERNAL FUNCTIONS */

EWT.ajax._csrfToken = function() {
	if (window.EWT_CSRF_TOKEN && window.EWT_CSRF_TOKEN !== 'NOTPROVIDED') {
		return window.EWT_CSRF_TOKEN;
	}
	var fromForm = $('input[name=csrfmiddlewaretoken]').filter(function() {
		return $(this).val();
	}).val();
	if (fromForm) {
		return fromForm;
	}
	if ($.cookie) {
		return $.cookie('csrftoken');
	}
	return null;
};

/**
 * function for making AJAX request to server
 */ 
EWT.ajax._doAjax = function(p_url, p_type, p_data, p_error, p_success) {
	// define success and error functions
	error_func = p_error || EWT.ajax.listeners.error; 
	success_func = p_success || EWT.ajax.listeners.success; 
	
	// show loading animation
	EWT.utils.showLoadingAnimation(true);

	var method = (p_type || 'GET').toUpperCase();
	var csrf = EWT.ajax._csrfToken();
	if (method !== 'GET' && csrf) {
		if (!p_data) {
			p_data = {};
		}
		if ($.isArray(p_data)) {
			p_data = $.grep(p_data, function(item) {
				return item.name !== 'csrfmiddlewaretoken';
			});
			p_data.push({name: 'csrfmiddlewaretoken', value: csrf});
		} else if (typeof p_data === 'string') {
			if (p_data.indexOf('csrfmiddlewaretoken=') === -1) {
				p_data += (p_data ? '&' : '') + 'csrfmiddlewaretoken=' + encodeURIComponent(csrf);
			}
		} else {
			p_data.csrfmiddlewaretoken = csrf;
		}
	}
	
	// make request to server
	$.ajax({
		url: p_url,
		type: p_type,
		dataType: 'html',
		data: p_data,
		beforeSend: function(xhr) {
			if (method !== 'GET' && csrf) {
				xhr.setRequestHeader('X-CSRFToken', csrf);
			}
		},
		error: error_func,
		success: success_func
	});	
};

/** 
 * :TODO:
 */
EWT.ajax._afterAjaxLoad = function(){
	$(document).ready(function(){
		// prepare tooltips
		$('.ajax[title]').tooltip({
			track: true, 
		    delay: 2000, 
		    showURL: false
		});
		$('input.ajax-setter[title], .edit-img[title], .outer[title]').tooltip({
			track: true, 
		    delay: 500, 
		    showURL: false
		});
		// form 
		$('input[name=search-term], input[name=test-sign]', EWT.utils.getActiveTab()).keypress(function(event){
			if (event.keyCode == '13') {
				$('button', EWT.utils.getActiveTab()).trigger('click');
				return false;
		    }
		});
		$("#alert").dialog('close');
		$('input[name=test-sign]', EWT.utils.getActiveTab()).focus();
		$( EWT.utils.getActiveTab() ).perfectScrollbar( {suppressScrollX: true} );
	});
};

