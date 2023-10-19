let submit = document.getElementById("submitButton");
submit.setAttribute("disabled", "");


$("#ID").keyup(
	function (){
		CheckForm();
	}
),

$("#typeQuest").change(
	function (){
		CheckForm();
	}
);


function CheckForm(){
	let sel = document.getElementById("typeQuest").value;
	let name = document.getElementById("ID").value;

	if (sel != "---" && name != ""){
		submit.removeAttribute("disabled");
	}
	else {
		submit.setAttribute("disabled", "");
	}
}