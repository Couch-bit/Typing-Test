from os import listdir
from sys import exit
from multiprocessing import Process
from threading import Thread
from tkinter import *
from tkinter import ttk
from Src.typingwindow import TypingWindow


# Negates the value of display_time.
def set_time(event) -> None:

    global Display_time

    Display_time.set(not Display_time.get())

# Negates the value of display_precision.
def set_precision(event) -> None:

    global Display_precision

    Display_precision.set(not Display_precision.get())

# Negates the value of display_chars_per_minute.
def set_chars_per_minute(event) -> None:

    global Display_chars_per_minute

    Display_chars_per_minute.set(not Display_chars_per_minute.get())

# Negates the value of display_words_per_minute.
def set_words_per_minute(event) -> None:

    global Display_words_per_minute

    Display_words_per_minute.set(not Display_words_per_minute.get())

# Negates the value of display_final_graph.
def set_final_graph(event) -> None:

    global Display_final_graph

    Display_final_graph.set(not Display_final_graph.get())

# Sets the dropdown menu value to the one above the current one 
#   (if it's the first one it does nothing).
def text_up(event) -> None:

    global Text_source, List_of_texts, Dropdown_text

    try:
        index_of_text = List_of_texts.index(Text_source.get())
    except IndexError:
        index_of_text = -1

    if (len(List_of_texts) > 0 and index_of_text > 0):
        Text_source.set(List_of_texts[index_of_text - 1])

# Sets the dropdown menu value to the one below the current one 
#   (if it's the last one it does nothing).
def text_down(event) -> None:

    global Text_source, List_of_texts, Dropdown_text

    length_of_list = len(List_of_texts)

    try:
        index_of_text = List_of_texts.index(Text_source.get())
    except IndexError:
        index_of_text = -1

    if (length_of_list > 0 and index_of_text < length_of_list - 1):
        Text_source.set(List_of_texts[index_of_text + 1])

# Intermediates between main and start.
def start_mid(event) -> None:
    Thread(target=start).start()

# Starts the typing test if it's not already running.
def start() -> None:

    global typing_running, Options, Prompt_no_text, \
    Prompt_test_already_running, Prompt_tried_to_close_window, \
    Prompt_no_such_file

    if (Text_source.get() in List_of_texts) and (not typing_running):

        typing_running = True

        # Changes the protocol and bind for closing the window
        # as to not cause unexpected behavior.
        Options.bind('<Escape>', close_not)
        Options.protocol('WM_DELETE_WINDOW', close_not)

        # Gets rid of all prompts.
        Prompt_no_text.grid_forget()
        Prompt_test_already_running.grid_forget()
        Prompt_tried_to_close_window.grid_forget()
        Prompt_no_such_file.grid_forget()

        # Creates the typing window in seperate process.
        typing_test = Process(target=start_process,
            args=('Texts/' + Text_source.get() + '.txt', 
            Display_time.get(), Display_precision.get(),
            Display_chars_per_minute.get(),
            Display_words_per_minute.get(), 
            Display_final_graph.get(),
            icon_path_window))
        
        typing_test.start()
        typing_test.join()

        # Displays prompt if the file couldn't be opened.
        if typing_test.exitcode > 0:
            Prompt_no_such_file.grid(row=103, column=0, columnspan=2)
        
        typing_test.close()

        typing_running = False

        Options.focus()
        # Reenables the option to close the window.
        Options.bind('<Escape>', close)
        Options.protocol('WM_DELETE_WINDOW', close)

    # Displays prompt if no text is selected.  
    elif not typing_running:
        Prompt_no_text.grid(row=100, column=0, columnspan=2)

    # Displays prompt if the test is already running.
    else:
        Prompt_test_already_running.grid(row=101, column=0,
                                          columnspan=2)

# Starts the typing test.
def start_process(text_source : str, display_time : bool,
                   display_precision : bool,
                   display_chars_per_minute : bool,
                   display_words_per_minute : bool,
                   display_final_graph : bool,
                   icon_path_window : str) -> None:

    # Creates TypingWindow object.
    Typing_window = TypingWindow(text_source, display_time,
                                   display_precision,
                                   display_chars_per_minute,
                                   display_words_per_minute,
                                   display_final_graph,
                                   icon_path=icon_path_window)
    # Starts the typing test.
    Typing_window.initiate_typing()

# Terminates the program.
def close(event=None) -> None:

    exit()

# Close substitute gets called when test is already running
# as not to cause unexpected behavior.
def close_not(event=None) -> None:

    Prompt_tried_to_close_window.grid(row=102, column=0, columnspan=2)


if __name__ == '__main__':

    # Defines the list of texts that the user can choose from.
    List_of_texts = []
    # Defines the variable that indicates whether the
    # typing test is currently running.
    typing_running = False

    # Defines the path to the icon used by the windows.
    icon_path_window = 'Icon/icon_test-Window.ico'

    # Gets all .txt files from the Texts folder and adds them
    # to the list (stripping the extension for user experience).
    for file in listdir('Texts'):
        if file.endswith('.txt'):
            List_of_texts.append(file.strip('.txt'))

    Options = Tk()
    Options.title('Typing Speed Test Options')
    Options.minsize(450, 250)
    Options.maxsize(450, 250)
    Options.iconbitmap(icon_path_window)

    Main_frame = ttk.LabelFrame(Options, text='Options')
    Main_frame.pack(padx=10, pady=10)

    Text_source = StringVar(Main_frame)
    Display_time = BooleanVar(Main_frame, value=TRUE)
    Display_precision = BooleanVar(Main_frame, value=TRUE)
    Display_chars_per_minute = BooleanVar(Main_frame, value=TRUE)
    Display_words_per_minute = BooleanVar(Main_frame, value=TRUE)
    Display_final_graph = BooleanVar(Main_frame, value=TRUE)

    Show_Time = ttk.Checkbutton(Main_frame,
                                 text='Show Time',
                                 variable=Display_time)
    Show_precision = ttk.Checkbutton(Main_frame, text='Show Precision',
                                      variable=Display_precision)
    Show_chars_per_minute = ttk.Checkbutton(Main_frame,
                                             text='Show Characters Per Minute',
                                             variable=Display_chars_per_minute)
    Show_words_per_minute = ttk.Checkbutton(Main_frame,
                                             text='Show Words Per Minute',
                                             variable=Display_words_per_minute)
    Show_final_graph = ttk.Checkbutton(Main_frame,
                                        text='Show Final Graph',
                                        variable=Display_final_graph)

    # Sets the default value of the dropdown to the name of the
    # first .txt file in Texts folder or to "No text in folder"
    # if no files were found. 
    try:
        default = List_of_texts[0]
    except IndexError:
        default = 'No text in folder'
    Dropdown_text = ttk.OptionMenu(Main_frame, Text_source,
                                    default, *List_of_texts)

    # Defines the prompts for different situations.
    Prompt_no_text = ttk.Label(Main_frame,
                                text='No text chosen')
    Prompt_test_already_running = ttk.Label(Main_frame,
                                             text=
                                             'Test is already running')
    Prompt_tried_to_close_window = ttk.Label(Main_frame, 
                                              text=
                                              "Can't close options " +
                                              "while test is running")
    Prompt_no_such_file = ttk.Label(Main_frame, 
                                              text=
                                              "No such file") 

    Show_Time.grid(row=0, column=0, sticky=W)
    Show_precision.grid(row=0, column=1, sticky=W)
    Show_chars_per_minute.grid(row=1, column=0, sticky=W)
    Show_words_per_minute.grid(row=1, column=1, sticky=W)
    Show_final_graph.grid(row=2, column=0, columnspan=2)
    Dropdown_text.grid(row=99, column=0, columnspan=2, padx=20, pady=5)

    # Binds escape to terminate the application and
    # enter to start the test.
    Options.bind('<Escape>', close)
    Options.bind('<Return>', start_mid)

    # Binds keyboard shortcuts to operate the options menu.
    Options.bind('t', set_time)
    Options.bind('p', set_precision)
    Options.bind('c', set_chars_per_minute)
    Options.bind('w', set_words_per_minute)
    Options.bind('f', set_final_graph)
    Options.bind('<Up>', text_up)
    Options.bind('<Down>', text_down)

    # Makes sure ending the process is handled correctly when
    # the user closes the window by another means.
    Options.protocol('WM_DELETE_WINDOW', close)

    Options.focus()
    
    Options.mainloop()
    