# 🌐 Network Programming Project

## 📄 Description
This project was developed as part of a university **Computer Networks (ENCS3320)** course. It focuses on **network troubleshooting, socket programming, and real-time communication** using **TCP and UDP protocols**. The project consists of three main tasks:

1. **Network Diagnostic Tools**: Using and analyzing network commands like `ipconfig`, `ping`, `tracert`, `nslookup`, and `telnet`, as well as capturing DNS traffic using **Wireshark**.
2. **TCP-based Web Server**: Implementing a simple **multi-threaded web server** that serves both **English and Arabic webpages**, handles HTTP requests, and manages redirections for unavailable resources.
3. **UDP-based Trivia Game**: A multiplayer **real-time trivia game** using **UDP socket programming**, where the server broadcasts questions, collects answers, and tracks scores.

## 🛠️ Technologies Used
- **Python** (Socket Programming & Multithreading)
- **Wireshark**  (Network Traffic Analysis)
- **Command-Line Network Tools** (`ping`, `tracert`, `nslookup`, etc.)

## 🚀 Features
-  **Network Troubleshooting**: Analyzing network connectivity and performance.
-  **Web Server Implementation**: Serving multilingual web content via **socket programming**.
-  **Multiplayer Trivia Game**: Real-time question-answer interaction over **UDP sockets**.
-  **Data Capture & Analysis**: Monitoring **DNS messages** with **Wireshark**.
-  **Real-time Leaderboard**: Live scoring and player ranking system.

## ▶️ How to Run the Project
1. Clone the repository:
   ```sh
   git clone https://github.com/Raghed33/Socket-Programming
   ```
2. Navigate to the project directory:
   ```sh
   cd cd Socket-Programming
   ```
3. Execute each task separately as per the following instructions:
   - **Task 1 (Network Diagnostic Tools)**: Run the provided network commands directly from the terminal and analyze outputs using Wireshark.
   - **Task 2 (TCP-based Web Server)**: Navigate to `server1/` and run:
     ```sh
     python main.py
     ```
     Then, open a browser and access the hosted webpages.
   - **Task 3 (UDP-based Trivia Game)**: Run the server and client files located in the main project directory:
     ```sh
     python server.py
     ```
     Then, run multiple clients using:
     ```sh
     python client.py
     ```

## ℹ️ Additional Notes
- Ensure required dependencies are installed (`pip install -r requirements.txt` if applicable).
- Wireshark must be installed to analyze network traffic for Task 1.
- Future improvements could include:
  - Enhancing the web server’s request handling.
  - Introducing more interactive game mechanics.
  - Automating network diagnostics with scripting.

## 👥 Team Members & Contributions
- **Arein Almasri**: *Task 1 - Network Diagnostic Tools*
  - Used network utilities for troubleshooting and connectivity analysis.
  - Captured and examined DNS traffic using Wireshark.
  - Provided insights into network performance and diagnostics.

- **Lina Abufarha**: *Task 2 - TCP-based Web Server*
  - Developed a multi-threaded web server for English and Arabic webpages.
  - Implemented HTTP request handling and resource redirection.
  - Ensured stability, error handling, and efficient communication.

- **Raghed Isleem**: *Task 3 - UDP-based Trivia Game*
  - Built a real-time multiplayer trivia game using UDP sockets.
  - Implemented a question broadcasting system and real-time scoring.
  - Optimized game synchronization and minimized network latency.
 
## 📩 Contact
For any inquiries, feel free to contact any team member.

---
**🔗 GitHub Repository**: [Socket-Programming](https://github.com/Raghed33/Socket-Programming)



