import pandas as pd

marker_str = "var marker{} = L.marker([{}, {}]).addTo(map);"
popup_str = "var popup{} = marker{}.bindPopup(\"{}\")"


if __name__ == '__main__':

    entries = pd.read_csv('./entries.csv')
    jstr = []
    seent = set()

    msg_count = 0
    for message, lat, lon in zip(entries['message'], 
            entries['latitude'], entries['longitude']):
        if message not in seent:
            seent.add(message)
            m = marker_str.format(msg_count, lat, lon)
            p = popup_str.format(msg_count, msg_count, message)
            p = p.replace("'", "\\'")
            jstr.extend([m, p])
            msg_count += 1 
            

    with open("./map_template.html", 'r') as src:
        script = src.read()

    script = script.replace("// This content will be replaced.", "\t\t\n".join(jstr))

    with open('map.html', 'w') as dst:
        dst.write(script)
