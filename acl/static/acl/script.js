class RulesetEditor {
	constructor(dom_element) {
		this.dom = jQuery(dom_element)

		let config_json = this.dom.find('.config').text()
		this.config = JSON.parse(config_json)
		console.log(this.config);
		
		this.output_dom = this.dom.find('.base_widget textarea').first()
		this.config_area = this.dom.find('.config_area').first();
		this.widgets = this.dom.find('.widgets').first();

		this.init_value = JSON.parse(this.output_dom.val());
		this.value = [];

		this.init_widgets();

		this.make_fields(this.init_value);
		console.log(this.init_value);
	}

	init_widgets() {
		this.init_add_rule_widget();

		Object.keys(this.config).forEach((type) => {
			let config = this.config[type];

			let under_type = type.replace(/\./g, '_');
			let widget = jQuery('<span>').addClass(`form-${under_type}`);

			widget.append(`${config.description}: `);

			config.fields.forEach((field, idx) => {
				widget.append(`${field.name}:`);
				widget.append(this.get_input_for_field(field).data('name', field.name).val(field['default']));
				widget.append('; ');
			});

			this.widgets.append(widget);
		});
	}

	get_input_for_field(field) {
		switch(field.type) {
			case 'ChoiceField':
				let select = jQuery('<select>');
				field.custom.choices.forEach((choice) => jQuery('<option>').val(choice[0]).text(choice[1]).appendTo(select));
				return select;
			case 'CharField':
				return jQuery('<input>');
		}
	}

	init_add_rule_widget() {
		let widget = this.dom.find('.add_rule');

		let select = widget.find('select');
		Object.keys(this.config).forEach(key => {
			select.append(jQuery('<option>').val(key).text(this.config[key].description));
		});

		let button = widget.find('button');

		button.click((ev) => { ev.preventDefault(); this.add_new_rule(select.val());});
	}

	add_new_rule(type) {
		let rule_widget = this.get_widget('rule');

		let rule_desc = this.create_rule_desc_for_type(type);
		let rule_form = this.create_rule_form_for_type(type);

		rule_widget.find('.form').append(rule_form);
		
		rule_widget.appendTo(this.config_area);
		this.value.push(rule_desc);

		rule_widget.find('input,select').on('input', (ev) => {
			let target =  jQuery(ev.target);
			let name = target.data('name')
			let new_value = target.val()

			rule_desc[name] = new_value;

			this.update();
		});

		rule_widget.find('button').click((ev) => {
			ev.preventDefault();
			let button = jQuery(ev.target);

			let klass = button.attr('class');
			let rule = button.closest('.rule');
			let idx = rule.index();

			switch(klass) {
				case 'up': this.swap(rule.prev(), idx - 1); break;
				case 'down': this.swap(rule, idx); break;
				case 'del': this.erase(rule, idx); break;
			}
		});

		rule_widget.find('select.action').on('input', (ev) => {
			rule_widget.find('input.goto_label').toggle(ev.target.value == 'GOTO');
		});

		this.update();

		return rule_widget;
	}

	swap(obj, idx) {
		obj.before(obj.next());
		let tmp = this.value[idx];
		this.value[idx] = this.value[idx + 1];
		this.value[idx + 1] = tmp;

		this.update();
	}

	erase(obj, idx) {
		obj.remove();

		this.value.splice(idx, 1);

		this.update();
	}

	update_indices() {
		this.config_area.children().each((idx, elem) => {
			jQuery(elem).find('.id').text(idx + 1);
		});
	}

	update_buttons() {
		this.config_area.find('button').prop('disabled', false);

		this.config_area.find('button.up').first().prop('disabled', true);
		this.config_area.find('button.down').last().prop('disabled', true);
	}

	update() {
		this.update_indices();
		this.update_buttons();
		this.output_dom.val(JSON.stringify(this.value));
	}

	create_rule_form_for_type(type) {
		let under_type = type.replace(/\./g, '_');
		return this.get_widget(`form-${under_type}`);
	}

	create_rule_desc_for_type(type) {
		let result = {
			action: 'REJECT',
			goto_label: null,
			type: type
		}

		this.config[type].fields.forEach((field) => {
			result[field.name] = field['default'];
		});

		return result;
	}

	make_fields(value) {
		value.forEach((desc) => {
			this.make_field_from_desc(desc)
		});

		this.update();
	}
	
	make_field_from_desc(desc) {
		let widget = this.add_new_rule(desc.type);

		widget.find('input, select').each((_, elem_) => {
			let elem = jQuery(elem_);
			elem.val(desc[elem.data('name')]);
			elem.trigger('input');
		});

		if(desc['action'] == 'GOTO') {
			widget.find('.goto_label').show();
		};
	}

	get_widget(name) {
		return this.widgets.find(`.${name}`).clone(true);
	}
}

function initialize_acl() {
	jQuery('.acl_ruleset').each((idx, obj) => new RulesetEditor(obj));
}

document.addEventListener('DOMContentLoaded', initialize_acl);
