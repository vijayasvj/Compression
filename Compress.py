import imghdr
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import io
import cv2
import numpy as np
from io import BytesIO

from zmq import NULL

def compression(img):
    img = np.array(img)
    #cv2.imshow('image_original',img)
    rows,cols, channel = img.shape
    img_b,img_g,img_r = cv2.split(img)
    o_img_b,o_img_g,o_img_r = cv2.split(img)

    nodes = pow(2,depth)
    g_encode = median_cut(img_g,depth)
    b_encode = median_cut(img_b,depth)
    r_encode = median_cut(img_r,depth)

    #np.savetxt("green.csv", img_g, delimiter=",")
    #np.savetxt("blue.csv", img_b, delimiter=",")
    #np.savetxt("red.csv", img_r, delimiter=",")

    #lookup table creation
    with open('lookup32.csv','w') as file:
        file.write("Green lookup:\n")
        file.write("Start,End,Value\n")
        for i in range(nodes):
            file.write(str(g_encode[i])+','+str(g_encode[i+1])+','+str(int(g_encode[i]/2+g_encode[i+1]/2)))
            file.write('\n')
        file.write("Blue lookup:\n")
        file.write("Start,End,Value\n")
        for i in range(nodes):
            file.write(str(b_encode[i])+','+str(b_encode[i+1])+','+str(int(b_encode[i]/2+b_encode[i+1]/2)))
            file.write('\n')
        file.write("Red lookup:\n")
        file.write("Start,End,Value\n")
        for i in range(nodes):
            file.write(str(r_encode[i])+','+str(r_encode[i+1])+','+str(int(r_encode[i]/2+r_encode[i+1]/2)))
            file.write('\n')

    for i in range(rows):
        for j in range(cols):
            index = binarySearch(b_encode,0,nodes-1,img_b[i][j])
            if(index!=-1):
                img_b[i][j] = int(b_encode[index]/2+b_encode[index+1]/2)
            index = binarySearch(g_encode,0,nodes-1,img_g[i][j])
            if(index!=-1):
                img_g[i][j] = int(g_encode[index]/2+g_encode[index+1]/2)
            index = binarySearch(r_encode,0,nodes-1,img_r[i][j])
            if(index!=-1):
                img_r[i][j] = int(r_encode[index]/2+r_encode[index+1]/2)

    rgb = np.dstack((img_r,img_g,img_b))
    return rgb

def binarySearch(encode,l,h,x):
    " ceil binary search returns index and -1 if not present "
    if l>h:
        return -1
    if x>=(encode[h]):
        return h
    mid = int((l+h)/2)
    if encode[mid]==x:
        return mid
    if mid>0 and (encode[mid-1])<=x and x<(encode[mid]):
        return mid-1
    if x<(encode[mid]):
        return binarySearch(encode,l,mid-1,x)
    return binarySearch(encode,mid+1,h,x)

def flatten_image(image):
    " flatten an image from 2d to 1d array "
    flat = []
    flat = [x for sublist in image for x in sublist]
    flat = np.array(flat)
    return flat

def median_cut(img,depth):
    "This function decreases the number of bits required to 2^depth"
    img = flatten_image(img)
    img.sort()
    n = len(img)
    encode = []
    x = int(n/pow(2,depth))
    for i in range(0,pow(2,depth)):
        encode.append(img[i*x])
    encode.append(img[n-1])
    return encode

def SNR(original_img,compressed_img,rows,cols):
    "diff between original img and compressed img"
    noise = [[0 for x in range(rows)] for y in range(cols)]
    for i in range(rows):
        for j in range(cols):
            if(original_img[i][j]>compressed_img[i][j]):
                noise[i][j]=original_img[i][j]-compressed_img[i][j]
            else:
                noise[i][j]=(compressed_img[i][j]-original_img[i][j])
                noise[i][j]*=-1
    return noise



def load_image(image_file):
	img = Image.open(image_file)
	return img 

#resized_image = cv2.resize(img, (256, 256))
#cv2.imwrite('code_blooded.bmp',resized_image)


image = []
zh =1
st.set_page_config(layout = "wide")

body = st.container()

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_seidgi4z.json")

with body:
    st.title('Compress your images')
    st.write('##')
    #st.write('##')

    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown("This particular API was created to keep storage & size in mind. With smartphones & high end cameras in everyone’s hands, people tend to take photos that have huge file size. Most of the times we face issues uploading images to the official websites with limits on images. This API helps you compress all those images to the lowest possible extent and helps you upload them to the required websites. ")
        st.markdown("To see the effectiveness of the compression, upload a LARGE sized image... You will notice that the compressed image has inconspicuous loss.")        

    with right_column:
        st_lottie(lottie, height=250, key="coding")
    #st.write("---")

    uploaded_file = st.file_uploader("Choose a file", type=["png","jpg","jpeg"], accept_multiple_files=False, key=None, help="content image")

    if uploaded_file: 
        depth =7
        if st.button('Confirm'):
            if uploaded_file is not None:
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                opencv_image = cv2.imdecode(file_bytes, 1)
                with st.spinner('Compressing...'):
                    com = compression(opencv_image)
                im = Image.fromarray(com)
                buf = BytesIO()
                im.save(buf, format="JPEG")
                byte_im = buf.getvalue()
                zh = zh*0
                with body:
                    if zh == 0:
                        lbl = "Download image"
                    else :
                        lbl = "Upload an image to compress"
                    btn = st.download_button(
                                    label=lbl,
                                    data=byte_im,
                                    file_name="COMPRESSED.png",
                                    mime="image/jpeg",
                                    )
