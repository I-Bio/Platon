window.onload = SetDateFormat;

function SetDateFormat(){
	$("#dateFrom").datetimepicker(
		{
			format: 'DD.MM.YYYY HH:mm',
			inline: false,
			locale: 'ru',
		}
	);

	$("#dateTo").datetimepicker(
		{
			format: 'DD.MM.YYYY HH:mm',
			inline: false,
			locale: 'ru',
		}
	);
}
