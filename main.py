from http.server import HTTPServer, BaseHTTPRequestHandler
from textanalyzer import TextAnalyzer
import json
import urllib


class RestApiCgi:
    RequestBodyVars = ("text", "analysis")

    def __init__(self, data):
        self.json_data = data
        self.text_analyzer_obj = TextAnalyzer
        self.analysis_options = None

    def convert_to_json(self):
        try:
            return json.dumps(self.text_analyzer_obj.send_json_obj, ensure_ascii=False, indent=4)
        except TypeError:
            return False

    def convert_to_python(self):
        try:
            return json.loads(self.json_data)
        except json.decoder.JSONDecodeError:
            return False

    def handle_request_body(self):
        json_body = {}
        json_body = self.convert_to_python()
        text = json_body.get("text")
        if text == None:
            raise TypeError
        self.text_analyzer_obj = TextAnalyzer(text)
        if "analysis" in json_body.keys():
            self.analysis_options = json_body.get("analysis")
            print("analysis options:", self.analysis_options)
            app = RestApiHandleApps(self.text_analyzer_obj, api_options=self.analysis_options)
        else:
            app = RestApiHandleApps(self.text_analyzer_obj, api_options=None)
        print(self.text_analyzer_obj.send_json_obj)


class RestApiHandleApps:
    def __init__(self, text_analyzer_obj, api_options):
        self.all_options_is_done = False
        self.api_options = api_options
        self.text_analyzer_obj = text_analyzer_obj
        self.__functions = {'wordCount': text_analyzer_obj.wordCount,
                            # if you need to add a new function to rest api you can add a new func to TextAnlyzer class.
                            'letters': text_analyzer_obj.letters,
                            # And you can connect your function with rest system here. your variable names should same as the rest request analysis's array's var names.
                            'longest': text_analyzer_obj.longest,
                            'avgLength': text_analyzer_obj.avgLength,
                            'duration': text_analyzer_obj.duration,
                            'medianWordLength': text_analyzer_obj.medianWordLength,
                            'medianWord': text_analyzer_obj.medianWord,
                            'language': text_analyzer_obj.language,
                            'topfivewords': text_analyzer_obj.topfivewords
                            }
        self.__app_connection()  # private function

    def __app_connection(self):
        if self.api_options:
            for analysis in self.api_options:
                try:
                    self.__functions[analysis]()
                    self.all_options_is_done = True
                except KeyError:
                    self.all_options_is_done = False

        else:
            for all_funs in self.__functions:
                self.__functions[all_funs]()
                self.all_options_is_done = True


class HttpRestServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def send_bad_request(self):
        self.send_response(400, message="Bad Request")
        self.end_headers()

    def do_POST(self):
        print("request path: ", self.path)
        if self.path == '/analyze' or self.path.startswith("/analyze?"):
            if self.get_content_type() == "application/json":
                self.cgi = RestApiCgi(self.get_rfile_data())
                try:
                    self.cgi.handle_request_body()
                    self.send_msg_back(self.cgi.convert_to_json())
                except TypeError:
                    self.send_bad_request()
                except AttributeError:
                    self.send_bad_request()
            else:
                self.send_bad_request()
            del self.cgi
        else:
            self.send_bad_request()

    def get_rfile_data(self):
        content_length = int(self.headers.get("content-length"))
        return self.rfile.read(content_length)  # get data from client

    def send_msg_back(self, json_data):
        self.do_HEAD()
        response = bytes(json_data, 'utf-8')
        self.wfile.write(response)  # send data back to client

    def get_content_type(self):
        return self.headers.get("content-type")


if __name__ == "__main__":
    server_address = ('0.0.0.0', 8000)
    Rest = HTTPServer(server_address, HttpRestServer)
    print("Server started:", server_address)
    try:
        Rest.serve_forever()
    except KeyboardInterrupt:
        Rest.server_close()
