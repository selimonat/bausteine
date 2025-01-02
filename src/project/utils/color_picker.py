import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ColorPicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Color Picker")
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()
        self.color_palette = []
        self.file_path = r"/Users/mehmet.selim.onat/Pictures/noe_lego/noe.jpg"

        self.image = Image.open(self.file_path)

        self.canvas.config(width=500, height=500)
        self.img_tk = self.root.img_tk = ImageTk.PhotoImage(file=self.file_path)
        self.canvas.create_image((0, 0), anchor=tk.NW, image=self.root.img_tk)

        self.canvas.bind("<Button-1>", self.get_color)
        self.canvas.update()

    def get_color(self, event):
        pass
        if self.image is None:
            return
        x, y = event.x, event.y
        rgb = self.image.getpixel((x, y))
        print(f"Clicked at ({x}, {y}), Color: {rgb}")
        self.canvas.update()
        # self.color_palette.append(rgb)


def main():
    app = ColorPicker()
    app.root.mainloop()



if __name__ == "__main__":
    main()
