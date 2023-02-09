from time import (sleep, time)
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk


# Objects of this class are the typing speed test windows themselves.
class TypingWindow(Tk):

    """Description:
    ----------------

    Class of Typing test windows which inherit from Tk class that do not display on creation. 
    
    Customizable parts of them include:
    - the text to be typed
        (more precisely the path to it);
    - whether or not the time should be displayed;
    - whether or not the precision should be displayed
        (precision is correct characters/ total characters,
        1 is subtracted from correct characters if word typed is too long);
    - whether or not characters per minute should be displayed;
    - whether or not words per minute should be displayed;
    - whether or not the final graph illustrating precision on a per character basis should be displayed on summary;
    - delay between window updates.

    Necessary modules:
    ----------------

    - matplotlib;


    Methods:
    ----------------

    initiate_typing() -> None:
        Starts the typing test and displays it for the user. 
        
    set_text_path(text_path : str) -> None:
        Sets the text to type to the one at the given path.
        
    
    Useful Info:
    ----------------

    - use of del keyword over destroy method is preferred when terminating the window completely.
    """

    # Defines fonts.
    Text_font = ('Times New Roman', 15)
    Current_font = ('Times New Roman', 15, 'underline')
    Stat_font = ('Arial', 25)

    def __init__(self, text_path: str, display_time: bool = True,
                  display_precision: bool = True,
                  display_chars_per_minute: bool = True,
                  display_words_per_minute: bool = True,
                  display_final_graph: bool = True,
                  update_delay: float = 0.005,
                  icon_path: str = '') -> None:

        """
        Inits TypingWindow object with the atributes given.

        Args:

            text_path(str):
                Specifies the path to the text which will be typed out by user.

        Returns:
            object:

        Optional Args:

            display_time(bool):
                Specifies whether or not to display time.
            
            display_precision(bool):
                Specifies whether or not to display precision.
            
            display_chars_per_minute(bool):
                Specifies whether or not to display characters per minute (CPM).
            
            display_words_per_minute(bool):
                Specifies whether or not to display words per minute (WPM).
            
            display_final_graph(bool):
                Specifies whether or not to display the final graph. 
            
            update_delay(float):
                Specifies how long the update loop for the window sleeps after every iteration
                    (must be non-negative).
            
            icon_path(str):
                Specifies the icon used by TypingWindow in form of bitmap (more specifivally in this case path
                    (raises _tkinter.TclError if path is incorrect).
        """

        self.text_path = text_path
        self.display_time = display_time
        self.display_precision = display_precision
        self.display_chars_per_minute = display_chars_per_minute
        self.display_words_per_minute = display_words_per_minute
        self.display_final_graph = display_final_graph
        self.display_stats = display_time or display_precision or \
              display_chars_per_minute or display_words_per_minute
        self.update_delay = update_delay
        self.display_summary = self.display_stats or \
              display_final_graph

        self.Text_to_type = []

        self.Correct_letters = {}
        self.Total_letters = {}
        self.Graph_values = {}

        self.running = False
        self.terminate = False
        self.displaying_summary = False

        self.current_word = ''
        self.current_word_index = 0
        self.current_index = 0

        # Defines tkinter window.
        super().__init__()
        self.withdraw()
        self.title('Typing Speed Test')
        if icon_path != '':
            self.iconbitmap(icon_path)

        self.Typing_frame = ttk.LabelFrame(self, text='Typing')
        self.Stats_frame = ttk.LabelFrame(self, text='Statistics')

        self.Typing_frame.grid(row=0, column=0, padx=10)
        if self.display_stats:
            self.Stats_frame.grid(row=0, column=1, padx=10)

        self.timer_0 = 0
        self.timer_current = 0
        self.precision = 0.00
        self.correct_char_sum = 0
        self.total_char_sum = 0
        self.word_sum = 0
        self.chars_per_minute = 0.00
        self.words_per_minute = 0.00

        self.Time_value = StringVar(self.Stats_frame,
                                     value='0:00')
        self.Precision_value = StringVar(self.Stats_frame,
                                         value='0 %')
        self.Chars_per_minute_value = StringVar(self.Stats_frame,
                                                value='0.00')
        self.Words_per_minute_value = StringVar(self.Stats_frame,
                                                value='0.00')

        self.Time_header = ttk.Label(self.Stats_frame, text='Time',
                                      font=self.Stat_font)
        self.Time_label = ttk.Label(self.Stats_frame,
                                     textvariable=
                                     self.Time_value,
                                     font=self.Stat_font,
                                     foreground='blue')
        self.Precision_header = ttk.Label(self.Stats_frame,
                                           text='Precision', 
                                           font=self.Stat_font)
        self.Precision_label = ttk.Label(self.Stats_frame, 
                                         textvariable=
                                         self.Precision_value, 
                                         font=self.Stat_font,
                                         foreground='blue')
        self.CPM_header = ttk.Label(self.Stats_frame,
                                    text='CPM',
                                    font=self.Stat_font)
        self.CPM_label = ttk.Label(self.Stats_frame,
                                   textvariable=
                                   self.Chars_per_minute_value,
                                   font=self.Stat_font,
                                   foreground='blue')
        self.WPM_header = ttk.Label(self.Stats_frame,
                                     text='WPM',
                                     font=self.Stat_font)
        self.WPM_label = ttk.Label(self.Stats_frame,
                                     textvariable=
                                     self.Words_per_minute_value,
                                     font=self.Stat_font,
                                     foreground='blue')
        
        if self.display_stats:
            self._show_stat_widgets()
        
        # Defines placeholders that will be
        # used for displaying the graph.
        # Got code help from 
        # https://www.pythontutorial.net/tkinter/tkinter-matplotlib/.
        self.Figure = None
        self.Graph = None
        self.Canvas = None

    # "PUBLIC" METHODS

    # Starts the test.
    def initiate_typing(self) -> None:

        """
        Starts the typing test and displays it for the user. 
        The method is reusable and blocks running of the subsequent code until the test is finished
            (though it cannot run multiple times simultaneously on the same object).
        The text is going to be "There should be somehing here" if the file is empty.
        Raises FileNotFoundError if something has gone wrong while getting the text from file.
        The user can:
        - type word into the entry widget and press space to submit it and go on to the next word;
        - type the entire text ending the test and displaying the summary
            (summary includes stats and final graph, summary is not displayed if these things should not be displayed);
        - end the test prematurely by pressing enter while still displaying the summary; 
        - end the test prematurely by another means including escape thereby not displaying the summary;
        - track their stats in real time;
        - close the summary by pressing escape or any other means.
        """

        # Loads text and sets the current word to the first one 
        #   (the first one in the default sentence if file is empty).
        self._get_text() 
        try:
            self.current_word = \
            self.Text_to_type[self.current_word_index]
        except IndexError:
            self.Text_to_type = \
            ['There', 'should', 'be', 'something', 'here']
            self.current_word = self.Text_to_type[0]
        
        # Shows typing window to user.
        self._show_typing_window()

        # Program is blocked until user 
        # presses a key inside the window.
        while not self.running and not self.terminate:
            self.update()
            sleep(self.update_delay)

        # Runs mainloop substitute that uses
        # stats_calculate method to update stats.
        while self.running:
            self._stats_calculate()
            self.update()
            sleep(self.update_delay)

        there_is_no_data_for_graph = len(dict(
            filter(lambda item: item[1] > 0,
                    self.Correct_letters.items()))) < 1 and \
        self.display_final_graph

        if there_is_no_data_for_graph:
            self.display_final_graph = False
            self.display_summary = self.display_summary and \
                self.display_stats

        # Displays summary if typing test was "meant to end".
        if self.display_summary:
            self._show_summary()

        self.withdraw()

        if there_is_no_data_for_graph:
            self.display_final_graph = True
            self.display_summary = self.display_summary and \
                  self.display_stats

        self._reset_test()

    # Sets the text_path field to the one given.
    def set_text_path(self, text_path: str) -> None:

        """
        Sets the text to type to the one at the given path.
        Does not affect the test which is currently running (if it is running). 
        """

        self.text_path = text_path

    # __init__ METHODS

    # Adds the stat methods to their frame if they are to be displayed.
    def _show_stat_widgets(self) -> None:

        if self.display_time:
            self.Time_header.grid(row=0, column=0, sticky=W)
            self.Time_label.grid(row=0, column=1, sticky=W)

        if self.display_precision:
            self.Precision_header.grid(row=1, column=0, sticky=W)
            self.Precision_label.grid(row=1, column=1, sticky=W)

        if self.display_chars_per_minute:
            self.CPM_header.grid(row=2, column=0, sticky=W)
            self.CPM_label.grid(row=2, column=1, sticky=W)

        if self.display_words_per_minute:
            self.WPM_header.grid(row=3, column=0, sticky=W)
            self.WPM_label.grid(row=3, column=1, sticky=W)

    # RUNTIME METHODS

    # Loads chosen text from file at given path.
    def _get_text(self) -> None:

        try:
            with open(self.text_path, 'r') as text_file:
                self.Text_to_type = text_file.read().split()
        except OSError:
            raise FileNotFoundError

    # Starts the timer and sets the running field to True.
    def _start_timer(self, event) -> None:

        self.unbind('<Key>')
        self.running = True
        self.timer_0 = time()

    # Shows typing window.
    def _show_typing_window(self) -> None:

        if self.display_stats:
            self.minsize(1100, 700)
            self.maxsize(1100, 700)
        else:
            self.minsize(850, 700)
            self.maxsize(850, 700)
        
        self.Text_label = Text(self.Typing_frame,
                                wrap=WORD,
                                font=self.Text_font,
                                bg='black', fg='white')
        self.Entry_word = ttk.Entry(self.Typing_frame,
                                     font=self.Text_font)

        # Defines tags.
        self.Text_label.tag_configure('CURRENT',
                                       font=self.Current_font)
        self.Text_label.tag_configure('CORRECT',
                                       foreground='green')
        self.Text_label.tag_configure('INCORRECT',
                                       foreground='red')

        # Inserts typing widgets into Typing_frame.
        self.Text_label.grid(row=0, column=0)
        self.Entry_word.grid(row=1, column=0, pady=20)

        # Inserts the text into text widget.
        self.Text_label.insert(END,
                                ''.join([i + ' ' 
                                             for i in 
                                             self.Text_to_type]))
        self.Text_label.config(state=DISABLED)

        self.Text_label.tag_add('CURRENT', '1.0',
                                 '1.' + str(len(self.current_word)))

        self.bind('<Key>', self._start_timer)
        self.bind('<space>', self._check_word)
        self.bind('<Control_L>', self._force_stop)
        self.bind('<Escape>', self._force_stop)

        # Defines protocol that handles terminating the process 
        # if user closes window unexpectedly.
        self.protocol('WM_DELETE_WINDOW', self._force_stop)

        self.deiconify()
        self.focus()
        self.Entry_word.focus()

    # Calculates and updates stats.
    def _stats_calculate(self) -> None:

        if self.display_time or self.display_chars_per_minute or \
             self.display_words_per_minute:
            self.timer_current = round(time() - self.timer_0)

        try:
            if self.display_chars_per_minute:
                self.chars_per_minute = round(
                    (self.correct_char_sum / self.timer_current) * 60,
                     2)
            if self.display_words_per_minute:
                self.words_per_minute = round(
                    (self.word_sum / self.timer_current) * 60,
                     2)
            if self.display_precision:
                self.precision = round(
                    self.correct_char_sum / self.total_char_sum,
                     2)
        except ZeroDivisionError:
            pass

        # Updates the widgets with the new values
        #  (accounting for formatting).
        if self.display_time:
            temp_minutes = str(self.timer_current // 60)
            temp_seconds = str(self.timer_current % 60)
            if len(temp_seconds) < 2:
                temp_seconds = '0' + temp_seconds
            self.Time_value.set(temp_minutes + ':' + temp_seconds)
        if self.display_precision:
            self.Precision_value.set(
                str(int(self.precision * 100)) + ' %')
        if self.display_chars_per_minute:
            self.Chars_per_minute_value.set(str(self.chars_per_minute))
            if len(str(self.chars_per_minute).split('.')[1]) < 2:
                self.Chars_per_minute_value.set(
                    self.Chars_per_minute_value.get() + '0')
        if self.words_per_minute:
            self.Words_per_minute_value.set(str(self.words_per_minute))
            if len(str(self.words_per_minute).split('.')[1]) < 2:
                self.Words_per_minute_value.set(
                    self.Words_per_minute_value.get() + '0')

    # Checks the word in the box once user presses spacebar.
    def _check_word(self, event) -> None:

        typed = self.Entry_word.get().strip()
        self.Entry_word.delete(0, 'end')

        if typed == '' or typed == ' ':
            return

        length_of_word = len(self.current_word)
        length_of_typed = len(typed)

        # Checks the correctness of every character in the word.
        for i in range(length_of_word):

            self.total_char_sum += 1

            # If there is still another character in typed
            # checks if it's correct, otherwise defaults to incorrect.
            if length_of_typed >= i + 1 and \
                  self.current_word[i] == typed[i]:
                self.Text_label.tag_add('CORRECT',
                                         '1.' +
                                         str(self.current_index + i))
                self._letter_stat_update(self.current_word[i], True)
                self.correct_char_sum += 1
            else:
                self.Text_label.tag_add('INCORRECT',
                                         '1.' + 
                                         str(self.current_index + i))
                self._letter_stat_update(self.current_word[i], False)

        # Subtracts 1 from the correct characters
        # if the word typed is too long
        #  (making sure it doesn't turn negative).
        if length_of_typed > length_of_word and \
              self.correct_char_sum > 0:
            self.correct_char_sum -= 1

        self.Text_label.tag_remove('CURRENT',
                                   '1.' + 
                                   str(self.current_index),
                                   '1.' + 
                                   str(self.current_index +
                                        length_of_word))

        self.word_sum += 1
        self.current_word_index += 1
        self.current_index += length_of_word + 1

        # If the index now points to a non-existent word ends the test.
        if self.current_word_index >= len(self.Text_to_type):
            self.running = False
            return

        self.Text_label.tag_add('CURRENT',
                                '1.' + str(self.current_index),
                                '1.' +
                                str(self.current_index + 
                                len(self.Text_to_type
                                    [self.current_word_index])))

        self.current_word = self.Text_to_type[self.current_word_index]

    # Updates letter stats.
    def _letter_stat_update(self, letter: str, correct: bool) -> None:

        if letter in self.Total_letters.keys():
            self.Total_letters[letter] += 1
            if correct:
                self.Correct_letters[letter] += 1
        else:
            self.Total_letters.update({letter: 1})
            if correct:
                self.Correct_letters.update({letter: 1})
            else:
                self.Correct_letters.update({letter: 0})

    # Handles force stop scenarios.
    def _force_stop(self, event=None) -> None:
        
        self.running = False
        self.terminate = True
        if not ('keysym=Control_L' in str(event)):
            self.display_summary = False

    # SUMMARY METHODS

    # Displays summary. 
    def _show_summary(self) -> None:

        self.Typing_frame.grid_forget()

        self.displaying_summary = True

        if self.display_stats and self.display_final_graph:
            self.minsize(1000, 600)
            self.maxsize(1000, 600)
        elif self.display_stats and not self.display_final_graph:
            self.minsize(300, 200)
            self.maxsize(300, 200)
        else:
            self.minsize(1000, 400)
            self.maxsize(1000, 400)

        if self.display_final_graph:

            # Fills the Graph_values dictionary with letters
            # and the relations between how many were
            # correctly typed and total count.
            for i in self.Total_letters.keys():
                self.Graph_values.update({i: self.Correct_letters[i] / 
                                          self.Total_letters[i]})

            # Uses line of code from this thread:
            # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value,
            # but sorted by key.
            self.Graph_values = dict(sorted(self.Graph_values.items(),
                                             key=lambda item: item[0]))

            # Adds The Graph to the window.
            self.Figure = Figure(figsize=(10, 4), dpi=100)
            self.Graph = self.Figure.add_subplot(111)
            self.Canvas = FigureCanvasTkAgg(self.Figure, master=self)
            self.Graph.set_title('Precision By Character')
            self.Graph.bar(self.Graph_values.keys(),
                            self.Graph_values.values(),
                            color=['blue', 'orange'])
            self.Canvas.get_tk_widget().grid(row=1, column=1)

        self.bind('<Escape>', self._close_summary)
        self.protocol('WM_DELETE_WINDOW', self._close_summary)

        while self.displaying_summary:
            self.update()
            sleep(self.update_delay)

    # Closes summary
    def _close_summary(self, event=None) -> None:

        self.displaying_summary = False

    # POST-CORRECTION METHODS

    # Resets fields to default values.
    def _reset_test(self):

        self.Correct_letters = {}
        self.Total_letters = {}
        self.Graph_values = {}

        self.current_word_index = 0
        self.current_index = 0

        self.terminate = False

        self.timer_0 = 0
        self.timer_current = 0
        self.precision = 0.00
        self.correct_char_sum = 0
        self.total_char_sum = 0
        self.word_sum = 0
        self.chars_per_minute = 0.00
        self.words_per_minute = 0.00

        self.Time_value.set('0:00')
        self.Precision_value.set('0 %')
        self.Chars_per_minute_value.set('0.00')
        self.Words_per_minute_value.set('0.00')

        if self.Canvas is not None:
            self.Canvas.get_tk_widget().grid_forget()
            self.Canvas = None
            self.Figure = None
            self.Graph = None
        self.Typing_frame.grid(row=0, column=0, padx=10)

        self.display_summary = self.display_stats or \
              self.display_final_graph
