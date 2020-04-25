from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import base64
import io
import matplotlib.image as mpimg
from skimage.io import imsave


original_new_upload = {}
processed_new_upload = {}

def image_file_to_b64_string(filename):
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def b64_string_to_ndarray(b64_string):
    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


def ndarray_to_tkinter_image(img_ndarray):
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    out_img = io.BytesIO()
    out_img.write(f.getvalue())
    img_obj = Image.open(out_img)
    img_obj.thumbnail((500,500), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(img_obj)
    return tk_image


def get_new_upload_image(b64_str):
        img_ndarray = b64_string_to_ndarray(b64_str)
        tk_image = ndarray_to_tkinter_image(img_ndarray)
        return tk_image


def main_window():

    def open_button_cmd():
        root.newFilename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        original_new_upload['name'] = root.newFilename
        b64str = image_file_to_b64_string(root.newFilename)
        original_new_upload['b64_string'] = b64str

        print("The selected image is {}".format(root.newFilename))

        new_tk_image = get_new_upload_image(b64str)
        bg_label_1.image = new_tk_image
        bg_label_1.configure(image=new_tk_image)
        return

    root = Tk()
    root.title("Image Database")
    root.geometry("1050x800")


    # original image label
    select_label = ttk.Label(root, text="Original Image")
    select_label.grid(column=0, row=0, columnspan=2)

    # upload label
    select_label = ttk.Label(root, text="Upload a new image")
    select_label.grid(column=0, row=1)

    # open original button
    open_button = ttk.Button(root, text="Open", command=open_button_cmd)
    open_button.grid(column=0, row=2)

    # choose database dropdown
    ttk.Label(root, text="Select from database").grid(column=1, row=1)
    file_name = StringVar()
    original_image_combo = ttk.Combobox(root, textvariable=file_name)
    original_image_combo.grid(column=1, row=2, padx=5)
    original_image_combo['values'] = ("x", "y", "z")
    original_image_combo.state(['readonly'])

    # initialize upload background image
    background = Image.open("images/acl1.jpg")
    bg_image_1 = ImageTk.PhotoImage(background)
    bg_label_1 = ttk.Label(root, image=bg_image_1)
    bg_label_1.image = bg_image_1
    bg_label_1.grid(column=0, row=3, columnspan=2, padx=5)

    # show original metadata
    ori_timestamp_data = "Default"
    ori_timestamp_label = ttk.Label(root, text="timestamp: {}".format(ori_timestamp_data))
    ori_timestamp_label.grid(column=0, row=4, columnspan=2)
    ori_size_data = 0
    ori_size_data = ttk.Label(root, text="image size: {}".format(ori_size_data))
    ori_size_data.grid(column=0, row=5, columnspan=2)

    # download original button
    ori_download_button = ttk.Button(root, text="Download")
    ori_download_button.grid(column=0, row=6, columnspan=2)

    # image process label
    process_label = ttk.Label(root, text="Processed Image")
    process_label.grid(column=3, row=0, columnspan=2)

    # invert label
    invert_label = ttk.Label(root, text="Invert the image you upload")
    invert_label.grid(column=3, row=1)

    # start invertion button
    invert_button = ttk.Button(root, text="Invert")
    invert_button.grid(column=3, row=2)

    # choose database dropdown
    ttk.Label(root, text="Select from database").grid(column=4, row=1)
    file_name = StringVar()
    processed_image_combo = ttk.Combobox(root, textvariable=file_name)
    processed_image_combo.grid(column=4, row=2, padx=5)
    processed_image_combo['values'] = ("x", "y", "z")
    processed_image_combo.state(['readonly'])

    # initialize processed background image
    background = Image.open("images/acl1.jpg")
    bg_image_2 = ImageTk.PhotoImage(background)
    bg_label_2 = ttk.Label(root, image=bg_image_2)
    bg_label_2.image = bg_image_1
    bg_label_2.grid(column=3, row=3, columnspan=2)

    # show processed metadata
    processed_timestamp_data = "Default"
    processed_timestamp_label = ttk.Label(root, text="timestamp: {}".format(processed_timestamp_data))
    processed_timestamp_label.grid(column=3, row=4, columnspan=2)
    processed_size_data = 0
    processed_size_data = ttk.Label(root, text="image size: {}".format(processed_size_data))
    processed_size_data.grid(column=3, row=5, columnspan=2)

    # download original button
    ori_download_button = ttk.Button(root, text="Download")
    ori_download_button.grid(column=3, row=6, columnspan=2)


    root.mainloop()
    return


if __name__ == '__main__':
    main_window()