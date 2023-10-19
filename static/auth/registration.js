let submitButton = document.getElementById("submitButton");
let firstPassword = document.getElementById("firstPassword");
let lastPassword = document.getElementById("lastPassword");


submitButton.setAttribute("disabled","");

firstPassword.onkeyup = ValidatePassword;

lastPassword.onkeyup = ValidatePassword;

function ValidatePassword(event){
	if (firstPassword.value == lastPassword.value){
		submitButton.removeAttribute("disabled");
		lastPassword.classList.remove("is-invalid");
		lastPassword.classList.add("is-valid");
	}
	else {
		submitButton.setAttribute("disabled","");
		lastPassword.classList.remove("is-valid");
		lastPassword.classList.add("is-invalid");
	}
}