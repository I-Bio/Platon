var csrf = $("input[name=csrfmiddlewaretoken]").val();

let RemoveButton = document.getElementById("RemoveButton");

$('button[name="delButton"]').click(TranslateDataToModal);

$("#searchField").keyup(SearchQuest);

function TranslateDataToModal(event){
	let button = event.target;
	let text = button.parentNode.parentNode.querySelector("p").textContent;
	let modalText = document.getElementById("modalText");

	modalText.textContent = `Вы точно хотите удалить вопрос ${text}?`

	RemoveButton.removeEventListener('click', DeleteQuestion);
	RemoveButton.setAttribute("data-name", button.id);
	RemoveButton.addEventListener('click', DeleteQuestion);
}

function DeleteQuestion(event){
	let removeButton = event.target;
	let id = removeButton.getAttribute("data-name");

	let node = document.getElementById(id).parentNode.parentNode.parentNode;

	$.ajax({
		url: '',
		type: 'post',
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

function SearchQuest() {
	let input, filter, li;

	input = document.getElementById("searchField");
	filter = input.value.toUpperCase();
	li = document.getElementById("BankList").getElementsByTagName("li");

	for (let i = 0; i < li.length; i++) {
		let p = li[i].querySelector("p");
		let text = p.textContent || p.innerText;

		if (text.toUpperCase().indexOf(filter) > -1) {
			li[i].style.display = "";
		}
		else {
			li[i].style.display = "none";
		}
	}
}