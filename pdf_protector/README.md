# PDF Protector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, modern, and secure desktop application to easily password-protect and unprotect your PDF files. Built with Python and PyQt6, it offers a clean user interface and reliable encryption, performed entirely on your local machine. Your files are never uploaded to the internet.


## Features

-   **🔒 Encrypt PDFs**: Add a strong password to any PDF file to secure its contents.
-   **🔓 Decrypt PDFs**: Quickly remove password protection from an existing PDF.
-   **✨ Modern UI**: A clean, intuitive, and dark-themed interface that's easy to navigate.
-   **📂 Open File Location**: After processing a file, instantly open its containing folder with a single click.
-   **🔐 Strong Encryption**: Utilizes AES-256 encryption, one of the most secure standards.
-   **💻 Fully Offline**: All operations are performed locally on your computer. Your privacy is guaranteed.
-   **🚀 Cross-Platform**: Works on Windows, macOS, and Linux.

## Getting Started

There are two ways to use PDF Protector: by downloading the ready-to-use executable or by running the script from the source code.

### For Users (Recommended)

1.  Navigate to the [**Releases**](https://github.com/your-username/your-repository-name/releases) page of this repository.
2.  Download the latest executable (`.exe` for Windows) from the assets list.
3.  Run the application. No installation is required!

### For Developers (Running from Source)

If you want to run the application from the source code, follow these steps.

**Prerequisites:**
-   Python 3.8+

**Installation:**

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/PetterSsantos/Protetor-de-PDFs.git
    cd Protetor-de-PDFs
    ```

2.  **(Recommended) Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```sh
    python pdf_protector.py
    ```

## How to Use

1.  Launch the application.
2.  Select the **Protect PDF** or **Unprotect PDF** tab based on your needs.
3.  Click **Browse...** to select your PDF file.
4.  Enter the password in the password field.
5.  Click the main action button (**🔒 Protect File** or **🔓 Desprotect File**).
6.  A status message will appear at the bottom confirming success or failure.
7.  On success, click the **📂 Open Location** button to find your newly created file.

## Built With

-   [Python](https://www.python.org/) - The core programming language.
-   [PyQt6](https://riverbankcomputing.com/software/pyqt/) - For the graphical user interface.
-   [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) - For core PDF processing and encryption.
-   [pyqtdarktheme](https://pypi.org/project/pyqtdarktheme/) - For the modern dark look and feel.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

#### See you later, fellow programmer 👋