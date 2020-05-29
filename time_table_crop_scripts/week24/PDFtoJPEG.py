# setup instructions:
# https://pypi.org/project/pdf2image/
# i got lazy to work with dependencies so path is hardcoded


#PDF TO JPEG -------------------------------------------------------------------------------------------------------------------------------------------------------------------
from pdf2image import convert_from_path

pages = convert_from_path('ip.pdf', poppler_path= r'C:\Program Files\poppler-0.68.0\bin')
class_names =["1A20","1B20","1C20","1D20","1E20","2A19","2B19","2C19","2D19","2E19","3A20","3B20","3C20","3D20","3E20","3F20","4A19","4B19","4C19","4D19","4E19","4F19"]
#class_names = ["0120", "0220", "0320", "0420", "0520", "0620", "0720", "0820", "0920", "1020", "1120", "1220", "1320", "1420", "1520", "1620", "1720", "1820", "1920", "2020", "2120", "2220", "2320", "2420", "2520"]
#class_names = ["0119", "0219","0319","0419","0519","0619","0719","0819","0919","1019","1119","1219","1319","1419","1519","1619","1719","1819","1919","2019","2119","2219","2319","2419","2519"]

class_counter = -1
print( len(pages))


for page in pages:

    try:
        class_counter = class_counter + 1
        page_name = 'timetables/' + class_names[class_counter] + '.jpeg'
        print(class_counter)
        print(page_name)
        page.save(page_name, 'JPEG')

    except Exception:
        pass

# JPEG ----------------------------------------------------------------------------------------------------------------------------
from PIL import Image

for class_name in class_names:
    image_name = 'timetables/' + class_name + '.jpeg'
    imageObject = Image.open(image_name)
    imageObject = imageObject.crop((31,164,2307,1573))
    imageObject.save(image_name)

