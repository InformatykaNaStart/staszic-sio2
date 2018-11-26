function cisza() {
let ls=window.sessionStorage;

let currDate = (new Date).getTime();
let lastDate = ls.getItem('lastDate');
let HOUR = 1000 * 60 * 60;

if(!lastDate || lastDate + HOUR < currDate) {
	let banner = $('<div>');
	banner.css('height', '100vh');
	banner.css('widht', '100%');
	banner.css('z-index', Math.floor(70000+Math.random()*30000));
	banner.css('position', 'fixed');
	banner.css('top', 0);
	banner.css('left', 0);
	banner.css('background-color', 'black');
	banner.css('display', 'flex');
	banner.css('justify-content', 'center');
	banner.css('align-items', 'center');
	banner.css('text-align', 'center');
	banner.css('color', 'white');
	banner.css('font-size', '72px');
	banner.css('font-family', 'sans-serif');

	let pre = Math.random() * 100;
	for(let i=0; i < pre; i++) jQuery('<div>').appendTo(jQuery('body'));
	banner.appendTo(jQuery('body'));
	let post = Math.random() * 100;
	for(let i=0; i < post; i++) jQuery('<div>').appendTo(jQuery('body'));

	let text = $('<div>');
	text.html('<span>Ważne ogłoszenie!</span><br>Cisza nocna polega na tym, że jest się cicho i się siedzi w pokoju.<br><span>To ogłoszenie zniknie za 10 sekund.</span>');

	text.appendTo(banner);

	banner.find('span').first().css('font-size', '108px');
	banner.find('span').last().css('font-size', '32px');

	setTimeout(()=>{
		banner.fadeOut(1000); 
		ls.setItem('lastDate', currDate);
	}, 9000);
}

}

// in case of emergency
// uncomment
//jQuery(document).on('DOMContentLoaded', cisza);
