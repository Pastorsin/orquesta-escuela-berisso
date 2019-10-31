$(document).ready(() => {
	const section = Array.from($(".section"));

	const data = {
		'user_new' : {
			'name' : 'Crear usuario',
			'icon' : 'fa-user-plus',
			'url'  : 'usuarios/new'
		},
		'user_index' : {
			'name' : 'Listado de usuarios',
			'icon' : 'fa-users',
			'url'  : 'usuarios'
		},
		'webconfig_update' : {
			'name' : 'Configuración',
			'icon' : 'fa-cogs',
			'url'  : 'configuracion'
		}
	}

	section.forEach((item) => {
		const titleSelector = item.querySelector(".item-title")
		const iconSelector = item.querySelector(".item-icon")
		const urlSelector = item.querySelector(".item-url")


		let sectionItem = data[item.id]
		if (sectionItem) {
			titleSelector.textContent = sectionItem.name;
			iconSelector.classList.add(sectionItem.icon);
			urlSelector.setAttribute("href", sectionItem.url);
		} else {
			item.remove();
		}

	});
});