from django.contrib import messages


class MessageSuccess:
    def get_message_success(self, request, text="Сохранено"):
        messages.success(request, text)

