function hook_form_init() {
	let modelSelect = document.getElementById('id_model_type');
	let objectSelect = document.getElementById('id_object');
	let actionSelect = document.getElementById('id_action');
	
	function filterValues(select, value) {
		select.value = undefined;
		let value_set = false;
		Array.from(select.children).forEach((child) => {
			if(child.value.startsWith(value + ':')) { 
				child.hidden = false;
				if(!value_set)
					select.value = child.value;
				value_set = true;
			} else {
				child.hidden = true;
			}
		});

	}

	let onInput = () => {
		let value = modelSelect.value;

		filterValues(objectSelect, value);
		filterValues(actionSelect, value);

	};

	modelSelect.addEventListener('input', onInput);
	onInput();
}

document.addEventListener('DOMContentLoaded', hook_form_init);
