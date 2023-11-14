import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from huffman import compress, decompress
import pickle
import matplotlib.pyplot as plt
import glob
import cv2

from chess_stegano import main_embedMessage, readMessage
from chess_vission import detect_fen

tree = None

def on_embed():
    global tree
    # Placeholder for embedion logic
    text_value = text_entry_embed.get()
    key_value = key_entry_embed.get()
    blocksize_value = blocksize_combobox.get()

    if blocksize_value == "24 bits":
        blocksize_value = 24
    elif blocksize_value == "32 bits":
        blocksize_value = 32
    elif blocksize_value == "40 bits":
        blocksize_value = 40

    try:
        key_value = int(key_value)
        if key_value < 2 or key_value > 7:
            raise Exception
    except:
        result_label_embed.config(text=f"Invalid key!")
        return

    text_compress, tree = compress(text_value)

    # add padding
    while len(text_compress) % blocksize_value != 0:
        text_compress += "0"

    status, img_path_list = main_embedMessage(text_compress, key_value, blocksize_value)
    if status:
        result_label_embed.config(text=f"Success!, Total image: {len(img_path_list)}")
        # combine all image into one image

        plt.figure(figsize=(10, 10))
        for i in range(len(img_path_list)):
            plt.subplot(4, 4, i+1)
            plt.imshow(plt.imread(img_path_list[i]))
            plt.axis("off")

        plt.savefig("boards/display.png")
        
        update_image("boards/display.png")
    else:
        result_label_embed.config(text=f"Failed!")


def on_save():
    # Placeholder for save logic
    # You can replace this with your save implementation
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    # if file_path:
    #     image.save(file_path)

def on_save_tree():
    # write tree to pickle
    global tree
    file_path = filedialog.asksaveasfilename(defaultextension=".pickle", filetypes=[("Pickle files", "*.pickle"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'wb') as f:
            pickle.dump(tree, f)

def update_image(img_path):
    # Placeholder for image update logic
    # You can replace this with your image update implementation
    global image_display
    image = load_image(img_path)
    image_display.config(image=image)
    image_display.image = image

def load_image(file_path):
    img = Image.open(file_path)
    img = img.resize((150, 150))
    return ImageTk.PhotoImage(img)

# Create the main window
window = tk.Tk()
window.title("Chess Steganography")
window.geometry("400x400")  # Set the default window size

# Create notebook (tabs)
notebook = ttk.Notebook(window)

# Embedion tab
embedion_tab = ttk.Frame(notebook)
notebook.add(embedion_tab, text='Embed Message')

text_label_embed = tk.Label(embedion_tab, text="Text:")
text_label_embed.pack(pady=2.5)
text_entry_embed = tk.Entry(embedion_tab, width=30)
text_entry_embed.pack(pady=5)

key_label_embed = tk.Label(embedion_tab, text="Key (2-7):")
key_label_embed.pack(pady=2.5)
key_entry_embed = tk.Entry(embedion_tab, width=10)
key_entry_embed.pack(pady=5)

blocksize_label = tk.Label(embedion_tab, text="Capacity:")
blocksize_label.pack(pady=5)

# Dropdown select (Combobox) for blocksizes
blocksizes = ["24 bits", "32 bits", "40 bits"]
blocksize_combobox = ttk.Combobox(embedion_tab, values=blocksizes)
blocksize_combobox.pack(pady=5)
blocksize_combobox.set(blocksizes[0])  # Set the default selection

embed_button = tk.Button(embedion_tab, text="Embed", command=on_embed)
embed_button.pack(pady=5)

result_label_embed = tk.Label(embedion_tab, text="")
result_label_embed.pack(pady=5)

# Image displayer
image_label = tk.Label(embedion_tab, text="Chess Board:")
image_label.pack(pady=5)

image_display = tk.Label(embedion_tab, image=None)
image_display.image = None  # To keep a reference and prevent garbage collection
image_display.pack(pady=5)

# Text label
text_label_image = tk.Label(embedion_tab, text="Image Text:")
text_label_image.pack(pady=5)

# Save button
save_button = tk.Button(embedion_tab, text="Save Image", command=on_save)
save_button.pack(pady=5)

# Save button
save_button = tk.Button(embedion_tab, text="Save Huffman Tree", command=on_save_tree)
save_button.pack(pady=5)

### Decoding tab

def on_load_tree():
    global tree
    file_path = filedialog.askopenfilename(defaultextension=".pickle", filetypes=[("Pickle files", "*.pickle"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'rb') as f:
            tree = pickle.load(f)

    print(tree)

    huffman_tree_label.config(text=f"Huffman Tree: {file_path}")

def on_decode():
    print("Decoding...")
    message = ""

    blocksize_value = blocksize_combobox.get()
    key_value = key2_entry_decode.get()

    if blocksize_value == "24 bits":
        blocksize_value = 24
    elif blocksize_value == "32 bits":
        blocksize_value = 32
    elif blocksize_value == "40 bits":
        blocksize_value = 40
    
    try:
        key_value = int(key_value)
        if key_value < 2 or key_value > 7:
            raise Exception
    except:
        result_label_embed.config(text=f"Invalid key!")
        return
    
    folder_path = folder_entry_decode.get()

    for file in glob.glob(f'{folder_path}/board_*.png'):
        # read image
        image_list = []
        img = cv2.imread(file)

        # split image to 8x8
        for i in range(8):
            for j in range(8):
                x = 50 * j
                y = 50 * i
                image_list.append(img[y:y+50, x:x+50])

        # detect piece
        detected_FEN = detect_fen(image_list)

        # compare
        print("Detected FEN: ", detected_FEN)

        msg_read = readMessage(detected_FEN, key_value, block_size=blocksize_value)

        message += msg_read

    print(f"Compressed message: {message}")
    decoded_message = decompress(message, tree)
    print(f"Decoded message: {decoded_message}")
    result_label_decode.config(text=f"Decoded Message: {decoded_message}")


decode_tab = ttk.Frame(notebook)

notebook.add(decode_tab, text='Decode Message')

load_button = tk.Button(decode_tab, text="Load Huffman Tree", command=on_load_tree)
load_button.pack(pady=5)

huffman_tree_label = tk.Label(decode_tab, text="Huffman Tree:")
huffman_tree_label.pack(pady=5)

# add text input

folder_label_decode = tk.Label(decode_tab, text="Folder:")
folder_label_decode.pack(pady=2.5)
folder_entry_decode = tk.Entry(decode_tab, width=30, text="boards")
folder_entry_decode.pack(pady=5)

key2_label_decode = tk.Label(decode_tab, text="Key:")
key2_label_decode.pack(pady=2.5)
key2_entry_decode = tk.Entry(decode_tab, width=30)
key2_entry_decode.pack(pady=5)

decode_button = tk.Button(decode_tab, text="Decode", command=on_decode)
decode_button.pack(pady=5)

result_label_decode = tk.Label(decode_tab, text="")
result_label_decode.pack(pady=5)

# Pack the notebook (tabs) with fill set to both X and Y
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Start the main loop
window.mainloop()
