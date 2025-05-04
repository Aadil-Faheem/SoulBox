# SoulBox

Welcome to **SoulBox**! A collection of random, fun, and learning projects that I’m building for fun and personal growth. The goal of this repository is to explore new ideas, experiment with different technologies, and create tools that help with everyday tasks and coding challenges.

<img
src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWMzMmFocGNjYXdqbndhcnlqdWx0YmhjdnlsZ2M1cDlnbDVsYzE2aiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Rlqzt1kP5459lJi6oi/giphy.gif" height="600" />


## Projects

A. **Python to EXE Converter**  
   This app allows you to easily convert Python `.py` files into standalone `.exe` executables using `PyInstaller`. With a user-friendly interface built using `tkinter`, you can select your Python script, press a button, and get an executable file ready for distribution.

   <br>

B. **IP Address Finder**  
   A simple Python app that uses `tkinter` to display your local machine’s hostname and IP address. Additionally, it allows you to input any website (e.g., `github.com`) and fetch the IP address of that website. It's a small tool that showcases basic networking and GUI development using Python. 

   <br>

C. **Game Of Life**  
   A Python app that simulates the famous **"Game of Life"** cellular automaton. It displays a grid where cells evolve based on simple rules of survival, death, and reproduction. This interactive tool lets users start, stop, and control the simulation while visualizing complex patterns emerging from simple initial configurations.

   <br>

D. **Speed Test**  
   A simple Python app that uses `tkinter` to measure and display your internet speed, including download, upload, and ping statistics. It provides a clean and user-friendly interface, showcasing basic network testing and GUI development using Python.
   
   <br>

E. **Schrute Buck Converter**  
   A fun Python app built with tkinter to convert between Schrute Bucks and real USD, inspired by The Office. It features a clean, user-friendly interface and showcases basic GUI development with a humorous twist.
   
   <br>

F. **TaskWatch**  
    Python-based task manager built with `psutil` and `tkinter`. It provides a user-friendly GUI to monitor, log, and manage system processes in real-time.
    It also adds customizable scanning intervals, color-coded usage, logging features, and a clean interface.

   
   
   <br><br>

## Upcoming Projects

I will be expanding this repository with more random, fun, and useful tools. Keep an eye out for new additions in the future! <br><br>

## Getting Started

To run these projects locally, you need Python installed on your machine. Here’s how you can get started: <br><br>

### Prerequisites (For Running Locally OR Use the EXE file to Run):

- **Python 3.x**: Ensure you have Python 3.x installed. [Python website](https://www.python.org/downloads/)
- **PyInstaller** (for Python to EXE Converter)
- **numpy**       (for Game Of Life)
- **matplotlib**  (for Game Of Life)
- **argparse**    (for Game Of Life)
- **pygame**      (for Game Of Life)
- **psutil**   (for TaskWatch)


<br>

  To install Prereqs, you can use pip, Example to Install PyInstaller:
  ```bash
  pip install pyinstaller
  ```

<br>

### How to Use

- **Python to EXE Converter**: <br>
  Locate and Set the Tkinter Folder (First Time Use Only - It will save the location for next use) <br>
  Select a Python file with Browse Button <br>
  Press the “Convert to EXE” button, and the script will generate an `.exe` file in the same directory as the Python file <br>

- **IP Address Finder**: <br>
  Simply click the button to see your machine’s IP address <br>
  You can also input a website name and get its IP <br>
  History of IP searched can also be seen by History Button <br>
  
- **Game Of Life**: <br>
  Start and stop the simulation <br>
  Adjust the grid size <br>
  Change Pattern <br>
  Change Interval <br>
  Watch the evolution of the grid step-by-step or in continuous mode <br>

- **Speed Test**: <br>
  Test Internet Speed with a Single Button <br>
  Get both Download and Upload Speed <br>

- **Schrute Buck Converter**: <br>
  Convert Schrute Buck to USD with a Single Button <br>
  Convert USD to Schrute Buck with a Single Button <br>

- **TaskWatch**: <br>
  Real-time process monitoring (CPU, memory, status) <br>
  Color-coded rows: <br>
  Red = High CPU usage || Yellow = Medium CPU usage || Green = Low CPU usage <br>
  Kill selected process <br>
  Log selected process to file (with timestamp) <br>
  Adjustable scan interval (2s, 5s, 10s) <br>
  Timed logging for selected process over a span of N seconds <br>


  <br>

## Contributing

Feel free to fork this repository, make contributions, and open pull requests! Whether you want to add a new fun project, fix bugs, or improve the documentation, your contributions are always welcome.

<br>

### Guidelines
- Put your Python Script in a Folder that starts with a letter and a dash that is next in line eg: A - Python To Exe
- Make sure to keep the projects fun and useful.
- Follow basic Python coding standards.
- Add a description and instructions for any new tools you add.

<br>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
