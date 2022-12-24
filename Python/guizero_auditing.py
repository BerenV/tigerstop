from guizero import App, Text, PushButton

def change_message():
    message.value = "You pressed the button!"

app = App(title="Hello world")

message = Text(app, text="Welcome to the Hello world app!")

button = PushButton(app, text="Press me", command=change_message)
button.bg = "red"

app.display()