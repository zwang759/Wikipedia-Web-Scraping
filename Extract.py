# python 3.6
# author: Zhiheng Wang
import wikipediaapi
import wptools
import regex
import json
from bs4 import BeautifulSoup


def clean_director():
    if 'director' in infobox.keys():

        # check for split
        if '|' or '<br>' or '<br />' or '\n*' in infobox['director']:

            # split string by <everything> or | except | inside the [] or \n*
            splited_list = regex.split('\<.*?\>|\|\s*(?![^[]*\])|\n\*', infobox['director'])

            # modify strings in list
            for idx, word in enumerate(splited_list):
                # check for duplicate name inside []
                if '|' in word:
                    duplicate_list = word.split('|')
                    for index, substring in enumerate(duplicate_list):
                        temp = regex.sub('\(.*?\)', '', substring)
                        duplicate_list[index] = regex.sub('[^\p{L}-. ]+', '', temp)
                    if len(duplicate_list[0]) > len(duplicate_list[1]):
                        splited_list[idx] = duplicate_list[0]
                    else:
                        splited_list[idx] = duplicate_list[1]
                else:
                    # remove everything in ()
                    temp = regex.sub('\(.*?\)', '', word)

                    # remove non-letter char in all languages except dash
                    temp = regex.sub('[^\p{L}-. ]+', '', temp)

                    # replace non-name string by empty string
                    # there are three or four types of html list in the infobox
                    # reference: https://en.wikipedia.org/wiki/Template:Plainlist
                    temp = regex.sub('plainlist|hlist|unbulleted list|flatlist|bulleted list', '', temp, flags=regex.IGNORECASE)

                    # strip leading space and space in the end
                    temp = temp.lstrip()
                    temp = temp.rstrip()
                    # check the initial letter
                    if ' ' in temp:
                        token_list = temp.split(' ')
                        for p, token in enumerate(token_list):
                            if len(token) >=1 and token[0].islower():
                                token_list[p] = ''
                        token_list = list(filter(None, token_list))
                        temp = ' '.join(token_list)
                        splited_list[idx] = temp
                    else:
                        if len(temp) != 0:
                            if temp[0].islower():
                                splited_list[idx] = ''
                            else:
                                splited_list[idx] = temp
                        else:
                            splited_list[idx] = temp

            # remove duplicates in list if any
            splited_list = list(dict.fromkeys(splited_list))

            # remove empty string in list
            clean_list = list(filter(None, splited_list))

        # No need to split
        else:
            # remove everything in ()
            temp = regex.sub('\(.*?\)', '', infobox['director'])
            # remove non-letter char in all languages except dash
            temp = regex.sub('[^\p{L}-. ]+', '', temp)
            # strip leading space and space in the end
            temp = temp.lstrip()
            temp = temp.rstrip()
            # check the initial letter
            if ' ' in temp:
                token_list = temp.split(' ')
                for p, token in enumerate(token_list):
                    if len(token) >= 1 and token[0].islower():
                        token_list[p] = ''
                token_list = list(filter(None, token_list))
                temp = ' '.join(token_list)

            clean_list = temp
    else:
        clean_list = ''

    return clean_list


def clean_starring():
    if 'starring' in infobox.keys():

        # check for split
        if '|' or '<br>' or '<br />' or '\n*' in infobox['starring']:

            # split string by <everything> or | except | inside the [] or \n*
            splited_list = regex.split('\<.*?\>|\|\s*(?![^[]*\])|\n\*', infobox['starring'])

            # modify strings in list
            for idx, word in enumerate(splited_list):
                # check for duplicate name inside [], and always get the substring after |
                if '|' in word:
                    temp = word.split('|')[1]
                else:
                    temp = word
                # remove everything in ()
                temp = regex.sub('\(.*?\)', '', temp)

                # remove non-letter char in all languages except dash
                temp = regex.sub('[^\p{L}-. ]+', '', temp)

                # replace non-name string by empty string
                # there are three or four types of html list in the infobox
                # reference: https://en.wikipedia.org/wiki/Template:Plainlist
                temp = regex.sub('plainlist|hlist|unbulleted list|flatlist|bulleted list', '', temp, flags=regex.IGNORECASE)

                # strip leading space and space in the end
                temp = temp.lstrip()
                temp = temp.rstrip()

                # check the initial letter
                if ' ' in temp:
                    token_list = temp.split(' ')
                    for p, token in enumerate(token_list):
                        if len(token) >= 1 and token[0].islower():
                            token_list[p] = ''
                    token_list = list(filter(None, token_list))
                    temp = ' '.join(token_list)
                    splited_list[idx] = temp
                else:
                    if len(temp) != 0:
                        if temp[0].islower():
                            splited_list[idx] = ''
                        else:
                            splited_list[idx] = temp
                    else:
                        splited_list[idx] = temp
            # remove duplicates in list if any
            splited_list = list(dict.fromkeys(splited_list))

            # remove empty string in list
            clean_list = list(filter(None, splited_list))

        # No need to split
        else:
            # remove everything in ()
            temp = regex.sub('\(.*?\)', '', infobox['starring'])
            # remove non-letter char in all languages except dash
            temp = regex.sub('[^\p{L}-. ]+', '', temp)
            # strip leading space and space in the end
            temp = temp.lstrip()
            temp = temp.rstrip()

            # check for capitalization
            if ' ' in temp:
                token_list = temp.split(' ')
                for p, token in enumerate(token_list):
                    if len(token) >= 1 and token[0].islower():
                        token_list[p] = ''
                token_list = list(filter(None, token_list))
                temp = ' '.join(token_list)

            clean_list = temp
    else:
        clean_list = ''

    return clean_list


def clean_country():
    if 'country' in infobox.keys():

        # check for split
        if '|' or '<br>' or '<br />' or '\n*' in infobox['country']:

            # split string by <everything> or | except | inside the [] or \n*
            splited_list = regex.split('\<.*?\>|\|\s*(?![^[]*\])|\n\*|\*', infobox['country'])

            # modify strings in list
            for idx, word in enumerate(splited_list):
                # check for duplicate name inside [], and always get the substring after |
                if '|' in word:
                    temp = word.split('|')[1]
                else:
                    temp = word
                # remove everything in ()
                temp = regex.sub('\(.*?\)', '', temp)

                # remove non-letter char in all languages except dash
                temp = regex.sub('[^\p{L}-. ]+', '', temp)

                # replace non-name string by empty string
                # there are three or four types of html list in the infobox
                # reference: https://en.wikipedia.org/wiki/Template:Plainlist
                temp = regex.sub('plainlist|hlist|unbulleted list|flatlist|bulleted list', '', temp, flags=regex.IGNORECASE)

                # strip leading space and space in the end
                temp = temp.lstrip()
                temp = temp.rstrip()

                # remove string that starts with a lower case letter
                # check the initial letter
                if ' ' in temp:
                    token_list = temp.split(' ')
                    for p, token in enumerate(token_list):
                        if len(token) >= 1 and token[0].islower():
                            token_list[p] = ''
                    token_list = list(filter(None, token_list))
                    temp = ' '.join(token_list)
                    splited_list[idx] = temp
                else:
                    if len(temp) != 0:
                        if temp[0].islower():
                            splited_list[idx] = ''
                        else:
                            splited_list[idx] = temp
                    else:
                        splited_list[idx] = temp

            # remove duplicates in list if any
            splited_list = list(dict.fromkeys(splited_list))

            # remove empty string in list
            clean_list = list(filter(None, splited_list))

        # No need to split
        else:
            # remove everything in ()
            temp = regex.sub('\(.*?\)', '', infobox['country'])
            # remove non-letter char in all languages except dash
            temp = regex.sub('[^\p{L}-. ]+', '', temp)
            # strip leading space and space in the end
            temp = temp.lstrip()
            temp = temp.rstrip()
            # check for capitalization
            if ' ' in temp:
                token_list = temp.split(' ')
                for p, token in enumerate(token_list):
                    if len(token) >= 1 and token[0].islower():
                        token_list[p] = ''
                token_list = list(filter(None, token_list))
                temp = ' '.join(token_list)

            clean_list = temp
    else:
        clean_list = ''

    return clean_list


def clean_language():
    if 'language' in infobox.keys():

        # check for split
        if '|' or '<br>' or '<br />' or '\n*' in infobox['language']:

            # split string by <everything> or | except | inside the [] or \n*
            splited_list = regex.split('\<.*?\>|\|\s*(?![^[]*\])|\n\*|\*', infobox['language'])

            # modify strings in list
            for idx, word in enumerate(splited_list):
                # remove everything in ()
                temp = regex.sub('\(.*?\)', '', word)

                # check for duplicate name inside [], and always get the substring after |
                if '|' in temp:
                    temp = temp.split('|')[1]

                # remove non-letter char in all languages except dash dat and whitespace
                temp = regex.sub('[^\p{L}-. ]+', '', temp)

                # replace non-name string by empty string
                # there are three or four types of html list in the infobox
                # reference: https://en.wikipedia.org/wiki/Template:Plainlist
                temp = regex.sub('plainlist|hlist|unbulleted list|flatlist|bulleted list', '', temp,
                                 flags=regex.IGNORECASE)

                # strip leading space and space in the end
                temp = temp.lstrip()
                temp = temp.rstrip()

                # remove string that starts with a lower case letter
                # check the initial letter
                if ' ' in temp:
                    token_list = temp.split(' ')
                    print(token_list)
                    for p, token in enumerate(token_list):
                        if len(token) >= 1 and token[0].islower():
                            token_list[p] = ''
                    token_list = list(filter(None, token_list))
                    temp = ' '.join(token_list)
                    splited_list[idx] = temp
                else:
                    if len(temp) != 0:
                        if temp[0].islower():
                            splited_list[idx] = ''
                        else:
                            splited_list[idx] = temp
                    else:
                        splited_list[idx] = temp

            # remove duplicates in list if any
            splited_list = list(dict.fromkeys(splited_list))

            # remove empty string in list
            clean_list = list(filter(None, splited_list))

        # No need to split
        else:
            # remove everything in ()
            temp = regex.sub('\(.*?\)', '', infobox['language'])
            # remove non-letter char in all languages except dash
            temp = regex.sub('[^\p{L}-. ]+', '', temp)
            # strip leading space and space in the end
            temp = temp.lstrip()
            temp = temp.rstrip()
            # check for capitalization
            if ' ' in temp:
                token_list = temp.split(' ')
                for p, token in enumerate(token_list):
                    if len(token) >= 1 and token[0].islower():
                        token_list[p] = ''
                token_list = list(filter(None, token_list))
                temp = ' '.join(token_list)

            clean_list = temp
    else:
        clean_list = ''

    return clean_list


def clean_runtime():
    # according to https://en.wikipedia.org/wiki/Template:Infobox_film, there is no 'duration'
    if 'runtime' in infobox.keys():
        # check for split
        if '|' or '<br>' or '<br />' or '\n*' in infobox['runtime']:
            # split string by <everything> or | except | inside the [] or \n*
            splited_list = regex.split('\<.*?\>|\|\s*(?![^[]*\])|\n\*|\*', infobox['runtime'])

            # modify strings in list
            for idx, word in enumerate(splited_list):
                # check for duplicate name inside [], and always get the substring after |
                if '|' in word:
                    temp = word.split('|')[1]
                else:
                    temp = word
                # remove everything in ()
                temp = regex.sub('\(.*?\)', '', temp)

                # remove non-numeric char in all languages
                temp = regex.sub('[^0-9]', '', temp)

                # replace non-name string by empty string
                # there are three or four types of html list in the infobox
                # reference: https://en.wikipedia.org/wiki/Template:Plainlist
                temp = regex.sub('plainlist|hlist|unbulleted list|flatlist|bulleted list', '', temp,
                                 flags=regex.IGNORECASE)

                # strip leading space and space in the end
                temp = temp.lstrip()
                temp = temp.rstrip()

                # remove string that starts with a lower case letter
                # check the initial letter
                if ' ' in temp:
                    token_list = temp.split(' ')
                    print(token_list)
                    for p, token in enumerate(token_list):
                        if len(token) >= 1 and token[0].islower():
                            token_list[p] = ''
                    token_list = list(filter(None, token_list))
                    temp = ' '.join(token_list)
                    splited_list[idx] = temp
                else:
                    if len(temp) != 0:
                        if temp[0].islower():
                            splited_list[idx] = ''
                        else:
                            splited_list[idx] = temp
                    else:
                        splited_list[idx] = temp

            # remove duplicates in list if any
            splited_list = list(dict.fromkeys(splited_list))

            # remove empty string in list
            clean_list = list(filter(None, splited_list))

        # No need to split
        else:
            # remove everything in ()
            temp = regex.sub('\(.*?\)', '', infobox['runtime'])
            # remove non-numeric char
            temp = temp = regex.sub('[^0-9]', '', temp)
            # strip leading space and space in the end
            temp = temp.lstrip()
            temp = temp.rstrip()
            # check for capitalization
            if ' ' in temp:
                token_list = temp.split(' ')
                for p, token in enumerate(token_list):
                    if len(token) >= 1 and token[0].islower():
                        token_list[p] = ''
                token_list = list(filter(None, token_list))
                temp = ' '.join(token_list)

            clean_list = temp
    else:
        clean_list = ''

    return clean_list


# input: string
def clean_categories(category):
    clean_list = []
    for cat in category.keys():
        clean_list.append(regex.sub('Category:', '', cat))
    return clean_list


def find_time(category):
    time = ''
    if category != None:
        for i in dict['Category']:
            match = regex.search('Films set in (\d+)', i)
            if match:
                time = match.group(1)
    return time


def find_location(category, text):
    location = ''
    if category != None:
        for i in dict['Category']:
            match = regex.search('Films set in (\p{L}+)', i)
            if match:
                temp = match.group(1)
                if 'the' not in temp:
                    location = temp
    else:
        if 'Plot' in text:
            for i in geographic_location:
                if i in text:
                    location = i
    return location


def clean_text(text):
    pass


# credit to kaungmyatlwin, reference: https://gist.github.com/marijn/396531#file-readme-markdown

geographic_location = ["Afghanistan", "Åland Islands", "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antarctica",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia",
    "Bonaire, Sint Eustatius and Saba",
    "Bosnia and Herzegovina",
    "Botswana",
    "Bouvet Island",
    "Brazil",
    "British Indian Ocean Territory",
    "United States Minor Outlying Islands",
    "Virgin Islands",
    "Virgin Islands",
    "Brunei Darussalam",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cabo Verde",
    "Cayman Islands",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Christmas Island",
    "Cocos Islands",
    "Colombia",
    "Comoros",
    "Congo",
    "Congo",
    "Cook Islands",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Curaçao",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Ethiopia",
    "Falkland Islands",
    "Faroe Islands",
    "Fiji",
    "Finland",
    "France",
    "French Guiana",
    "French Polynesia",
    "French Southern Territories",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guadeloupe",
    "Guam",
    "Guatemala",
    "Guernsey",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Heard Island and McDonald Islands",
    "Holy See",
    "Honduras",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Côte d'Ivoire",
    "Iran",
    "Iraq",
    "Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jersey",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kuwait",
    "Kyrgyzstan",
    "Lao People's Democratic Republic",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macao",
    "Macedonia",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Martinique",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Norfolk Island",
    "Korea",
    "Northern Mariana Islands",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestine, State of",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Pitcairn",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Republic of Kosovo",
    "Réunion",
    "Romania",
    "Russian Federation",
    "Rwanda",
    "Saint Barthélemy",
    "Saint Helena, Ascension and Tristan da Cunha",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Martin",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Sint Maarten",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Georgia and the South Sandwich Islands",
    "Korea",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Svalbard and Jan Mayen",
    "Swaziland",
    "Sweden",
    "Switzerland",
    "Syrian Arab Republic",
    "Taiwan",
    "Tajikistan",
    "Tanzania, United Republic of",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Turks and Caicos Islands",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom of Great Britain and Northern Ireland",
    "United States of America",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela",
    "Viet Nam",
    "Wallis and Futuna",
    "Western Sahara",
    "Yemen",
    "Zambia",
    "Zimbabwe" ]
wiki = wikipediaapi.Wikipedia('en')
cat = wiki.page("Category:2018 films")
cat_pages = [wiki.page(p) for p in cat.categorymembers]
dict = {}
result = {}
count_page = 0
count_infobox = 0

for i in cat_pages:
    count_page += 1
    page = wptools.page(i.title)
    dict['Tittle'] = i.title
    infobox = page.get_parse().data['infobox']
    category = i.categories
    if infobox != None:
        count_infobox += 1
        dict['Language'] = clean_language()
        dict['Country'] = clean_country()
        dict['Director'] = clean_director()
        dict['Starring'] = clean_starring()
        dict['Running_time'] = clean_runtime()
    else:
        dict['Director'] = ''
        dict['Starring'] = ''
        dict['Running_time'] = ''
        dict['Country'] = ''
        dict['Language'] = ''
    dict['Category'] = clean_categories(category)
    dict['Time'] = find_time(category)
    dict['Location'] = find_location(category, i.text)
    soup = BeautifulSoup(i.text)
    text = soup.get_text()
    dict['Text'] = text
    result[count_page] = dict
    print(dict)
        #result[count_page] = dict
        #print(result)
    dict = {}

# with open('file.txt', 'w') as file:
#     file.write(json.dumps(result))

with open('2018_movies.json', 'w') as fp:
    json.dump(result, fp, indent=2)