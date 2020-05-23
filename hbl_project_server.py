from flask import *
import csv
import requests
import hashlib
import random
from hash_table import *
app = Flask(__name__)

class_set =  ["1A20","1B20","1C20","1D20","1E20","2A19","2B19","2C19","2D19","2E19","3A20","3B20","3C20","3D20","3E20","3F20","4A19","4B19","4C19","4D19","4E19","4F19","0120", "0220", "0320", "0420", "0520", "0620", "0720", "0820", "0920", "1020", "1120", "1220", "1320", "1420", "1520", "1620", "1720", "1820", "1920", "2020", "2120", "2220", "2320", "2420", "0119", "0219", "0319", "0419", "0519", "0619", "0719", "0819", "0919", "1019", "1119", "1219", "1319", "1419", "1519", "1619", "1719", "1819", "1919", "2019", "2119", "2219", "2319", "2419", "2519"]

ip_set = ["1A20","1B20","1C20","1D20","1E20","2A19","2B19","2C19","2D19","2E19","3A20","3B20","3C20","3D20","3E20","3F20","4A19","4B19","4C19","4D19","4E19","4F19"]
j1_set = ["0120", "0220", "0320", "0420", "0520", "0620", "0720", "0820", "0920", "1020", "1120", "1220", "1320", "1420", "1520", "1620", "1720", "1820", "1920", "2020", "2120", "2220", "2320", "2420"]
j2_set = ["0119", "0219", "0319", "0419", "0519", "0619", "0719", "0819", "0919", "1019", "1119", "1219", "1319", "1419", "1519", "1619", "1719", "1819", "1919", "2019", "2119", "2219", "2319", "2419", "2519"]

# For the homepage
@app.route("/")
def index():
    img_url = 'static/images/tjc/' + str(random.randint(1,37)) + '.jpg'
    print (img_url)

    return render_template("homepage.html", ip_set = ip_set, j1_set = j1_set, j2_set = j2_set, img_url = img_url)


# For the main dashboard
@app.route('/<class_name>', methods=['GET'])
def class_name(class_name):
    
    if not class_name in class_set:
        return ("Invalid Class")

    csv_name = "./static/class_link_database/" + class_name + "_links.csv"
    link_list = []
    try:
        with open(csv_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row == []:
                    continue
                link_list.append(row)
                # link_list.append([html.escape(i) for i in row])
    except:
        link_list = []

    print(link_list)
    return render_template("dashboard.html", class_name=class_name, link_list=link_list)

@app.route('/<class_name>', methods=['POST'])
def update_notepad(class_name):
    text_file_name = "./static/class_notepad_database/" +  class_name + ".txt"
    new_text = request.form["notepad"]

    f = open(text_file_name, "w")
    f.write(new_text)
    f.close()

    return new_text

# For the Update Page
@app.route('/update')
def update_form():
    return render_template("update_form.html")

@app.route('/submit_update', methods=['POST'])
def submit_update():
    def check_password(class_name, user_pass):
        if hash_dict[class_name] == hashlib.sha1(user_pass.encode(encoding='UTF-8')).hexdigest():
            return True
        
    user_pass = request.form['password']
    class_name = request.form['class_name']

    if not class_name in class_set:
        return ("INVALID Class")
    
    if not check_password(class_name, user_pass):
        return (render_template("invalid_pass.html"))

    link_list = []
    
    for index in range(1, 16):
        
        title = request.form['title_'+ str(index) + "_custom"]
        if title == "":
            title = request.form['title_'+ str(index)]

        url = request.form["url_" + str(index)]
        desc = request.form["desc_" + str(index)]
        if title != "" or url != "":
            link_list.append((title, url, desc))
        else:
            break
    print(link_list)
    csv_name = "./static/class_link_database/" + class_name + "_links.csv"
    csv_file = open(csv_name, 'w')

    with csv_file:
        writer = csv.writer(csv_file)

        for row in link_list:
            writer.writerow(row)


    return (render_template("success_update.html", class_name=class_name))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True)