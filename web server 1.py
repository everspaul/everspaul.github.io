# main.py
import machine
import socket

# Konfigurer innebygd LED (ofte GPIO 2 på ESP32)
led = machine.Pin(2, machine.Pin.OUT)

# HTML-side som sendes til nettleseren
def generer_html(led_status):
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>ESP32 Webserver</title>
        <style>
            body {{ font-family: Arial; text-align: center; margin-top: 50px; }}
            .knapp {{ padding: 15px 30px; font-size: 20px; color: white; border: none; cursor: pointer; text-decoration: none; }}
            .paa {{ background-color: #4CAF50; }}
            .av {{ background-color: #f44336; }}
        </style>
    </head>
    <body>
        <h1>ESP32 MicroPython Webserver</h1>
        <p>LED-status: <strong>{"PÅ" if led_status else "AV"}</strong></p>
        <p><a href="/?led=paa"><button class="knapp paa">Skru PÅ</button></a></p>
        <p><a href="/?led=av"><button class="knapp av">Skru AV</button></a></p>
        <p>web server 1</p>
    </body>
    </html>
    """
    return html

# Sett opp TCP-socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

print('Webserveren kjører og lytter på port 80...')

while True:
    try:
        # Vent på tilkobling fra nettleser
        conn, addr = s.accept()
        print('Fikk tilkobling fra:', addr)
        request = conn.recv(1024).decode('utf-8')
        
        # Sjekk URL-paramatere for å styre LED
        if '/?led=paa' in request:
            led.value(1)
            print('PÅ')
        elif '/?led=av' in request:
            led.value(0)
            print('AV')
            
        # Hent gjeldende status og send HTML-respons
        respons = generer_html(led.value())
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
        conn.sendall(respons)
        conn.close()
        
    except Exception as e:
        print('En feil oppstod:', e)
