import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

# Constants
END_MARKER = "#####END#####"
THEME_COLOR = "#2c3e50"
ACCENT_COLOR = "#3498db"
BG_COLOR = "#ecf0f1"
TEXT_COLOR = "#2c3e50"

# Convert message to binary
def msg_to_bin(msg):
    binary = ''.join(format(ord(c), '08b') for c in msg + END_MARKER)
    return binary

# Convert binary to message
def bin_to_msg(binary):
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    text = ''.join(chars)
    if END_MARKER in text:
        return text[:text.index(END_MARKER)]
    else:
        return "[Error: No hidden message found or corrupted image]"

# Hide binary data in image
def hide_data(img, msg):
    binary = msg_to_bin(msg)
    data_index = 0
    new_pixels = []
    for pixel in img.getdata():
        r, g, b = pixel
        if data_index < len(binary):
            r = (r & ~1) | int(binary[data_index])
            data_index += 1
        if data_index < len(binary):
            g = (g & ~1) | int(binary[data_index])
            data_index += 1
        if data_index < len(binary):
            b = (b & ~1) | int(binary[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    if data_index < len(binary):
        raise ValueError("Message too long for this image.")

    img.putdata(new_pixels)
    return img

# Extract hidden message from image
def extract_data(img):
    binary = ""
    for pixel in img.getdata():
        for value in pixel[:3]:
            binary += str(value & 1)

    chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ""
    for byte in chunks:
        char = chr(int(byte, 2))
        message += char
        if END_MARKER in message:
            return message[:message.index(END_MARKER)]
    return "[Error: No hidden message found or corrupted image]"

class CenteredTextLabel(tk.Label):
    """Custom label widget that centers text both horizontally and vertically"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Configure>', self._on_configure)
    
    def _on_configure(self, event):
        """Handle resize events to keep text centered"""
        self.update_idletasks()
        self.configure(wraplength=self.winfo_width())

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureSteg - Image Steganography")
        
        # Window settings - starts maximized
        self.root.state('zoomed')  # For Windows
        # self.root.attributes('-zoomed', True)  # Alternative for Linux/macOS
        self.root.configure(bg=BG_COLOR)
        
        # Initialize attributes
        self.image_path = None
        self.img = None
        
        # Configure styles
        self.configure_styles()
        
        # Setup UI
        self.setup_ui()
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure('TButton', font=('Helvetica', 10), padding=6)
        style.configure('Primary.TButton', foreground='white', background=ACCENT_COLOR)
        style.configure('Secondary.TButton', foreground='white', background=THEME_COLOR)
        style.configure('TEntry', font=('Helvetica', 10), padding=5)
        style.configure('Header.TLabel', font=('Helvetica', 18, 'bold'), foreground=THEME_COLOR)
        style.configure('Subheader.TLabel', font=('Helvetica', 12), foreground=TEXT_COLOR)
        
        # Map button colors
        style.map('Primary.TButton',
                  background=[('active', '#2980b9'), ('pressed', '#1a5276')])
        style.map('Secondary.TButton',
                  background=[('active', '#34495e'), ('pressed', '#1c2833')])
    
    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=(20, 10), fill='x')
        
        ttk.Label(header_frame, text="SecureSteg", style='Header.TLabel').pack()
        ttk.Label(header_frame, text="Hide and extract secret messages in images", 
                 style='Subheader.TLabel').pack(pady=(5, 0))
        
        # Image display section
        image_frame = ttk.Frame(self.root, relief=tk.GROOVE, borderwidth=2)
        image_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.image_label = CenteredTextLabel(
            image_frame, 
            text="No image selected\n\nClick 'Choose Image' to load one", 
            justify='center', 
            font=('Helvetica', 10), 
            foreground='gray',
            bg=BG_COLOR
        )
        self.image_label.pack(pady=40, fill='both', expand=True)
        
        self.status_label = ttk.Label(image_frame, text="", font=('Helvetica', 9), foreground=ACCENT_COLOR)
        self.status_label.pack(pady=(0, 10))
        
        # Button panel
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, fill='x', padx=20)
        
        ttk.Button(button_frame, text="Choose Image", style='Primary.TButton',
                  command=self.open_image).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(button_frame, text="Encode Message", style='Secondary.TButton',
                  command=self.encode_message).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(button_frame, text="Decode Message", style='Secondary.TButton',
                  command=self.decode_message).pack(side='left', padx=5, fill='x', expand=True)
        
        # Message entry
        message_frame = ttk.Frame(self.root)
        message_frame.pack(pady=(10, 20), padx=20, fill='x')
        
        ttk.Label(message_frame, text="Secret Message:", font=('Helvetica', 10)).pack(anchor='w')
        self.message_entry = ttk.Entry(message_frame, font=('Helvetica', 10))
        self.message_entry.pack(fill='x', pady=(5, 0))
        self.message_entry.insert(0, "Type your secret message here...")
        self.message_entry.bind("<FocusIn>", self.clear_placeholder)
        
        # Instructions
        instructions_frame = ttk.Frame(self.root, relief=tk.GROOVE, borderwidth=1)
        instructions_frame.pack(pady=(0, 20), padx=20, fill='x')
        
        instructions = """
        How to use:
        1. Choose an image (PNG or JPEG)
        2. Enter your secret message
        3. Click 'Encode Message' to hide the message
        4. To extract a message, load an encoded image and click 'Decode Message'
        
        Note: For best results, use PNG format as it's lossless.
        """
        ttk.Label(instructions_frame, text=instructions, justify='center', 
                 font=('Helvetica', 9), foreground='gray').pack(padx=10, pady=10)
        
        # Footer
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(side='bottom', fill='x', pady=(0, 10))
        
        ttk.Label(footer_frame, text="© 2025 SecureSteg - Image Steganography Tool", 
                 font=('Helvetica', 8), foreground='gray').pack()
    
    def clear_placeholder(self, event):
        if self.message_entry.get() == "Type your secret message here...":
            self.message_entry.delete(0, tk.END)
    
    def open_image(self):
        path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg"),
                ("All Files", "*.*")
            ],
            initialdir=os.path.expanduser("~"),
        )
        
        if path:
            self.image_path = path
            try:
                img = Image.open(path).convert("RGB")
                img.thumbnail((400, 400))
                self.img = img
                img_tk = ImageTk.PhotoImage(img)
                
                # Clear the text and show the image
                self.image_label.config(image=img_tk, text="")
                self.image_label.image = img_tk
                
                # Update status with image info
                self.status_label.config(
                    text=f"Loaded: {os.path.basename(path)} ({img.size[0]}x{img.size[1]})"
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", 
                    f"Could not open image:\n{str(e)}",
                    parent=self.root
                )
    
    def encode_message(self):
        if not hasattr(self, 'img'):
            messagebox.showerror("Error", "Please select an image first!", parent=self.root)
            return
        
        msg = self.message_entry.get()
        if not msg or msg == "Type your secret message here...":
            messagebox.showerror("Error", "Please enter a message!", parent=self.root)
            return

        try:
            encoded_img = hide_data(self.img.copy(), msg)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve), parent=self.root)
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Encoded Image",
            defaultextension=".png",
            filetypes=[
                ("PNG (Recommended)", "*.png"), 
                ("JPEG", "*.jpg *.jpeg"), 
                ("BMP", "*.bmp")
            ],
            initialfile="encoded_image.png",
            parent=self.root
        )
        
        if save_path:
            try:
                encoded_img.save(save_path)
                messagebox.showinfo(
                    "Success", 
                    f"Message successfully encoded and saved to:\n{save_path}\n\n"
                    "You can now share this image. To extract the message, "
                    "load this image and click 'Decode Message'.",
                    parent=self.root
                )
            except Exception as e:
                messagebox.showerror("Error", f"Could not save image:\n{str(e)}", parent=self.root)
    
    def decode_message(self):
        if not hasattr(self, 'img'):
            messagebox.showerror("Error", "Please select an image first!", parent=self.root)
            return

        decoded_msg = extract_data(self.img)
        
        # Create a new window to display the decoded message
        result_window = tk.Toplevel(self.root)
        result_window.title("Decoded Message")
        result_window.geometry("500x300")
        result_window.resizable(False, False)
        result_window.configure(bg=BG_COLOR)
        
        ttk.Label(result_window, text="Decoded Message", style='Header.TLabel').pack(pady=10)
        
        text_frame = ttk.Frame(result_window)
        text_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side='right', fill='y')
        
        message_text = tk.Text(
            text_frame, 
            wrap='word', 
            yscrollcommand=text_scroll.set,
            padx=10, 
            pady=10,
            font=('Helvetica', 11),
            bg='white',
            relief=tk.FLAT
        )
        message_text.pack(fill='both', expand=True)
        message_text.insert('1.0', decoded_msg)
        message_text.config(state='disabled')
        
        text_scroll.config(command=message_text.yview)
        
        button_frame = ttk.Frame(result_window)
        button_frame.pack(pady=(0, 10))
        
        ttk.Button(button_frame, text="Close", style='Secondary.TButton',
                  command=result_window.destroy).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()