import hashlib
from pprint import pprint
def hash_a_dict(plain_dict):
        for item in plain_dict.items():
            plain_dict[item[0]] =  hashlib.sha1(item[1].encode(encoding='UTF-8')).hexdigest()

        return plain_dict


def hash_a_dict_2(plain_dict):
    for item in plain_dict.items():
        plain_dict[item[0]] =  [hashlib.sha1(i.encode(encoding='UTF-8')).hexdigest() for i in item[1]]

    return plain_dict

pass_dict = {
            "1A20": "mushywatermelon",
            "1B20": "crumblypear",
            "1C20": "sharppear",
            "1D20": "giantpomelo",
            "1E20": "maturetomato",
            "2A19": "milddurian",
            "2B19": "gameyelderberry",
            "2C19": "crunchypapaya",
            "2D19": "riperaspberry",
            "2E19": "maturehoneyberry",
            "3A20": "maturewatermelon",
            "3B20": "happystrawberry",
            "3C20": "ripetomato",
            "3D20": "seasonedapples",
            "3E20": "hotpapaya",
            "3F20": "bittersweetelderberry",
            "4A19": "crumblybanana",
            "4B19": "bittersweetacai",
            "4C19": "grilledblackcurrants",
            "4D19": "spicyorange",
            "4E19": "tartjackfruit",
            "4F19": "bittersweetdurian",
            "0120": "bittersweetsoursop",
            "0119": "grilledapples",
            "0220": "incrediblewatermelon",
            "0219": "bittercranberry",
            "0320": "happyorange",
            "0319": "savouryraspberry",
            "0420": "gameybanana",
            "0419": "gameyorange",
            "0520": "incredibleraspberry",
            "0519": "mushyelderberry",
            "0620": "astringentelderberry",
            "0619": "happywatermelon",
            "0720": "gameypear",
            "0719": "gameycranberry",
            "0820": "tartmango",
            "0819": "sharpblackcurrants",
            "0920": "grilledelderberry",
            "0919": "astringentstrawberry",
            "1020": "mushyhoneyberry",
            "1019": "happyraspberry",
            "1120": "crunchyblackcurrants",
            "1119": "mushywatermelon",
            "1220": "mildblackcurrants",
            "1219": "giantapricots",
            "1320": "maturedurian",
            "1319": "giantcherry",
            "1420": "tartpomegranate",
            "1419": "crumblyelderberry",
            "1520": "spicypomegranate",
            "1519": "maturesoursop",
            "1620": "happypapaya",
            "1619": "maturestrawberry",
            "1720": "acidicpomelo",
            "1719": "crumblysoursop",
            "1820": "spicyelderberry",
            "1819": "unsaltedapricots",
            "1920": "bittersweetstrawberry",
            "1919": "burntpassionfruit",
            "2020": "happyorange",
            "2019": "sourelderberry",
            "2120": "blandcranberry",
            "2119": "mushystrawberry",
            "2220": "astringentblackcurrants",
            "2219": "gameyjackfruit",
            "2320": "spicycherry",
            "2319": "maturecherry",
            "2420": "mushyblackcurrants",
            "2419": "incredibleapricots"
        }

personal_pass_dict = {
    "1319": ["hello","hellogaian"]
}

pprint(hash_a_dict_2(personal_pass_dict))