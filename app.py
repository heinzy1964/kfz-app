
from flask import Flask, render_template_string, request

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Kfz-Kontrolle nach DGUV 70</title>
</head>
<body>
    <h2>Kfz-Kontrolle nach DGUV Vorschrift 70</h2>
    <form method="POST">
        <label>Fahrzeug-Kennzeichen:</label><br>
        <input type="text" name="kennzeichen"><br><br>

        <label>Fahrername:</label><br>
        <input type="text" name="fahrername"><br><br>

        {% for punkt in pruefpunkte %}
            <b>{{ punkt }}</b><br>
            In Ordnung? 
            <select name="ok_{{ loop.index0 }}">
                <option value="">-</option>
                <option value="Ja">Ja</option>
                <option value="Nein">Nein</option>
            </select><br>
            Mangelbeschreibung:<br>
            <input type="text" name="mangel_{{ loop.index0 }}"><br><br>
        {% endfor %}

        <input type="submit" value="Absenden">
    </form>

    {% if submitted %}
        <h3>Erfasste Daten</h3>
        <p><strong>Fahrzeug:</strong> {{ daten['kennzeichen'] }}</p>
        <p><strong>Fahrer:</strong> {{ daten['fahrername'] }}</p>
        <ul>
        {% for eintrag in daten['pruefungsergebnisse'] %}
            <li><b>{{ eintrag['punkt'] }}</b> – OK: {{ eintrag['ok'] }}, Mangel: {{ eintrag['mangel'] }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

pruefpunkte = [
    "Karosserie (äußere Schäden)",
    "Reifen (Profil, Schäden, Luftdruck)",
    "Beleuchtung (Front, Heck, Blinker)",
    "Scheiben & Spiegel (Sauberkeit, Schäden)",
    "Scheibenwischer & Waschanlage",
    "Hupe & Warnsignal",
    "Bremsfunktion (ggf. Probefahrt)",
    "Flüssigkeitsstände sichtbar (Öl, Wasser, Bremsfl.)",
    "Warndreieck & Verbandskasten vorhanden",
    "Zubehör & Ladung gesichert"
]

@app.route("/", methods=["GET", "POST"])
def index():
    submitted = False
    daten = {}

    if request.method == "POST":
        submitted = True
        daten["kennzeichen"] = request.form["kennzeichen"]
        daten["fahrername"] = request.form["fahrername"]
        daten["pruefungsergebnisse"] = []

        for i, punkt in enumerate(pruefpunkte):
            ok = request.form.get(f"ok_{i}", "")
            mangel = request.form.get(f"mangel_{i}", "")
            daten["pruefungsergebnisse"].append({"punkt": punkt, "ok": ok, "mangel": mangel})

    return render_template_string(html_template, pruefpunkte=pruefpunkte, submitted=submitted, daten=daten)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
