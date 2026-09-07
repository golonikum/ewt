EWT.namespace('tabs');

EWT.tabs.init = function() {
	EWT.utils.setGlobal('tabCounter', 2);
	EWT.utils.setGlobal('tabManager',
		$('#content').tabs({
			tabTemplate: '<li><a href="#{href}">#{label}</a> <span class="ui-icon ui-icon-close">Закрыть</span></li>',
			add: function(event, ui) {
				$(ui.panel).append('');
			}
		})
	);
	// close icon: removing the tab on click (TODO: closable tabs gonna be an option in the future)
	$('#content span.ui-icon-close').live('click', function() {
		var tabManager = EWT.utils.getGlobal('tabManager');
		var index = $('li',tabManager).index($(this).parent());
		tabManager.tabs('remove', index);
	});
};

EWT.tabs.addTab = function(title) {
	var tabManager = EWT.utils.getGlobal('tabManager');
	var tabCounter = EWT.utils.getGlobal('tabCounter');
	var tabSelector = '#tabs-'+tabCounter;
	tabManager.tabs('add', tabSelector, title);
	tabManager.tabs('select', tabSelector);
	EWT.utils.normalizeTabHeight(tabSelector);
	tabCounter++;
	EWT.utils.setGlobal('tabCounter', tabCounter);
};

EWT.tabs.closeAllTabs = function() {
	var tabManager = EWT.utils.getGlobal("tabManager");
	tabManager.tabs('select', '#tabs-1');
	$('li.ui-state-default:gt(0)').remove();
	$('div.ui-tabs-panel:gt(0)').remove();
	EWT.utils.setGlobal('tabCounter', 2);
};

EWT.tabs.closeTab = function() {
  $("#content li.ui-tabs-selected span.ui-icon-close").trigger("click");
};

EWT.tabs.changeTabTitle = function(url) {
	$('#content li.ui-tabs-selected a').html(EWT.tabs.getTabTitle(url));	
};

EWT.tabs.createNewTab = function(url) {
	EWT.tabs.addTab(EWT.tabs.getTabTitle(url));
};

EWT.tabs.getTabTitle = function(url) {
	var all_tabs = jQuery.data(document.body, 'menuDictionary');
	var new_tab = 'Новая';
	for (var item in all_tabs) {
		var patt = new RegExp(item);
		if (patt.test(url)) {
			new_tab = all_tabs[item];
			break;
		}
	}
	return new_tab;
};
