$(document).ready(function(){
	$('#dialog').dialog({
		draggable: false
		,resizable: false
		,width: 380
	});

	$('a.ui-dialog-titlebar-close').hide();

	$( "input[type=submit]" ).button();

	Cufon('#ui-dialog-title-dialog', {
		fontFamily: 'Practicum'
		,textShadow: '1px 1px #768B81'
		,color: '#768B81'
	});

	$('.ui-dialog').fadeTo(0, 0.9);	
});

