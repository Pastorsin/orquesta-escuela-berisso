function samePasswords() {
	let password = $("#password-input").val();
	let confirm = $("#confirm-password-input").val();
	return password == confirm
}

function notEmptyRoles() {
	return $(".rol-checkbox").is(":checked")
}

function validatePassword() {
	let message;

	if (samePasswords()) {
		message = ''
	}
	else {
		message = 'Las contraseñas no coinciden'
	}
	$("#confirm-password-error").text(message)
}

function validateRoles() {
	let message; 

	if (notEmptyRoles()) {
		message = ''
	} else {
		message = 'Se debe asignar al menos un rol'
	}
	$("#roles-error").text(message)
}

function renderErrors() {
	validatePassword();
	validateRoles();
}

$(document).ready(() => {

	$("#confirm-password-input").keyup(validatePassword)
	$("#password-input").keyup(validatePassword)


	$("form").submit(() => (samePasswords() && notEmptyRoles()));
	$("#save-button").click(renderErrors);
});