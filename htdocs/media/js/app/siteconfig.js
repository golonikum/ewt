EWT.namespace('siteconfig');

EWT.siteconfig.toggleDragAndResize = function() {
	var blocks = '#' + EWT.utils.getGlobal('blocks').join(', #');
	if (Boolean(EWT.utils.getGlobal('enableDragAndResize'))) {
		$(blocks)
			.draggable('destroy')
			.resizable('destroy');
		EWT.utils.setGlobal('enableDragAndResize', false);
		EWT.utils.toggleItems('enable-drag-btn', 'disable-drag-btn');
	} else {
		$(blocks)
			.draggable({cursor: 'crosshair', opacity: 0.35})
			.resizable({minWidth: 300, minHeight: 100})
			.fadeTo(0, 0.9);
		EWT.utils.setGlobal('enableDragAndResize', true);
		EWT.utils.toggleItems('disable-drag-btn', 'enable-drag-btn');
	}
};

EWT.siteconfig.saveBlocksPlacement = function() {
	var blocks = EWT.utils.getGlobal('blocks');
	for (var i in blocks) {
		var block_id = blocks[i];
		var block = $('#'+block_id);
		var cookieVal = block.css('left') + ';' + block.css('top');
		if (block.css('position') == 'absolute') {
			cookieVal += ';' + block.css('width') + ';' + block.css('height');
		}		
		$.cookie(block_id, cookieVal, {expires: 30});
	}
};

EWT.siteconfig.setBlocksPlacement = function() {
	var blocks = EWT.utils.getGlobal('blocks');
	for (var i in blocks) {
		var block = '#'+blocks[i];
		var dimArr = String($.cookie(blocks[i])).split(';');
		if (dimArr.length == 2) {
			$(block).css({'position': 'relative', 'left': dimArr[0], 'top': dimArr[1]});
		} else if (dimArr.length == 4) {
			$(block).css({'position': 'absolute', 'left': dimArr[0], 'top': dimArr[1], 'width': dimArr[2], 'height': dimArr[3]});
		}	
	}
};

EWT.siteconfig.restoreDefaultBlocksPlacement = function() {
	var blocks = EWT.utils.getGlobal('blocks');
	for (var i in blocks) {
		$('#'+blocks[i]).css({'position': 'relative', 'left': '', 'top': '', 'width': '', 'height': ''});
	}
    EWT.utils.normalizeTabHeight( '#content .ui-tabs-panel' );
};
