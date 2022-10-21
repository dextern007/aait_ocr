from langdetect import detect
# from textblob import TextBlob

def get_launguage_code(txt):
    return detect(txt["res_two"])


from tesserocr import PyTessBaseAPI


def get_launguage_code_new(image):
    img = image
    res = "eng"
    l=[]
    langs =["chi_sim","eng","spa"]
    count = 0
    count2 = 0
    count3 = 0

    with PyTessBaseAPI() as api:

        api.Init(lang = 'chi_sim')
        api.SetImageFile(img)
        # print api.AllWordConfidences()
        arr = list(api.AllWordConfidences())
        sumarr = sum(arr) / float(len(arr))
        l.append(sumarr)

        # print("Confidence score is " + str(sumarr))


    with PyTessBaseAPI() as api:
        
        api.Init(lang = 'eng')
        api.SetImageFile(img)
        # print api.AllWordConfidences()
        arr2 = list(api.AllWordConfidences())
        sumarr2 = sum(arr2) / float(len(arr2))
        l.append(sumarr2)

        # print("Confidence score is " + str(sumarr2))


    with PyTessBaseAPI() as api:
        
        api.Init(lang = 'spa')
        api.SetImageFile(img)
        # print api.AllWordConfidences()
        arr3 = list(api.AllWordConfidences())
        sumarr3 = sum(arr3) / float(len(arr3))
        l.append(sumarr3)

        # print("Confidence score is " + str(sumarr3))

    out =max(l)
    index = l.index(out)
    # with PyTessBaseAPI() as api:
        
    #     api.Init(lang = 'fra')
    #     api.SetImageFile(img)
    #     # print api.AllWordConfidences()
    #     arr4 = list(api.AllWordConfidences())
    #     sumarr4 = sum(arr4) / float(len(arr4))
    #     print("Confidence score is " + str(sumarr4))
    # with PyTessBaseAPI() as api:
    
    #     api.Init(lang = 'nld')
    #     api.SetImageFile(img)
    #     # print api.AllWordConfidences()
    #     arr4 = list(api.AllWordConfidences())
    #     sumarr3 = sum(arr3) / float(len(arr3))



    # n = min(len(arr) , len(arr2) , len(arr3))
    # for i in range(0 , n):
    #     if (arr[i] > arr2[i]) & (arr[i] > arr3[i]):
    #         count += 1
    #     elif (arr2[i] > arr[i]) & (arr2[i] > arr3[i]):
    #         count2 += 1
    #     elif (arr3[i] > arr[i]) & (arr3[i] > arr2[i]):
    #         count3 += 1
    #     else:
    #         pass


    # if (count3 > count2) & (count3 > count):
    #     res = "spa"
    #     # print("Confidence score is " + str(sumarr3))
    #     api.Init(lang = 'spa')
    #     api.SetImageFile(img)

    # elif (count2 > count) & (count2 > count3):
    #     res = "eng"
        
    #     # print("Confidence score is " + str(sumarr2))
    #     api.Init(lang = 'eng')
    #     api.SetImageFile(img)
    # else:
    #     res = "chi_sim"
    #     # print("Confidence score is " + str(sumarr))
    #     api.Init(lang = 'chi_sim')
    #     api.SetImageFile(img)
    
    return langs[index]