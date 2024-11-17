function initDropdown() {
	const button = document.getElementById('user-menu-button');
	const menu = document.getElementById('user-menu');

	button.addEventListener('click', e => {
		e.stopPropagation();
		menu.classList.toggle('hidden');
	});

	menu.addEventListener('click', e => {
		e.stopPropagation();
	});
}

document.addEventListener('click', e => {
	const menu = document.getElementById('user-menu');
	if (!menu.classList.contains('hidden')) {
		menu.classList.add('hidden');
	}
});

document.addEventListener('DOMContentLoaded', function () {
	initDropdown();

	document.body.addEventListener('htmx:afterSwap', e => {
		initDropdown();
	});
});

