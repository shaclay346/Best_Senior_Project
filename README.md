# Best_Senior_Project

Docs:
<u><strong>Libraries Used</strong></u>

<ul>
    <li>speech_recognition: Performing speech recognition online and offline</li>
    <li>pyaudio: Playing and recording audio on a variety of platforms</li>
    <li>pyttsx3: Offline text-to-speech conversion</li>
    <li>beautifulsoup (bs4): Grabbing html from urls</li>
    <li>googlesearch: Searching google and returning top results</li>
    <li>requests: Grabbing urls off the web</li>
    <li>playsound: Playing sounds</li>
    <li>robobrowser: Fetching websites, submitting login forms, and grabbing html</li>
    <li>threading: Allows for multiple threads to track alarms and timers</li>
    <li>multithreading: Allows for multiple threads to track alarms and timers</li>
    <li>random: Random events (coin flips, responses to certian questions, etc.)</li>
    <li>time: Lets certian threads wait to not clog resources</li>
    <li>math: Complex math</li>
    <li>json: Easy parsing through returned web information</li>
    <li>pdb: Python debugging</li>
    <li>re: Provides regular expression matching operations for strings (Unicode and 8-bit)</li>
    <li>datetime: Provides objects for any time, present or other</li>
    <li>keyboard: Grabs keyboard presses</li>
    <li>sys: System functions</li>
    <li>nltk: Command simplification and recognition</li>
    <li>multiprocessing: Allows for multiple processes</li>
    <li>sklearn: SVC (C-Support Vector Classification)</li>
    <li>openpyxl: Works with Excel files</li>
    <li>numpy: Simplify array functions and use</li>
    <li>pandas: Provides data structures for manipulating numerical data</li>
    <li>pickle: Serialize Python objects into Byte stream</li>
    <li>argparse: Arguement parser</li>
    <li>os: Operating system controals</li>
    <li>joblib: Dump and load numpy arrays</li>
    <li>werkzeug: Interactive debugger that allows inspecting stack traces</li>
    <li>io: Provides main facilities for I/O</li>
    <li>urllib: Handels URLs efficiently</li>
    <li>wave: Deals with wave files for sound streams</li>
    <li>selenium: for web browsing and browser automation</li>
</ul>

<u><strong>Installation (Windows)</u></strong>

<ul>
<li>Download the Project</li>
    <ul>
    <li>1) Open a terminal in the same folder as the setpy.py file</li>
    <li>2) Run "pip install ." Note: Do not forget the "." / Full stop</li>
        <ul>
        <li>a) This will install all of the necessary installs from pip and create a build of the project</li>
        </ul>
    </ul>
<li>Running the project Build</li>
    <ul>
    <li>Option 1: terminal</li>
    <ul>
        <li>1) Open the new build -> lib -> FSCVA folder</li>
        <li>2) From there you can open a terminal and run “python” -> “import main” -> “main.main()” to run the program</li>
    </ul>
    <li>Option 2: IDE</li>
    <ul>
        <li>1) Open up an IDE and move to the main.py file in the built project</li>
        <li>2) Run the main.py file</li>
    </ul>
    </ul>
    <li>Upon first running the program you may have to install additional files that weren't installed by the inital building. Just follow all instuctions, installing all required files, & then the project should work.</li>
</ul>

<u><strong>Installation (Mac)</u></strong>

<li>Download the Project</li>
    <ul>
    <li>1) Open a terminal in the same folder as the setpy.py file</li>
    <li>2) Run "python -m pip install ." Note: Do not forget the "." / Full stop</li>
        <ul>
        <li>a) This will install all of the necessary installs from pip and create a build of the project</li>
        </ul>
    </ul>
<li>Running the project Build</li>
    <ul>
    <li>Option 1: terminal</li>
    <ul>
        <li>1) Open the new build -> lib -> FSCVA folder</li>
        <li>2) From there you can open a terminal and run “python” -> “import main” -> “main.main()” to run the program</li>
    </ul>
    <li>Option 2: IDE</li>
    <ul>
        <li>1) Open up an IDE and move to the main.py file in the built project</li>
        <li>2) Run the main.py file</li>
    </ul>
    </ul>
    <li>Upon first running the program you may have to install additional files that weren't installed by the inital building. Just follow all instuctions, installing all required files, & then the project should work.</li>
</ul>

<u><strong>Commands</u></strong>

<ul>
<li><u>Get Upcoming Canvas Assignments</u></li>
    <ul>
    <li>Requirements: Canvas login credentials in "login_credentials.txt" file</li>
    <li>Function: Returns a list of your upcoming assignments for all classes from your Canvas page</li>
    </ul>
<li><u>Get Cafeteria Menu</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Function: Returns the food options being served at the cafeteria for the given meal and day</li>
    </ul>
<li><u>Get Snakebite Balence</u></li>
    <ul>
    <li>Requirements: Get Balence credentials in "login_credentials.txt" file</li>
    <li>Function: Returns the amount of snakebites you have left for the week</li>
    </ul>
<li><u>Get Current Weather</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Function: Returns the current weather, including tempurature in fahrenheit, type of weather (cloudy, sunny, etc.)</li>
    </ul>
<li><u>Flip a Coin</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Function: Returns heads or tails randomly, as if you're flipping a coin</li>
    </ul>
<li><u>Roll Dice</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Function: Returns a number between 1 and a number given (default 6), as if you're rolling a die</li>
    </ul>
<li><u>Get time</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Function: Returns the current time</li>
    </ul>
<li><u>Get Date</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Function: Returns the current date</li>
    </ul>
<li><u>Get Schedule</u></li>
    <ul>
    <li>Requirements: Portal credentials in "login_credentials.txt" file</li>
    <li>Function: Returns the classes you have that day and their current grade</li>
    </ul>
<li><u>Timer</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Functions:</li>
    <ul>
        <li>Creates a timer with a time and name that will sound when the timer ends</li>
        <li>Cancels a set timer</li>
    </ul>
    </ul>
<li><u>Calculator</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Function: Returns the result of a supported operation</li>
    <li>Supported Operations: Addition, Subtraction, Division, Multiplication</li>
    </ul>
<li><u>Alarm</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Functions:</li>
    <ul>
        <li>Creates an alarm within a 24-hour time frame that will sound when it is the given time</li>
        <li>Cancels a set alarm</li>
    </ul>
    </ul>
<li><u>Google Search</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Function: Returns a list of results from a google search of a command</li>
    </ul>
<li><u>Word Definition</u></li>
    <ul>
    <li>Requirements: NA</li>
    <li>Function: Returns the definition of a given word</li>
    </ul>
</ul>