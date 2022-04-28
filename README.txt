Description:

This is a typing test that first displays an options menu which lets the user choose the text and stats to display. The app is written in Python 3.10.

Necessary modules:

- matplotlib (pip install matplotlib);
- ttkthemes (pip install ttkthemes).

Options menu behavior:

- User can check boxes that dictate whether certain stats should be displayed
	(User can also use keyboard shortcuts: t - time, p - precision, c - CPM, w - WPM, f - final graph);
- User can choose text from dropdown menu 
	(texts are obtained from Texts folder, User can also navigate dropdown using arrows on keyboard);
- User can close options menu by pressing escape or any other means
	(assuming the typing test is not active, otherwise options will not close unless closed by task manager);
- User can start the test by pressing enter 
	(test will not start if one is already running);
- The test will not start if no text is chosen.

Typing test behavior:

- If the file is empty a placeholder text will be displayed 
	("There should be something here")
- User can type as soon as the window opens;
- Timer starts along with the first keypress;
- The current word is displayed in bold, while correctly typed letters are displayed in green and incorrect ones in red;
- User can submit the word by pressing spacebar;
- If the user chose to display stats they are displayed on the right side of the window;
- User can press left ctrl to end test prematurely while still displaying the summary;
- User can end the test without displaying the summary by pressing escape or any other means;
- The test also ends when the last word is typed, displaying the summary;
- Summary contains stats along with a precision by letter graph
	(Excluding elements based on options, not displaying the graph if user didn't type out any characters correctly);
- Summary is not displayed if there is nothing to be displayed;
- Summary can be closed by escape or any other means.

Folders and Files:
 
- User can add their own texts to the Texts folder
	(non .txt files added to this folder will be ignored, 
	the app will ignore new lines and display the text as one paragraph, <300 words is recommended);
- User should not mess with the placement of source files 
	(Src folder and Icon_Test-Window.ico in Icon folder);
- The actual app is the pyw file in the folder.
