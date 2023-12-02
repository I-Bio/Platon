function copyToClipboard() {
    let linkElement = document.getElementById("link");

    let tempInput = document.createElement("input");

    tempInput.value = linkElement.innerText;

    document.body.appendChild(tempInput);

    tempInput.select();

    document.execCommand("copy");

    document.body.removeChild(tempInput);

}
$("#dateTo").datetimepicker(
    {
        format: 'DD.MM.YYYY HH:mm',
        inline: false,
        locale: 'ru',
    }
);

document.getElementById("copybutton").addEventListener("click", function() {
    copyToClipboardd();
});

function copyToClipboardd() {
    let linkElement = document.getElementById("link");

    let tempInput = document.createElement("input");

    tempInput.value = linkElement.innerText;

    document.body.appendChild(tempInput);

    tempInput.select();

    document.execCommand("copy");

    document.body.removeChild(tempInput);

}


