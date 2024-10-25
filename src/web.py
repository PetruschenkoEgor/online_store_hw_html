import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

# Настройки запуска
hostName = "localhost"
serverPort = 8080
url = f"http://{hostName}:{serverPort}"
PATH_TO_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "html", "contacts.html")


class MyServer(BaseHTTPRequestHandler):
    """ Отвечает за обработку запросов от клиентов """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "text/html")  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа
        try:
            with open(PATH_TO_FILE, 'r', encoding='utf-8') as file:
                html_file = file.read()
            self.wfile.write(bytes(html_file, "utf-8"))  # Тело ответа
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(bytes(f"Error: {str(e)}", "utf-8"))

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body)  # Логируем тело запроса
        self.send_response(200)
        self.end_headers()


if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Отправим запрос только в момент запуска сервера
        with open(PATH_TO_FILE, 'r', encoding='utf-8') as file:
            html_file = file.read()

        server_thread = threading.Thread(target=webServer.serve_forever)
        server_thread.start()

        # После запуска сервера отправляем POST-запрос
        response = requests.post(url, data=html_file, timeout=5)  # Отправляем html в body
        print(response.status_code)  # Вывод кода состояния ответа
        print(response.text)
        webServer.serve_forever()

    except KeyboardInterrupt:
        pass
    finally:
        webServer.server_close()
        print("Server stopped.")
