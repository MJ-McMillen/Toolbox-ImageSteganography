"""A program that encodes and decodes hidden images in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    for r in range(x_size):
        for t in range(y_size):
            color = encoded_image.getpixel((r,t))
            rbin = bin(color[0])
            rbin = rbin[2:]
            lenr = 8-len(rbin)
            rbin = "0"*lenr + rbin
            bbin = bin(color[1])
            bbin = bbin[2:]
            lenb = 8-len(bbin)
            bbin = "0"*lenb + bbin
            gbin = bin(color[2])
            gbin = gbin[2:]
            leng = 8-len(gbin)
            gbin = "0"*leng + gbin
            pixels[r,t] = (int(rbin[5:]+"00000",2),int(bbin[5:]+"00000",2),int(gbin[5:]+"00000",2))
    decoded_image.save("images/decoded_image.png")


def fix_image(image,template_image):
    """This reformats the image so that it is the same dimensions as the parant image."""
    secret = Image.open(image)
    target_size = template_image.size
    current_size = secret.size
    backdrop = Image.open("images/black.jpg")
    backdrop= backdrop.resize(target_size)
    if current_size[0]> target_size[0] and current_size[1]>target_size[1]:
        if current_size[0]> current_size[1]:
            #x is the largest.
            #x/y=c/z    zx/y = c  zx = cy  z = cy/x
            secret = secret.resize((target_size[0],int((target_size[0]*current_size[1])/current_size[0])))
            backdrop.paste(secret,(0,int((target_size[1]-secret.size[1])/2)))
            backdrop.save("images/fixedsecret.jpg")
        else:
            #y is the largest.
            secret = secret.resize((int((target_size[1]*current_size[0])/current_size[1]),target_size[1]))
            backdrop.paste(secret,(int((target_size[0]-((target_size[1]*current_size[0])/current_size[1])/2)),0))
            backdrop.save("images/fixedsecret.jpg")
    elif current_size[0]> target_size[0]:
        #resize down based on x size.
        secret = secret.resize((target_size[0],int((target_size[0]*current_size[1])/current_size[0])))
        backdrop.paste(secret,(0,int((target_size[1]-((target_size[0]*current_size[1])/current_size[0])/2))))
        backdrop.save("images/fixedsecret.jpg")
    elif current_size[1]>target_size[1]:
        #resize down based on y size.
        secret = secret.resize((int((target_size[1]*current_size[0])/current_size[1]),target_size[1]))
        backdrop.paste(secret,(int((target_size[0]-((target_size[1]*current_size[0])/current_size[1])/2)),0))
        backdrop.save("images/fixedsecret.jpg")
    else:
        #just pad the image.
        backdrop.paste(secret,(int((target_size[0]-current_size[0])/2),int((target_size[1]-current_size[1])/2)))
        backdrop.save("images/fixedsecret.jpg")


def encode_image(image_to_encode, template_image="images/cat.jpg"):
    """Encodes an image into another image.

    """
    Template_image = Image.open(template_image)
    x_size = Template_image.size[0]
    y_size = Template_image.size[1]
    secret_message = fix_image(image_to_encode,Template_image)
    secret_message = Image.open("images/fixedsecret.jpg")
    encoded_image = Image.new("RGB", Template_image.size)
    pix = encoded_image.load()
    for r in range(x_size):
        for t in range(y_size):
            color = Template_image.getpixel((r,t))
            secretcolor = secret_message.getpixel((r,t))
            rbin = bin(color[0])
            rbin = rbin[2:]
            lenr = 8-len(rbin)
            rbin = "0"*lenr + rbin
            bbin = bin(color[1])
            bbin = bbin[2:]
            lenb = 8-len(bbin)
            bbin = "0"*lenb + bbin
            gbin = bin(color[2])
            gbin = gbin[2:]
            leng = 8-len(gbin)
            gbin = "0"*leng + gbin

            srbin = bin(secretcolor[0])
            srbin = srbin[2:]
            slenr = 8-len(srbin)
            srbin = "0"*slenr + srbin
            sbbin = bin(secretcolor[1])
            sbbin = sbbin[2:]
            slenb = 8-len(sbbin)
            sbbin = "0"*slenb + sbbin
            sgbin = bin(secretcolor[2])
            sgbin = sgbin[2:]
            sleng = 8-len(sgbin)
            sgbin = "0"*sleng + sgbin

            ein = rbin[0]+rbin[1]+rbin[2]+rbin[3]+rbin[4]+srbin[0]+srbin[1]+srbin[2]
            zwei = bbin[0]+bbin[1]+bbin[2]+bbin[3]+bbin[4]+sbbin[0]+sbbin[1]+sbbin[2]
            drei = gbin[0]+gbin[1]+gbin[2]+gbin[3]+gbin[4]+sgbin[0]+sgbin[1]+sgbin[2]
            pix[r,t]= (int(ein,2),int(zwei,2),int(drei,2))
    encoded_image.save("images/mjencoded_image.png")

if __name__ == '__main__':

    print("Encoding the image...")
    encode_image("images/kitty.jpg")
    #encode_image("BOOO TESTING 123 @#!")
    decode_image('images/bond.png')
