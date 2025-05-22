from PIL import Image

filename = input("Enter file to be resized: ")
with open(filename) as img:
    image = Image.open(filename)
    length = int(input("Enter int for length: "))
    height = int(input("Enter int for height: "))
    image = image.resize((length, height), Image.Resampling.LANCZOS)
    opfname = input("Enter filename to save as: ")
    image.save(opfname)
