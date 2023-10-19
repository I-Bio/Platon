var csrf = $("input[name=csrfmiddlewaretoken]").val();

let removeButton = document.getElementById("RemoveButton");

$('button[name="delButton"]').click(TranslateDataToModal);

$('button[name="editButton"]').click(EditElement);

function TranslateDataToModal(event){
	let button = event.target;
	let text = button.parentNode.parentNode.querySelector(".name-text").textContent;
	let modalText = document.getElementById("textModal");

	modalText.textContent = `Вы точно хотите удалить вопрос ${text}?`

	removeButton.removeEventListener('click', DeleteElement);
	removeButton.setAttribute("data-name", button.id);
	removeButton.addEventListener('click', DeleteElement);
}

function DeleteElement(event){
	let removeButton = event.target;
	let id = removeButton.getAttribute("data-name");
	let node = document.getElementById(id).parentNode.parentNode.parentNode;

	$.ajax({
		url: '',
		type: "post",
		data: {
			'toDelete': id,
			csrfmiddlewaretoken: csrf,
		},
		success: function (response){
			node.remove();

			console.log("Удаление завершено");
		}
	});

}

function EditElement(event){
	let buttonId = event.target.parentNode.parentNode.querySelector(".bg-danger").id;

	$.ajax({
		url: '',
		type: "post",
		data: {
			'toEdit': buttonId,
			//csrfmiddlewaretoken: csrf,
		},
		success: function (response){
			console.log("Редактируем");
		}
	});
}
