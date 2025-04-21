# SecureSteg - Image Steganography Tool

## Overview

SecureSteg is a Python-based desktop application that provides a secure and intuitive interface for performing image steganography. Users can hide secret messages within images and retrieve encoded messages using the application. The project leverages **Tkinter** for the graphical user interface and **Pillow** for image manipulation.



## Features

- **Message Encoding**: Hide text messages within PNG or JPEG images.
- **Message Decoding**: Extract hidden messages from encoded images.
- **User-Friendly Interface**: A clean and responsive GUI for ease of use.
- **File Compatibility**: Works seamlessly with PNG (recommended) and JPEG formats.
- **Customizable Themes**: Styled with modern color schemes for better aesthetics.



## Prerequisites

To run SecureSteg, ensure you have the following installed:

- Python 3.7 or later
- Required libraries (install using `pip`):
  ```bash
  pip install pillow
  ```



## How to Use

1. **Launch the Application**:
   - Run the `main.py` file:
     ```bash
     python main.py
     ```

2. **Encode a Message**:
   - Click "Choose Image" to select a PNG or JPEG image.
   - Enter your secret message in the text field.
   - Click "Encode Message" and save the encoded image.

3. **Decode a Message**:
   - Load an encoded image using "Choose Image".
   - Click "Decode Message" to reveal the hidden text.

4. **Best Practices**:
   - Use PNG images for better results (lossless format).
   - Avoid overly large messages as the image capacity is limited.



## Project Structure

- `main.py`: Main application script containing all functionality.
- **Dependencies**:
  - `tkinter`: GUI library for the desktop interface.
  - `Pillow`: Used for image processing.



## Screenshots

**Main Interface**

![Screenshot 2025-04-19 181459](https://github.com/user-attachments/assets/ffc4e599-4eb0-4644-a817-46770bdbff8f)



## Acknowledgements

This project was built as part of a cybersecurity initiative to explore secure communication techniques.  



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



