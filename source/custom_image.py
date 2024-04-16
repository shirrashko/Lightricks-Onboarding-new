from PIL import Image


class CustomImage:
    def __init__(self, path):
        self.image = Image.open(path)
        self.pixels = self.image.load()
        self.width, self.height = self.image.size

    def save(self, path):
        self.image.save(path)

    def show(self):
        self.image.show()
