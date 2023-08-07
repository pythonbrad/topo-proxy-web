document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Add a click event on each of them
  $navbarBurgers.forEach(el => {
    el.addEventListener('click', () => {

      // Get the target from the "data-target" attribute
      const target = el.dataset.target;
      const $target = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle('is-active');
      $target.classList.toggle('is-active');

    });
  });

	//
	var $queryInputButton = document.querySelector('#query-input-button'); 
	var $queryInputText = document.querySelector('#query-input-text');
	var $queryOutputText = document.querySelector('#query-output-text');
	var $queryOutput = document.querySelector('#query-output');

	$queryInputButton.addEventListener('click', () => {
		var action = $queryInputText.attributes.action.value;
		var url = $queryInputText.value.trim();

		if (url) {
			$queryInputButton.classList.add('is-loading');
			fetch(`${action}?url=${url}`).then((response) => response.json()).then((data) => {
				$queryOutput.hidden = false;
				$queryOutput.className = $queryOutput.className.replace(/is-\w*$/g, data.type);
				$queryOutputText.innerHTML = data.message.replaceAll(/(^|\n)(.*?):/g, '<br><b>$2:</b>');
				$queryInputButton.classList.remove('is-loading');
			});
		};
	});
});


