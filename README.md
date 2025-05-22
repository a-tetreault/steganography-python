# steganography-python
Exploration of steganography in python. 

Decode operations work in many cases, but still investigating why some strings with short front ends (before a space, ex. Wow! E... or I am ...) don't get decoded and are wonky chars.

Ideas to be added:
- Encryption for the message before being loaded.
- Error checks for image - Sizing (pixels vs. message), file type (PNG or BMP,) ???
- Pull random image from the internet or generate random image to be used?
- Hashing?
