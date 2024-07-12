import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from marketing_site.models import Product
from simulator.models import Element, TrainingData

SCALE = 4

class EditorService:

    def __init__(self, root, width, height):
        self.root = root
        self.root.title("Editor")

        self.canvas_width = width * SCALE
        self.canvas_height = height * SCALE

        # Create canvas
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.canvas.pack(side=tk.LEFT, expand=True)

        # Store images data
        self.images = []
        self.images_full_data = []

        self.selected_image = None

        # Create control panel
        control_panel = tk.Frame(root, width=200, height=height * SCALE)
        control_panel.pack(side=tk.RIGHT, expand=True)

        # Element size/position input
        tk.Label(control_panel, text="Width:").place(x=20, y=10, width=50, height=20)
        self.width_entry = tk.Entry(control_panel)
        self.width_entry.place(x=80, y=10, width=50, height=20)

        tk.Label(control_panel, text="Height:").place(x=20, y=50, width=50, height=20)
        self.height_entry = tk.Entry(control_panel)
        self.height_entry.place(x=80, y=50, width=50, height=20)

        tk.Label(control_panel, text="X:").place(x=20, y=100, width=20, height=20)
        self.x_entry = tk.Entry(control_panel)
        self.x_entry.place(x=80, y=100, width=50, height=20)

        tk.Label(control_panel, text="Y:").place(x=20, y=150, width=20, height=20)
        self.y_entry = tk.Entry(control_panel)
        self.y_entry.place(x=80, y=150, width=50, height=20)

        apply_button = tk.Button(control_panel, text="Apply Changes", command=self.apply_changes)
        apply_button.place(x=60, y=200, width=100, height=30)

        vertical_mirror_button = tk.Button(control_panel, text="Vertical Mirror", command=self.vertical_mirror)
        vertical_mirror_button.place(x=60, y=250, width=100, height=30)

        horizontal_mirror_button = tk.Button(control_panel, text="Horizontal Mirror", command=self.horizontal_mirror)
        horizontal_mirror_button.place(x=60, y=300, width=100, height=30)

        rotate_button = tk.Button(control_panel, text="Rotate", command=self.rotate)
        rotate_button.place(x=60, y=350, width=100, height=30)

        # Canvas size input
        tk.Label(control_panel, text="Canvas Width:").place(x=20, y=400, width=80, height=20)
        self.canvas_width_entry = tk.Entry(control_panel)
        self.canvas_width_entry.place(x=120, y=400, width=50, height=20)

        tk.Label(control_panel, text="Canvas Height:").place(x=20, y=450, width=80, height=20)
        self.canvas_height_entry = tk.Entry(control_panel)
        self.canvas_height_entry.place(x=120, y=450, width=50, height=20)

        canvas_button = tk.Button(control_panel, text="Resize Canvas", command=self.resize_canvas)
        canvas_button.place(x=60, y=500, width=100, height=30)

        tk.Label(control_panel, text="Image ID:").place(x=20, y=550, width=80, height=20)
        self.image_id = tk.Entry(control_panel)
        self.image_id.place(x=120, y=550, width=50, height=20)

        load_button = tk.Button(control_panel, text="Load Image", command=self.load_image)
        load_button.place(x=60, y=600, width=100, height=30)

        export_button = tk.Button(control_panel, text="Export Data", command=self.export_data)
        export_button.place(x=60, y=650, width=100, height=30)

        save_button = tk.Button(control_panel, text="Save Image", command=self.save_image)
        save_button.place(x=60, y=700, width=100, height=30)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Key>", self.on_key)
        self.canvas.bind("<Delete>", self.delete)

        self.width_entry.bind('<KeyRelease>', self.on_key_release)
        self.height_entry.bind('<KeyRelease>', self.on_key_release)

    def on_key_release(self, event):
        if self.selected_image is not None:
            entry_widget = event.widget
            if entry_widget == self.width_entry:
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, int(int(self.width_entry.get()) / self.images_full_data[self.selected_image]["width"] * self.images_full_data[self.selected_image]["height"]))
            elif entry_widget == self.height_entry:
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, int(int(self.height_entry.get()) / self.images_full_data[self.selected_image]["height"] * self.images_full_data[self.selected_image]["width"]))

    def on_click(self, event):
        """ Select an image to edit """
        self.canvas.focus_set()
        # Find the image selected by coordinates
        for index, (_, _, canvas_image) in enumerate(self.images):
            x1, y1, x2, y2 = self.canvas.bbox(canvas_image)
            # Check the position of the image
            if x1 < event.x < x2 and y1 < event.y < y2:
                self.selected_image = index
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, self.images_full_data[index]["width"] // SCALE)
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, self.images_full_data[index]["height"] // SCALE)
                self.x_entry.delete(0, tk.END)
                self.x_entry.insert(0, int((self.images_full_data[index]["x"] - self.canvas_width / 2) // SCALE))
                self.y_entry.delete(0, tk.END)
                self.y_entry.insert(0, int((self.images_full_data[index]["y"] - self.canvas_height / 2) // SCALE))
                break

    def on_drag(self, event):
        """ Change image position by dragging """
        if self.selected_image is not None:
            self.canvas.delete(self.images[self.selected_image][2])
            self.images_full_data[self.selected_image]["x"] = event.x
            self.images_full_data[self.selected_image]["y"] = event.y
            image, tk_image, canvas_image = self.images[self.selected_image]
            canvas_image = self.canvas.create_image(event.x, event.y, anchor=tk.CENTER, image=tk_image)
            self.images[self.selected_image] = (image, tk_image, canvas_image)
            self.images_full_data[self.selected_image]["canvas_image"] = canvas_image

    def on_key(self, event):
        """ Change image position by key press """
        if self.selected_image is not None:
            if event.keysym in ["Up", "Down", "Left", "Right"]:
                x, y = self.images_full_data[self.selected_image]["x"], self.images_full_data[self.selected_image]["y"]
                if event.keysym == "Up":
                    y -= 10
                elif event.keysym == "Down":
                    y += 10
                elif event.keysym == "Left":
                    x -= 10
                elif event.keysym == "Right":
                    x += 10
                self.images_full_data[self.selected_image]["x"] = x
                self.images_full_data[self.selected_image]["y"] = y
                self.canvas.delete(self.images[self.selected_image][2])
                image, tk_image, canvas_image = self.images[self.selected_image]
                canvas_image = self.canvas.create_image(x, y, anchor=tk.CENTER, image=tk_image)
                self.images[self.selected_image] = (image, tk_image, canvas_image)
                self.images_full_data[self.selected_image]["canvas_image"] = canvas_image

    def delete(self, event):
        self.canvas.delete(self.images[self.selected_image][2])
        self.images.pop(self.selected_image)
        self.images_full_data.pop(self.selected_image)
        self.selected_image = None

    def resize_image(self, image):
        return image.resize((self.canvas_width // 2, int(self.canvas_width // 2 / image.width * image.height)))

    def load_image(self):
        if self.image_id.get():
            file_path = Element.objects.get(id=1).get_image_url()
        else:
            file_path = filedialog.askopenfilename()

        if file_path:
            image = self.resize_image(Image.open(file_path))
            tk_image = ImageTk.PhotoImage(image)
            canvas_image = self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, anchor=tk.CENTER, image=tk_image)
            self.images.append((image, tk_image, canvas_image))
            self.images_full_data.append(
                {"image": image, "id": self.image_id.get() if self.image_id.get() else file_path[file_path.rfind('/') + 1 :-4], "tk_image": tk_image, "canvas_image": canvas_image, "x": self.canvas_width // 2, "y": self.canvas_height // 2,
                 "width": image.width, "height": image.height})

    def vertical_mirror(self):
        if self.selected_image is not None:
            image, tk_image, canvas_image = self.images[self.selected_image]
            x = self.images_full_data[self.selected_image]["x"]
            y = self.images_full_data[self.selected_image]["y"]
            if x > self.canvas_width / 2:
                x -= (x - self.canvas_width // 2) * 2
            else:
                x += (self.canvas_width // 2 - x) * 2
            mirrored_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            tk_image = ImageTk.PhotoImage(mirrored_image)
            canvas_image = self.canvas.create_image(x, y, anchor=tk.CENTER, image=tk_image)
            self.images.append((mirrored_image, tk_image, canvas_image))
            self.images_full_data.append(
                {"image": mirrored_image, "id": self.images_full_data[self.selected_image]["id"], "tk_image": tk_image, "canvas_image": canvas_image, "x": x, "y": y,
                 "width": mirrored_image.width, "height": mirrored_image.height})

    def horizontal_mirror(self):
        if self.selected_image is not None:
            image, tk_image, canvas_image = self.images[self.selected_image]
            x = self.images_full_data[self.selected_image]["x"]
            y = self.images_full_data[self.selected_image]["y"]
            if y > self.canvas_height / 2:
                y -= (y - self.canvas_height // 2) * 2
            else:
                y += (self.canvas_height // 2 - y) * 2
            mirrored_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            tk_image = ImageTk.PhotoImage(mirrored_image)
            canvas_image = self.canvas.create_image(x, y, anchor=tk.CENTER, image=tk_image)
            self.images.append((mirrored_image, tk_image, canvas_image))
            self.images_full_data.append(
                {"image": mirrored_image, "id": self.images_full_data[self.selected_image]["id"], "tk_image": tk_image, "canvas_image": canvas_image, "x": x, "y": y,
                 "width": mirrored_image.width, "height": mirrored_image.height})

    def rotate(self):
        if self.selected_image is not None:
            image, tk_image, canvas_image = self.images[self.selected_image]
            rotated_image = image.rotate(90, expand=True)
            self.canvas.delete(canvas_image)
            tk_image = ImageTk.PhotoImage(rotated_image)
            x = self.images_full_data[self.selected_image]["x"]
            y = self.images_full_data[self.selected_image]["y"]
            canvas_image = self.canvas.create_image(x, y, anchor=tk.NW, image=tk_image)
            self.images[self.selected_image] = (rotated_image, tk_image, canvas_image)

    def apply_changes(self):
        if self.selected_image is not None:
            try:
                image, tk_image, canvas_image = self.images[self.selected_image]
                width = int(self.width_entry.get()) * SCALE
                height = int(self.height_entry.get()) * SCALE
                x = int((int(self.x_entry.get()) + self.canvas_width / 2 / SCALE) * SCALE)
                y = int((int(self.y_entry.get()) + self.canvas_height / 2 / SCALE) * SCALE)
                resized_image = image.resize((width, height))
                self.images_full_data[self.selected_image]["width"] = width
                self.images_full_data[self.selected_image]["height"] = height
                self.images_full_data[self.selected_image]["x"] = x
                self.images_full_data[self.selected_image]["y"] = y
                self.canvas.delete(canvas_image)
                tk_image = ImageTk.PhotoImage(resized_image)
                canvas_image = self.canvas.create_image(x, y, anchor=tk.CENTER, image=tk_image)
                self.images[self.selected_image] = (resized_image, tk_image, canvas_image)
                self.images_full_data[self.selected_image]["tk_image"] = tk_image
                self.images_full_data[self.selected_image]["canvas_image"] = canvas_image

            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integer values for width, height, X, and Y.")

    def resize_canvas(self):
        new_width = int(int(self.canvas_width_entry.get()) * SCALE)
        new_height = int(int(self.canvas_height_entry.get()) * SCALE)
        self.canvas_width = new_width
        self.canvas_height = new_height
        self.canvas.config(width=new_width, height=new_height)

    def export_data(self):
        for img in self.images_full_data:

            try:
                TrainingData.objects.create(
                    product=Product.objects.get(link="p1"),
                    element=Element.objects.get(link=img["id"]),
                    container_width=self.canvas_width // SCALE,
                    container_height=self.canvas_height // SCALE,
                    position_x=(img["x"] - self.canvas_width / 2) // SCALE,
                    position_y=(img["y"] - self.canvas_height / 2) // SCALE,
                    width=img["width"] // SCALE,
                    height=img["height"] // SCALE
                )
            except Exception as e:
                return messagebox.showerror("Error", e)

        messagebox.showinfo('Done')
    def save_image(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = EditorService(root, 150, 200)
    root.mainloop()
