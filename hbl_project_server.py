from flask import *
import csv
import requests
import hashlib
from hash_table import *

app = Flask(__name__)
class_set =  ["1A20","1B20","1C20","1D20","1E20","2A19","2B19","2C19","2D19","2E19","3A20","3B20","3C20","3D20","3E20","3F20","4A19","4B19","4C19","4D19","4E19","4F19","0120","0119","0220","0219","0320","0319","0420","0419","0520","0519","0620","0619","0720","0719","0820","0819","0920","0919","1020","1019","1120","1119","1220","1219","1320","1319","1420","1419","1520","1519","1620","1619","1720","1719","1820","1819","1920","1919","2020","2019","2120","2119","2220","2219","2320","2319","2420","2419"]

@app.route('/')
def index():
    return render_template("homepage.html", class_set = class_set)

@app.route('/<class_name>')
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
    except:
        link_list = []

    print(link_list)
    return render_template("dashboard.html", class_name=class_name, link_list=link_list)


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