# Chrome Recovery Pro

Chrome Recovery Pro is a Python-based web application that helps you recover lost tabs from local Google Chrome session backup files. It parses raw Chrome session and tab files (`Session_*` and `Tabs_*`), extracts the URLs, and presents them in a clean, responsive, and easy-to-use interface.

## Features

- **Local Session Parsing**: Reads directly from your local Chrome session files (e.g., in `~/Desktop/Sessions`).
- **Binary Data Extraction**: Robustly extracts URLs from messy binary session data using Regex.
- **Smart Filtering**: Automatically deduplicates URLs, cleans them up, and filters out internal/unnecessary links (like blank Google searches) so you only see what matters.
- **Modern UI**: A responsive, card-based interface built with Bootstrap 5 and custom CSS.
- **Visual Context**: Automatically fetches and displays favicons for recovered domains to help you quickly identify your tabs.
- **Timestamped Records**: Groups tabs by the exact time the session file was last modified.

## Prerequisites

- Python 3.x
- `pip` (Python package manager)

## Installation & Usage

1. **Clone or Download the Repository:**
   Ensure you have the project files (including `app.py`) on your local machine.

2. **Prepare Session Files:**
   The application expects your Chrome session files to be located in:
   ```bash
   ~/Desktop/Sessions
   ```
   *Note: If your files are stored elsewhere, you can modify the `sessions_path` variable in `app.py`.*

3. **Set Up a Virtual Environment:**
   It is recommended to use a virtual environment to manage dependencies.
   ```bash
   # Create a virtual environment named 'venv'
   python3 -m venv venv

   # Activate the virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

4. **Install Dependencies:**
   With your virtual environment activated, install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application:**
   Navigate to the project directory and run:
   ```bash
   python app.py
   ```

6. **View Your Tabs:**
   Open your web browser and go to:
   ```
   http://127.0.0.1:5001
   ```

## Troubleshooting

- **No Session Files Found:** Ensure that files starting with `Session_` or `Tabs_` are placed in the correct directory (`~/Desktop/Sessions`).
- **Port Conflict:** If port `5001` is already in use, you can easily change the running port in the `app.run(port=5001)` section of `app.py`.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---
*Developed by Harsh Jaiswal.*
