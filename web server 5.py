import network
import time
import socket


def network_connect(network_name, network_password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(network_name, network_password)

    timeout = 60
    while not station.isconnected() and timeout > 0:
        time.sleep_ms(1000)
        timeout -= 1
    if station.isconnected():
        ips_and_mask = station.ifconfig()
        print(ips_and_mask)
        my_ip = ips_and_mask[0]
        return my_ip
    return False


  
def page_data():
    html = """
        <!DOCTYPE HTML>
        <html>
            <head>
                <title>get params</title>
            </head>
            <body>
                <form action="/" method="get" target="_blank">
                <label for="argument">Argument1:</label>
                <input type="text" id="argument1" name="argument1"><br>
                <label for="argument2">Argument2:</label>
                <input type="text" id="argument2" name="argument2"><br>
                <label for="argument3">Argument3:</label>
                <input type="text" id="argument3" name="argument3"><br>
                <input type="submit" value="Submit">
                </form>
                

            </body>
        </html>"""
    return html

def parse_params(part):
    parameters = {}
    for piece in part.split(" "):
        if "/?" in piece:
            piece = piece.replace("/?", "")
            amp_split = piece.split("&")
            for param_set in amp_split:
                eq_split = param_set.split("=")
                parameters[eq_split[0]] = eq_split[1]
                print(parameters)
    return parameters

def server(my_ip="", my_port=80):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((f'{my_ip}', my_port))
    s.listen(1)
    print("\nstarting server")
    print(f"http://{my_ip}/\n")
    while True:
        try:
            if gc.mem_free() < 102000:
                gc.collect()
            conn, addr = s.accept()
            conn.settimeout(3.0)
            print(f'\nGot a connection from {str(addr)}', '\n')
            request = conn.recv(1024)
            conn.settimeout(None)
            request = str(request).replace("b'","").replace("'","")
            request = request.split("\\r\\n")
            
            for part in request:
                print(part)

            for part in request:
                if "/?" and "GET" in part:
                    params = parse_params(part)
            
            if params:
                print(f"Params: {params}\n")
            
            response = page_data()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        except OSError as e:
            conn.close()
            print('Connection closed\n')


network_name = "newWIFI"
network_password = "gazkiX-poctyj-6kezny"

connection = network_connect(network_name, network_password)

if connection:
    my_ip = connection
    my_port = 80
    server(my_ip, my_port)
 