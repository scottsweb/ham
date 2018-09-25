// dependencies
const pixel = require( "node-pixel" );
const five = require( "johnny-five" );
const color = require( "color");
const temporal = require( "temporal" );
const WebSocket = require('ws');

// vars
const board = new five.Board({
	port: "/dev/ttyACM0"
});
// mycroft uses websockets
// https://mycroft.ai/documentation/message-bus/#generating-messages-within-a-mycroftskill
const ws = new WebSocket('ws://localhost:8181/core');
let strip = null;
let timer = null;

board.on( "ready", function() {

	// setup board
	strip = new pixel.Strip( {
		board: this,
		controller: "FIRMATA",
		strips: [ { pin: 10, length: 16 } ],
		gamma: 2.8,
	} );

	strip.on( "ready", function() {
		ws.on( "message", function incoming( data ) {
			const result = JSON.parse( data );
			console.log( data );
			switch ( result.type ) {
				case 'recognizer_loop:record_begin':
					kill();
					pulse();
					break;
				case 'enclosure.mouth.viseme':
					kill();
					set( '#096033', result.data.code );
					break;
				case 'mycroft.skill.handler.start':
				case 'add_context':
					kill();
					dance();
					break;
				case 'enclosure.notify.no_internet':
				case 'mycroft.speech.recognition.unknown':
				case 'msm.install.failed':
					kill();
					pulse( '#ad0505');
					break;
				case 'msm.updating':
				case 'msm.installing':
					kill();
					spin();
					break;
				case 'recognizer_loop:audio_output_end':
				case 'enclosure.mouth.events.deactivate':
				case 'skill.converse.response':
				case 'mycroft.skill.handler.complete':
				case 'msm.updated':
				case 'msm.installed':
					kill();
					break;
				//case 'recognizer_loop:audio_output_start':
				//	spin();
				//	break;
				// configuration.updated - show this has happend
				default:
			}
		});
	});
});

board.on( "exit", function() {
	kill();
});

function kill() {
	clearInterval( timer );
	strip.off();
}

function set( colour = '#096033', level ) {
	let col = color( colour );
	let darken = 0.5;
	darken = darken - (level / 10 );
	for ( led = 0; led < strip.length; led++ ) {
		strip.pixel( led ).color( col.darken( darken ).hex() );
	}
	
	strip.show();
}

function flash( colour = '#096033' ) {
	let col = color( colour );
	let onOff = 'off'

	setInterval( function () {
		for ( led = 0; led < strip.length; led++ ) {
			strip.pixel( led ).color( col.hex() );
		}
		
		strip.show();
		
		if ( onOff === 'off' ) {
			col = color( '#000' );
			onOff = 'on';
		} else {
			col = color( colour );
			onOff = 'off';
		}
	}, 1000 / 6 );
	
}

function pulse( colour = '#096033' ) {
	let col = color( colour );
	let darken = 0;
	let direction = 'out';

	timer = setInterval( function () {
		for ( led = 0; led < 16; led++ ) {
			strip.pixel( led ).color( col.darken( darken ).hex() );
		}
		
		strip.show();
		
		if ( direction === 'out' ) {
			darken = darken + 0.1;
			if ( darken >= 0.7 ) {
				direction = 'in';
				darken = 0.7;
			}
		}
		
		if ( direction === 'in' ) {
			darken = darken - 0.1;
			if ( darken <= 0 ) {
				direction = 'out';
				darken = 0;
			}
		}
	}, 1000 / 20 );
}

function spin( colour = '#096033' ) {
	let col = color( colour );
	
	strip.pixel( 8 ).color( col.hex() );
	strip.pixel( 7 ).color( col.darken( 0.2 ).hex() );
	strip.pixel( 6 ).color( col.darken( 0.3 ).hex() );
	strip.pixel( 5 ).color( col.darken( 0.4 ).hex() );
	strip.pixel( 4 ).color( col.darken( 0.5 ).hex() );
	strip.pixel( 3 ).color( col.darken( 0.6 ).hex() );
	strip.pixel( 2 ).color( col.darken( 0.7 ).hex() );
	strip.pixel( 1 ).color( col.darken( 0.8 ).hex() );
	strip.pixel( 0 ).color( col.darken( 0.9 ).hex() );

	timer = setInterval(function () {
		strip.shift(1, pixel.FORWARD, true);
		strip.show();
	}, 1000 / 24 );
}

function dance( colour = '#096033' ) {
	let col = color( colour );
	
	strip.pixel( 0 ).color( col.hex() );
	strip.pixel( 1 ).color( col.hex() );
	strip.pixel( 8 ).color( col.hex() );
	strip.pixel( 9 ).color( col.hex() );

	strip.show();

	timer = setInterval(function () {
		strip.shift( 12, pixel.FORWARD, true );
		strip.show();
	}, 1000 / 6 );
}

function rainbow() {
	let showColor;
	let cwi = 0;
	setInterval(function(){
		 if( ++cwi > 255 ) {
			 cwi = 0;
		 }

		 for( led = 0; led < strip.length; led++ ) {
			showColor = colorWheel( ( cwi+led ) & 255 );
			strip.pixel( led ).color( showColor );
		 }
		 strip.show();
	 }, 1000 / 24 );
 }

function colorWheel( WheelPos ){
	let r,g,b;
	WheelPos = 255 - WheelPos;

	if ( WheelPos < 85 ) {
		r = 255 - WheelPos * 3;
		g = 0;
		b = WheelPos * 3;
	} else if ( WheelPos < 170 ) {
		WheelPos -= 85;
		r = 0;
		g = WheelPos * 3;
		b = 255 - WheelPos * 3;
	} else {
		WheelPos -= 170;
		r = WheelPos * 3;
		g = 255 - WheelPos * 3;
		b = 0;
	}
	// returns a string with the rgb value to be used as the parameter
	return "rgb(" + r +"," + g + "," + b + ")";
}
