from pdf2image import convert_from_bytes,convert_from_path

def get_images(src,read_type):

    image_list = []
    if read_type !="bytes":
        images = convert_from_path(src)
    else:
        images = convert_from_bytes(src)
    
    for image in images:
        image_list.append(image)
        # print(image)

    return image_list