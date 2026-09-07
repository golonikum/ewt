/*  
 * initial prepare
 */ 
$(document).ready(function() {
	// tabs
	EWT.tabs.init();
	
	// make default height and scroll bars for first tab
	EWT.utils.normalizeTabHeight('#tabs-1');
    $( EWT.utils.getActiveTab() ).perfectScrollbar( {suppressScrollX: true} );

	// get blocks' placement from cookies (TODO: domain & path)
	var blocks = new Array('logo', 'menu', 'content', 'footer');
	EWT.utils.setGlobal('blocks', blocks);
	EWT.siteconfig.setBlocksPlacement();

	// make blocks draggable & resizable
	EWT.utils.setGlobal('enableDragAndResize', true);
	EWT.siteconfig.toggleDragAndResize();
	
	// menu dictionary
	EWT.utils.setGlobal('menuDictionary', {
		'index': 'Главная', 
		'config': 'Настройки', 
		'export': 'Экспорт', 
		'\/word\/': 'Слова',
		'sentence': 'Выражения',
		'group': 'Тэги',
		'search': 'Поиск',
		'exercise': 'Упражнения'
	});

	// make decoration features
	initDecoration();

	// set global key press handlers
	initKeyEvents();
	
	// init the player
	EWT.player.init();
});

function initDecoration() {
	// make Cufon font
	initCufon();

	// prepare tooltip
	$('*[title]').tooltip({
		track: true, 
	    delay: 500, 
	    showURL: false
	});

	// define form button style
	$('.fieldWrapper .ui-button').live('mouseover', function(){
		$(this).addClass('ui-state-hover');
	}).live('mouseout', function(){
		$(this).removeClass('ui-state-hover');
	});

	// decoration for form input elements
	var focusin = function() {
		$(this).css({
			'background': '#fff',
			'border-color': '#222'
		});
	};
	var focusout = function() {
		$(this).css({
			'background': '#ece8d9',
			'border-color': '#CBC7BD'
		});
	};
	$('input').live('focusin', focusin).live('focusout', focusout);
	$('select').live('focusin', focusin).live('focusout', focusout);
	$('textarea').live('focusin', focusin).live('focusout', focusout);

	// fade down main blocks
	var blocks = '#' + EWT.utils.getGlobal('blocks').join(', #');
	$(blocks).fadeTo(0, 0.9);
}

function initCufon() {
	Cufon.replace('#logo h1', {
		fontFamily: 'UKIJ 3D', 
		textShadow: '1px 1px white',
		color: '-linear-gradient(#E3DDCE, #122817)'
	});
    Cufon('#menu a', {
        fontFamily: 'Practicum',
        textShadow: '1px 1px #162B16',
        color: '#8EA299',
        hover: {
            textShadow: '1px 1px #768B81',
            color: '#99AD8C'
        }
	});
	Cufon('#menu #username span', {
        fontFamily: 'Practicum',
        textShadow: '1px 1px #162B16',
        color: '#9697AD'
    });
}

function initKeyEvents() {
	EWT.utils.setGlobal('Ctrl', false);
	EWT.utils.setGlobal('Alt', false);

	document.onkeydown = function(e){
		if (e.keyCode == 17) EWT.utils.setGlobal('Ctrl', true);
		if (e.keyCode == 18) EWT.utils.setGlobal('Alt', true);
	};
	document.onkeyup = function(e){
		var alt = EWT.utils.getGlobal('Alt');
		if (e.keyCode == 65 && alt) EWT.tabs.closeAllTabs(); // alt + A
		if (e.keyCode == 87 && alt) EWT.tabs.closeTab(); // alt + W
		if (e.keyCode == 82 && alt) EWT.utils.normalizeTabHeight(EWT.utils.getActiveTab()); // alt + R
		if (e.keyCode == 17) EWT.utils.setGlobal('Ctrl', false);
		if (e.keyCode == 18) EWT.utils.setGlobal('Alt', false);
	};
	document.onkeypress = function(e){
		if (e.keyCode == 13) $('div.fieldWrapper button.onenter-go').click();
	};

	// define live event handler for ajax
	$('input.ajax-setter').live('keypress', function(event){
		if (event.keyCode == 13) {
			var href = $(this).attr('href');
			var val = $(this).val();
			var name = $(this).attr('name');
			EWT.ajax.setValue(href, name + '=' + val);
		}
	});
}
