from os import listdir
from sys import exit
from Src.typingwindow import TypingWindow
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle


# Starts the typing test if it's not already running.
def start(event) -> None:

    # Gets necessary global variables.
    global Text_source, Display_time, Display_precision, Display_chars_per_minute, Display_words_per_minute, \
        Display_final_graph
    global typing_running
    global List_of_texts
    global Options
    global Prompt_no_text, Prompt_test_already_running, Prompt_tried_to_close_window
    global icon_path

    if (Text_source.get() in List_of_texts) and (not typing_running):
        # Sets the variable indicating whether the test is running to True.
        typing_running = True
        # Changes the protocol and bind for closing the window as to not cause unexpected behavior.
        Options.bind('<Escape>', close_not)
        Options.protocol('WM_DELETE_WINDOW', close_not)
        # Gets rid of all prompts.
        Prompt_no_text.grid_forget()
        Prompt_test_already_running.grid_forget()
        Prompt_tried_to_close_window.grid_forget()
        # Creates TypingWindow object.
        Typing_window = TypingWindow('Texts/' + Text_source.get() + '.txt', Display_time.get(), Display_precision.get(),
                                     Display_chars_per_minute.get(), Display_words_per_minute.get(),
                                     Display_final_graph.get(), icon_path=icon_path)
        # Starts the typing test.
        Typing_window.initiate_typing()
        # Deletes TypingWindow object.
        del Typing_window
        # Sets the variable indicating whether the test is running to False.
        typing_running = False
        # Gives focus back to the options window.
        Options.focus()
        # Reenable the option to close the window.
        Options.bind('<Escape>', close)
        Options.protocol('WM_DELETE_WINDOW', close)
    elif not typing_running:
        # Displays prompt if no text is selected.
        Prompt_no_text.grid(row=100, column=0, columnspan=2)
    else:
        # Displays prompt if the test is already running.
        Prompt_test_already_running.grid(row=101, column=0, columnspan=2)


# Terminates the program.
def close(event=None) -> None:

    exit()


# Close substitute gets called when test is already running as not to cause unexpected behavior.
def close_not(event=None) -> None:

    Prompt_tried_to_close_window.grid(row=102, column=0, columnspan=2)


if __name__ == '__main__':

    # Defines the list of texts that the user can chose from.
    List_of_texts = []
    # Defines the variable that indicates whether the typing test is currently running.
    typing_running = False

    # Defines the path to the icon used by the windows.
    icon_path = 'Icon/icon_test-Window.ico'

    # Gets all .txt files from the Texts folder and adds them to the list (stripping the extension for user experience).
    for file in listdir('Texts'):
        if file.endswith('.txt'):
            List_of_texts.append(file.strip('.txt'))

    # Defines the window and its attributes.
    Options = Tk()
    Options.title('Typing Speed Test Options')
    Options.minsize(450, 250)
    Options.maxsize(450, 250)
    Style = ThemedStyle(Options)
    Options.iconbitmap(icon_path)
    Style.set_theme('radiance')

    # Defines the frame that will contain the options and pack it inside the window.
    Main_frame = ttk.LabelFrame(Options, text='Options')
    Main_frame.pack(padx=10, pady=10)

    # Defines the tkinter variables storing the chosen options.
    Text_source = StringVar(Main_frame)
    Display_time = BooleanVar(Main_frame, value=TRUE)
    Display_precision = BooleanVar(Main_frame, value=TRUE)
    Display_chars_per_minute = BooleanVar(Main_frame, value=TRUE)
    Display_words_per_minute = BooleanVar(Main_frame, value=TRUE)
    Display_final_graph = BooleanVar(Main_frame, value=TRUE)

    # Defines the checkbuttons and dropdown list that can be used by user to customize the test.
    Show_Time = ttk.Checkbutton(Main_frame, text='Show Time', variable=Display_time)
    Show_precision = ttk.Checkbutton(Main_frame, text='Show Precision', variable=Display_precision)
    Show_chars_per_minute = ttk.Checkbutton(Main_frame, text='Show Characters Per Minute',
                                            variable=Display_chars_per_minute)
    Show_words_per_minute = ttk.Checkbutton(Main_frame, text='Show Words Per Minute', variable=Display_words_per_minute)
    Show_final_graph = ttk.Checkbutton(Main_frame, text='Show Final Graph', variable=Display_final_graph)
    Dropdown_text = ttk.OptionMenu(Main_frame, Text_source, *List_of_texts)

    # Defines the prompts for different situations.
    Prompt_no_text = ttk.Label(Main_frame, text='No text chosen')
    Prompt_test_already_running = ttk.Label(Main_frame, text='Test is already running')
    Prompt_tried_to_close_window = ttk.Label(Main_frame, text="Can't close options while test is running")

    # Puts all the option widgets inside the Main_frame.
    Show_Time.grid(row=0, column=0, sticky=W)
    Show_precision.grid(row=0, column=1, sticky=W)
    Show_chars_per_minute.grid(row=1, column=0, sticky=W)
    Show_words_per_minute.grid(row=1, column=1, sticky=W)
    Show_final_graph.grid(row=2, column=0, columnspan=2)
    Dropdown_text.grid(row=99, column=0, columnspan=2, padx=20, pady=5)

    # Binds escape to terminate the application and enter to start the test.
    Options.bind('<Escape>', close)
    Options.bind('<Return>', start)

    # Makes sure ending the process is handled correctly when the user closes the window by another means.
    Options.protocol('WM_DELETE_WINDOW', close)

    # Gives focus to the program.
    Options.focus()
    
    # Blocks exucution of program.
    Options.mainloop()
