function hideMessages() {
    var messages = document.querySelectorAll('.alert');

    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.display = 'none';
        }, 5000);
        console.log("Удаляем");
    });
}

window.onload = function () {
    hideMessages();
};