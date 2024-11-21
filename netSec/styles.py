def apply_styles(root):
    """
    Apply general styles to the Tkinter root window and widgets.
    """
    root.configure(bg="#f0f8ff")  # Set background color
    root.option_add("*Font", "Arial 10")  # Default font
    root.option_add("*Button.Background", "#007acc")  # Button background color
    root.option_add("*Button.Foreground", "white")  # Button text color
    root.option_add("*Label.Background", "#f0f8ff")  # Label background color
    root.option_add("*Label.Foreground", "#000")  # Label text color
    root.option_add("*Entry.Font", "Arial 10")  # Entry widget font
    root.option_add("*Button.Font", "Arial 10 bold")  # Button font
