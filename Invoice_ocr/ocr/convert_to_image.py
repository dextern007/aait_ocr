from pdf2image import convert_from_bytes,convert_from_path

def get_images(src):

    image_list = []
    images = convert_from_bytes(src)
    
    for image in images:
        image_list.append(image)
        # print(image)

    return image_list