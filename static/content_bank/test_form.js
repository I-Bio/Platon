var csrf = $("input[name=csrfmiddlewaretoken]").val();

var testQuest = new Splide( '#inTest', {
	direction: 'ttb',
	height   : '10rem',
	wheel    : true,
	perPage : 4,
	arrows : false,
} );
var bankQuest = new Splide( '#inBank', {
	direction: 'ttb',
	height   : '10rem',
	wheel    : true,
	perPage : 4,
	arrows : false,
} );

testQuest.mount();
bankQuest.mount();

$('button[name="addButton"]').click(
	function (){
		ListContentUpdater(this, 0);
	}
);

$('button[name="removeButton"]').click(
	function (){
		ListContentUpdater(this, 1);
	}
);

$("#searchField").keyup(SearchFunc);

function ListContentUpdater(myButton, type){
	let newItemId, containerId;
	let id = myButton.id;

	if (type == 1){
		newItemId = "AddQuestToTest";
		containerId = "BankList";
	}
	else {
		newItemId = "RemoveFromQuest";
		containerId = "TestList";
	}

	let newItem = document.getElementById(newItemId).content.cloneNode(true);
	let inputGroup = myButton.parentNode.parentNode;

	newItem.querySelector("button").id = id;
	if (newItem.querySelector("input")) newItem.querySelector("input").value = id;
	newItem.querySelector("p").textContent = inputGroup.querySelector("p").textContent;
	inputGroup.parentNode.remove();

	if (type == 1){
		newItem.querySelector("button").onclick = function (){
			ListContentUpdater(this, 0);
		};
	}
	else {
		newItem.querySelector("button").onclick = function (){
			ListContentUpdater(this, 1);
		};
	}

	document.getElementById(containerId).append(newItem);

	UpdateContentInLists();
}

function UpdateContentInLists(){
	testQuest.destroy();
	bankQuest.destroy();
	testQuest.mount();
	bankQuest.mount();
}
