function hideMessages() {
    var messages = document.querySelectorAll('.alert');
    console.log(messages);

    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.display = 'none';
        }, 3300);
        console.log("Удаляем");
    });
}

window.onload = function () {
    console.log("Начали");
    hideMessages();

};