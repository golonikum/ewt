EWT.namespace('player');

EWT.player.init = function() {
	$('#player')
		.jPlayer({
			ready: EWT.player.getRandomTrack,
			swfPath: '/media/flash'
		})
		.jPlayer('onSoundComplete', EWT.player.playNext)
		.jPlayer('cssId', 'play', 'play-btn')
		.jPlayer('cssId', 'pause', 'pause-btn');
};

EWT.player.playNext = function() {
	EWT.player.getRandomTrack();
	$("#player").jPlayer("play");	
};

EWT.player.getRandomTrack = function() {
	var random_num = Math.floor(Math.random()*5) + 1;
	var mp3_name = (random_num < 10) ? '0'+random_num : random_num;
	$("#player").jPlayer('setFile', '/media/mp3/' + mp3_name + '.mp3');
};
