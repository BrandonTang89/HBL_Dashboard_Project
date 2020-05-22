# setup instructions:
# https://pypi.org/project/pdf2image/
# i got lazy to work with dependencies so path is hardcoded


#PDF TO JPEG -------------------------------------------------------------------------------------------------------------------------------------------------------------------
from pdf2image import convert_from_path

pages = convert_from_path('timetable.pdf', poppler_path= r'C:\Program Files\poppler-0.68.0\bin')
#class_names:"1A","1B","1C","1D","1E","2A","2B","2C","2D","2E","3A","3B","3C","3D","3E","4A","4B","4C","4D","4E","120","119","220","219","320","319","420","419","520","519","620","619","720","719","820","819","920","919","1020","1019","1120","1119","1220","1219","1320","1319","1420","1419","1520","1519","1620","1619","1720","1719","1820","1819","1920","1919","2020","2019","2120","2119","2220","2219","2320","2319","2420","2419"}
class_names = ["119", "219","319","419","519","619","719","819","919","1019","1119","1219","1319","1419","1519","1619","1719","1819","1919","2019","2119","2219","2319","2419","2519"]
class_counter = -1
print( len(pages))


for page in pages:

    try:
        class_counter = class_counter + 1
        page_name = 'images/' + class_names[class_counter] + '.jpeg'
        print(class_counter)
        print(page_name)
        page.save(page_name, 'JPEG')

    except Exception:
        pass

# JPEG ----------------------------------------------------------------------------------------------------------------------------
from PIL import Image

for class_name in class_names:
    image_name = 'images/' + class_name + '.jpeg'
    imageObject = Image.open(image_name)
    imageObject = imageObject.crop((31,164,2307,1573))
    imageObject.save(image_name)

