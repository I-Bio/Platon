let filename = $("#filename")[0];
let textId = $("#name")[0];

$("#file").change(
	function (){
		filename.value = this.files.length ? this.files[0].name : '';
	}
);