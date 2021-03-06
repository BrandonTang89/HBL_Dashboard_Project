from flask import *
from hash_table import *
from PIL import Image
from pathlib import Path
from profanityfilter import ProfanityFilter
import csv
import hashlib
import random
import os.path
import os
import logging
from logging.handlers import TimedRotatingFileHandler

# Set up Flask App and Logging
app = Flask(__name__)

# Rotating Log Files with 5 Day Backup
def create_timed_rotating_log(path):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = TimedRotatingFileHandler(path,
                                       when="d",
                                       interval=1,
                                       backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = create_timed_rotating_log("logs/site_logs.log")

# Define Global Variables
ip_1_set = ["1A20", "1B20", "1C20", "1D20", "1E20"]
ip_2_set = ["2A19", "2B19", "2C19", "2D19", "2E19"]
ip_3_set = ["3A20", "3B20", "3C20", "3D20", "3E20", "3F20"]
ip_4_set = ["4A19", "4B19", "4C19", "4D19", "4E19", "4F19"]

j1_set = ["0120", "0220", "0320", "0420", "0520", "0620", "0720", "0820", "0920", "1020", "1120",
          "1220", "1320", "1420", "1520", "1620", "1720", "1820", "1920", "2020", "2120", "2220", "2320", "2420"]
j2_set = ["0119", "0219", "0319", "0419", "0519", "0619", "0719", "0819", "0919", "1019", "1119", "1219",
          "1319", "1419", "1519", "1619", "1719", "1819", "1919", "2019", "2119", "2219", "2319", "2419", "2519"]

ip_set = ip_1_set + ip_2_set + ip_3_set + ip_4_set
class_set = ip_set + j1_set + j2_set

attendance_links = {
    "ip1": "https://bit.ly/IP1HBLCheckin",
    "ip2": "https://bit.ly/IP2HBLCheckin",
    "ip3": "https://bit.ly/IP3HBLcheckin",
    "ip4": "https://bit.ly/IP4HBLcheckin",
    "jc1": "https://tinyurl.com/TJCT3J1att",
    "jc2": "https://tinyurl.com/TJCT3J2att",
}


# Initialise Profanity Filter with Extra Words
pf = ProfanityFilter()
swear_words_file = "static/swear_words.txt"
with open(swear_words_file) as f:
    for line in f:
        pf.append_words([line.strip()])

# Logging of Requests
@app.before_request
def log_request_info():
    if not request.method == "HEAD":
        logger.info(request)
    #if request.method == "POST":
    #    logger.debug('Body: %s', request.get_data())

# For the homepage
@app.route("/")
def index():
    random_var = random.randint(1, 39)
    if random_var == 39:
        random_var = random.randint(35, 39)

    img_url = 'static/images/tjc/' + str(random_var) + '.jpg'

    return render_template("homepage.html", ip_set=ip_set, j1_set=j1_set, j2_set=j2_set, img_url=img_url)


@app.route("/vid")
def video():

    return render_template("vid.html")


# For the main dashboard
@app.route('/<class_name>/<index_number>', methods=['GET'])
def class_name(class_name, index_number):
    if not class_name in class_set:
        return ("Invalid Class")

    if (int(index_number) < 0 or int(index_number) > 40):
        return ("Invalid Index Number")

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

    # Retreive Notepad
    notepad_name = "./static/class_notepad_database/" + class_name + ".txt"
    try:
        with open(notepad_name) as notepad_file:
            class_notepad = notepad_file.read()
    except:
        class_notepad = ""

    # Choose Icon URL
    icon_url = "static/class_icon_database/" + class_name + ".png"
    if not os.path.exists(icon_url):
        icon_url = "https://cdn.avero-tech.com/tjc/img/icon/android-icon-192x192.png"
    else:
        icon_url = "/" + icon_url

    # Retreive Selected Wallpaper
    wallpaper_csv_name = "./static/class_wallpaper_database/" + class_name + ".csv"
    try:
        with open(wallpaper_csv_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            wallpaper_url = next(csv_reader)[1]
    except:
        wallpaper_url = ""

    # Retreive 2048 Game Scores
    game_score_filename = "./static/class_2048_database/" + class_name + ".txt"

    try:
        with open(game_score_filename) as game_score_file:
            class_score = str(int(float(game_score_file.read())))
    except:
        class_score = "0"

    # Retreive Individual Links
    personal_link_list = []
    user_name = ""
    if int(index_number) > 0:
        csv_name = "./static/personal_link_database/" + \
            class_name + "/" + index_number + "_links.csv"
        if os.path.exists(csv_name):
            with open(csv_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if row == []:
                        continue
                    personal_link_list.append(row)

            user_name = personal_link_list[0][0]
            if user_name != "":
                user_name = user_name + "'s "

            personal_link_list.pop(0)

    # Get Attendance Links
    if class_name in ip_1_set:
        attendance_link = attendance_links["ip1"]
    elif class_name in ip_2_set:
        attendance_link = attendance_links["ip2"]
    elif class_name in ip_3_set:
        attendance_link = attendance_links["ip3"]
    elif class_name in ip_4_set:
        attendance_link = attendance_links["ip4"]
    elif class_name in j1_set:
        attendance_link = attendance_links["jc1"]
    else:
        attendance_link = attendance_links["jc2"]

    return render_template("dashboard.html", class_name=class_name, index_number=index_number, link_list=link_list, class_notepad=class_notepad, icon_url=icon_url, wallpaper_url=wallpaper_url, class_score=class_score, personal_link_list=personal_link_list, user_name=user_name, attendance_link=attendance_link)


@app.route('/<class_name>', methods=['POST'])
def update_notepad(class_name):
    if not class_name in class_set:
        return ("Invalid Class")
    text_file_name = "./static/class_notepad_database/" + class_name + ".txt"
    new_text = request.form["new_text"]
    new_text = pf.censor(new_text)

    f = open(text_file_name, "w")
    f.write(new_text)
    f.close()

    return new_text


# For upload of icons
@app.route('/<class_name>/edit_icon', methods=['POST'])
def update_icon(class_name):
    if not class_name in class_set:
        return ("Invalid Class")

    def make_square(im, min_size=190, fill_color=(255, 255, 255, 255)):
        x, y = im.size
        size = max(min_size, x, y)
        new_im = Image.new('RGBA', (size, size), fill_color)
        new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
        return new_im

    icon_file_name = "./static/class_icon_database/" + class_name + ".png"

    # Write Raw Files
    image_data = request.files['image_upload_input'].read()
    f = open(icon_file_name, 'wb')
    f.write(image_data)
    f.close()

    # Modify and Resave Square Files
    try:
        im = Image.open(icon_file_name)
        im = make_square(im)
        im.thumbnail((192, 192))
        im.save(icon_file_name)
    except:
        os.remove(icon_file_name)
        return ("Error Processing ur ICON")

    print("Image Written to", icon_file_name)
    return (render_template("success_update.html", class_name=class_name, updated_content="Class Icon", link_address=class_name+"/0"))

# For selection of background
@app.route('/<class_name>/edit_wallpaper', methods=['POST'])
def update_wallpaper(class_name):
    if not class_name in class_set:
        return ("Invalid Class")
    wallpaper_file_name = "./static/class_wallpaper_database/" + class_name + ".csv"
    chosen_wallpaper = request.form["chosen_wallpaper"]

    csv_file = open(wallpaper_file_name, 'w')
    with csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["wallpaper", chosen_wallpaper])

    return (render_template("success_update.html", class_name=class_name, updated_content="Class wallpaper", link_address=class_name+"/0"))


# For the Update Page
@app.route('/<class_name>/update')
def update_form(class_name):
    return render_template("update_form.html", class_name=class_name)


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
        return (render_template("invalid_pass.html", link_address="/" + class_name+"/update"))

    link_list = []
    for index in range(1, 16):

        title = request.form['title_' + str(index) + "_custom"]
        if title == "":
            title = request.form['title_' + str(index)]

        url = request.form["url_" + str(index)]
        desc = request.form["desc_" + str(index)]
        if title != "" and url != "":
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

    return (render_template("success_update.html", class_name=class_name, updated_content="Class Links", link_address=class_name+"/0"))

# For the Game Page
@app.route('/<class_name>/game', methods=['GET'])
def game(class_name):
    return render_template("2048/index.html", class_name="class_name")

# Update Class Score with Total Score
@app.route('/<class_name>/game', methods=['POST'])
def update_class_score(class_name):
    if not class_name in class_set:
        return ("Invalid Class")

    text_file_name = "./static/class_2048_database/" + class_name + ".txt"
    new_score = float(request.form["score"])

    # Get Existing Score (If Any)
    if os.path.exists(text_file_name):
        with open(text_file_name) as f:
            cur_score = float(f.read())
    else:
        cur_score = 0

    # Calculate New Score and Write to File
    total_score = str(cur_score + new_score)

    f = open(text_file_name, "w")
    f.write(total_score)
    f.close()

    return total_score


@app.route('/<class_name>/<index_number>/update', methods=['GET'])
def personal_update_form(index_number, class_name):
    return render_template("personal_update_form.html", index_number=index_number, class_name=class_name)


@app.route('/<class_name>/<index_number>/update', methods=['POST'])
def update_personal_links(index_number, class_name):

    def check_password(index_number, class_name, user_pass):
        if personal_hash_dict[class_name][int(index_number)-1] == hashlib.sha1(user_pass.encode(encoding='UTF-8')).hexdigest():
            return True
        return False

    user_pass = request.form['password']

    if not class_name in class_set:
        return ("INVALID Class")

    if int(index_number) < 1 or int(index_number) > 40:
        return ("INVALID Index Number")

    if not check_password(index_number, class_name, user_pass):
        return (render_template("invalid_pass.html", link_address="/" + class_name + "/" + index_number + "/update"))

    personal_link_list = [(request.form["user_name"], "")]

    for index in range(1, 16):

        title = request.form['title_' + str(index) + "_custom"]
        if title == "":
            title = request.form['title_' + str(index)]

        url = request.form["url_" + str(index)]
        desc = request.form["desc_" + str(index)]
        if title != "" and url != "":
            personal_link_list.append((title, url, desc))
        else:
            break

    print(personal_link_list)

    Path("./static/personal_link_database/" + class_name).mkdir(exist_ok=True)
    csv_name = "./static/personal_link_database/" + \
        class_name + "/" + index_number + "_links.csv"
    csv_file = open(csv_name, 'w')

    with csv_file:
        writer = csv.writer(csv_file)

        for row in personal_link_list:
            writer.writerow(row)

    return (render_template("success_update.html", class_name=class_name + " Index Number: " + index_number, updated_content="Individual Links", link_address=class_name+"/"+index_number))


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='3000', debug=True)
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
