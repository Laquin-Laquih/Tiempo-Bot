import urllib.request
import json

def sublist_i(l, s):
    sub_set_i = -1
    if s == []:
        sub_set_i = 0
    elif s == l:
        sub_set_i = 0
    elif len(s) > len(l):
        sub_set_i = -1
    else:
        for i in range(len(l)):
            if l[i] == s[0]:
                n=1
                while (n < len(s)) and (l[i+n] == s[n]):
                    n+=1
                if n == len(s):
                    sub_set_i = i
    return sub_set_i

def correct(str):
    #str.replace(" ", "_")
    i=0
    while i < len(str):
        str[i] = str[i].lower()
        if str[i] == ' ':
        	str[i] = '_'
        elif str[i] in (",./_:;?¿¡!'\\\"-^*¨}{[]#@|~€¬)(/&%$·ªº"):
        	str.pop(i)
        	i-=1
        elif str[i] == 'á' or str[i] == 'à':
        	str[i] = 'a'
        elif str[i] == 'é' or str[i] == 'è':
        	str[i] = 'e'
        elif str[i] == 'í' or str[i] == 'ì'or str[i] == 'ï':
        	str[i] = 'i'
        elif str[i] == 'ó' or str[i] == 'ò':
        	str[i] = 'o'
        elif str[i] == 'ú' or str[i] == 'ù' or str[i] == 'ü':
        	str[i] = 'u'
        i+=1
    if(str[len(str)-2] == '_'):
        str.pop(len(str)-2)
    str.append('\n')
    return str

def get_municipality(text):
    final_text = ""
    corrected = correct(text)

    mention_i = sublist_i(corrected, "eltiempoen")
    if mention_i != -1:
        for i in range(11):
            corrected.pop(mention_i)

    new = "".join(corrected)

    data = open("municipalities.data", "r").readlines()

    found = False

    for i, line in enumerate(data):
        if line.lower() == new:
            longitude = list(data[i+1])
            latitude = list(data[i+2])
            found = True
            break

    if not found:
        final_text = "Lo siento, no reconozco ese lugar... ¿Está seguro de que se encuentra en España?"

    else:
        longitude.pop(len(longitude)-1)
        latitude.pop(len(latitude)-1)

        url = "https://api.tutiempo.net/json/?lan=es&apid=zCGX4qzqzaascO3&ll=" + "".join(longitude) + "," + "".join(latitude)

        date = ""
        min_temperature = ""
        max_temperature = ""
        remark = ""

        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
            dic = json.loads(text)

            date = str(dic['day1']['date'])
            min_temperature = str(dic['day1']['temperature_min'])
            max_temperature = str(dic['day1']['temperature_max'])
            remark = str(dic['day1']['text'])

        final_text = "".join((
                date + ": " + remark + ", con temperaturas de entre ", min_temperature, " y ", max_temperature, " ºC.",
                "\n\nFuente: tutiempo.net."
            ))

    return final_text