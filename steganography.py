"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    white = (0,0,0)
    for r in range(x_size):
        for t in range(y_size):
            color = encoded_image.getpixel((r,t))
            p = color[0]
            q = bin(p)
            if q[-1:] == "1":
                pixels[r,t]= (0,
                              0,
                              0)
            if q[-1:] == "0":
                pixels[r,t]= (255,
                              255,
                              255)


    decoded_image.save("images/decoded_image.png")

def text_file_to_string(file_name):
    f = open(file_name)
    final_string = ""
    lines = f.readlines()
    for i in lines:
        for c in i:
            final_string+= c
    return final_string

def write_text(text_to_write, image_size,wrapping=True):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    #Text wrapping. Change parameters for different text formatting
    margin = 10
    offset = 10
    drawer = ImageDraw.Draw(image_text)
    if wrapping == True:
        for line in textwrap.wrap(text_to_write, width=60):
            drawer.text((margin,offset), line, font=font)
            offset += 10
    else:
        for i in text_to_write.splitlines():
            margin = 10
            for t in i:
                drawer.text((margin,offset), t, font = font)
                margin+=5
            offset +=10
    return image_text

def encode_image(text_to_encode, template_image="images/samoyed.jpg",wrapping=True):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    Template_image = Image.open(template_image)
    x_size = Template_image.size[0]
    y_size = Template_image.size[1]
    secret_message = write_text(text_to_encode,(x_size,y_size),wrapping)
    encoded_image = Image.new("RGB", Template_image.size)
    pixels = encoded_image.load()
    for r in range(x_size):
        for t in range(y_size):
            color = Template_image.getpixel((r,t))
            textcolor= secret_message.getpixel((r,t))
            p = color[0]
            g = color[1]
            b = color[2]
            b_w = textcolor[0]
            binp = bin(p)
            if b_w == 255:
                if binp[-1:] == "0":
                    pixels[r,t]= (p,
                              g,
                              b)
                else:
                    pixels[r,t]= (p+1,
                              g,
                              b)
            if b_w == 0:
                if binp[-1:] == "0":
                    pixels[r,t]= (p+1,
                              g,
                              b)
                else:
                    pixels[r,t]= (p,
                              g,
                              b)
    encoded_image.save("images/mjencoded_image.png")

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image(text_file_to_string("secret_plan.txt"),"images/kitty.jpg",False)
    #encode_image("BOOO TESTING 123 @#!")
    decode_image('images/bond.png')
