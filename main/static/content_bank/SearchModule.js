$("#searchField").keyup(SearchFunc);

function SearchFunc() {
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