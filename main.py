from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MainApp(App):
    def build(self):
        self.icon = "calculator.png"
        self.operators = ["/", "*", "+", "-"]
        self.ended_on_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation = "vertical")
        self.solution = TextInput(
            background_color = "black", foreground_color = "white",
            multiline = False, halign = "right", font_size = 55, readonly = True
        )

        main_layout.add_widget(self.solution)
        # set up buttons and in their intended order
        buttons = [
            ["7", "8", "9", "del"],
            ["4", "5", "6", "/"],
            ["1", "2", "3", "*"],
            ["C", "0", ".", "+"],
            ["=", "-"]
        ]

        # loop through button rows and define each value as an actual button with function
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text = label, font_size=30, background_color="grey",
                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
                if label == "=":
                    button.size_hint = (3, 1)
                    button.bind(on_press = self.on_find_solution)
                elif label == "del":
                    button.bind(on_press = self.on_delete)

                else:
                    button.bind(on_press = self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        return main_layout

    # provides funtionality for when a button is pressed and how it should be added to the input box
    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = ""
        else:
            # check is last input was an operator so two can not be put back to back
            if current and (
                self.ended_on_operator and button_text in self.operators
            ):
                return None
            # check if first input is an operator 
            elif current == "" and button_text in self.operators:
                return None
            
            else:
                new_text = current + button_text
                self.solution.text = new_text
        
        self.last_button = button_text
        self.ended_on_operator = self.last_button in self.operators

    # when func is called the expression in self.solution is evaluated and replaced with result
    def on_find_solution(self, instance):
        text = self.solution.text
        if text:
            solution = str(eval(self.solution.text))
            self.solution.text = solution

    def on_delete(self, instance):
        text = self.solution.text
        if text:
            self.solution.text = self.solution.text[:-1]


if __name__ == "__main__":
    app = MainApp()
    app.run()