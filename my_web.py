from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import  urlparse, parse_qs
import json

# Для начала определим настройки запуска
hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети

class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    def __get_index(self): # делает главную
        with open('index.html') as file:
            content = file.read()
        return content


    def do_GET(self): # делает гет запрос выполняется когда перехожу на сайт
        """ Метод для обработки входящих GET-запросов """
        query_components= parse_qs(urlparse(self.path).query)
        page_address = query_components.get('page')
        page_content=self.__get_index()
        if page_address:
            page_content = self.__get_blog_article(page_address[0])
        self.send_response(200) # Отправка кода ответа
        self.send_header("Content-type", "text/html") # Отправка типа данных, который будет передаваться
        self.end_headers() # Завершение формирования заголовков ответа
        self.wfile.write(bytes(page_content, 'utf-8')) # Тело ответа


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрам в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

        # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")