from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib, re


class TextAnalyzer:

    def __init__(self, text):
        self.send_json_obj = {}
        print("textttt", text)
        self.words = re.findall(r"\w+", text)
        self.__get_word_dict()  # union the all words (no occurrence)
        self.word_count_dict = self.__find_texts_word_ct(self.word_dict)  # find all words's length
        pass

    def wordCount(self):
        self.__wordCount()
        self.send_json_obj.update({"wordCount": len(self.words)})

    def __wordCount(self):
        self.word_ct = len(self.words)
        return self.word_ct

    def letters(self):
        self.__letters()
        self.send_json_obj.update({"letters": self.letter_ct})

    def __letters(self):
        ct = 0
        for i in self.words:
            ct += len(i)
        self.letter_ct = ct
        return self.letter_ct

    def longest(self):
        self.__longest()
        self.send_json_obj.update({"longest": self.sorted_words_by_length[0][0]})

    def __longest(self):
        self.sorted_words_by_length = self.__sort_text_dict_values(self.word_count_dict)
        return self.sorted_words_by_length

    def avgLength(self):
        self.__avgLength()
        self.send_json_obj.update({"avgLength": self.avg_len})

    def __avgLength(self):
        self.avg_len = self.__letters() / self.__wordCount()
        return self.avg_len

    def duration(self):
        self.__duration()
        self.send_json_obj.update({"duration": self.min_duration})

    def __duration(self):
        self.min_duration = self.__wordCount() / 200 * 60  # https://marketingland.com/estimated-reading-times-increase-engagement-79830
        return self.min_duration  # in seconds

    def medianWordLength(self):
        self.__medianWordLength()
        self.send_json_obj.update({"medianWordLength": self.med_word_ct})

    def __medianWordLength(self):
        meadian_word = self.__medianWord()
        self.med_word_ct = len(meadian_word)
        return self.med_word_ct

    def medianWord(self):
        self.__medianWord()
        self.send_json_obj.update({"medianWord": self.med_word})

    def __medianWord(self):
        word_count = self.__create_zero_word_dict_values(self.words)
        word_count = self.__find_texts_word_ct(self.words)
        word_count = self.__sort_text_dict_values(word_count)
        self.med_word = word_count[int(len(word_count)/2)][0]
        return self.med_word

    def language(self):


    def topfivewords(self):
        word_occurrence = self.__create_zero_word_dict_values(self.word_dict)
        for key in self.words:
            temp = int(word_occurrence.get(key))
            word_occurrence.update({key: temp + 1})
        word_occurrence = self.__sort_text_dict_values(word_occurrence)
        topfive = {'topfivewords': []}
        for temp in word_occurrence[:5]:  # list top five word
            topfive["topfivewords"].append(temp[0])
        self.send_json_obj.update(topfive)
        print("Top 5 words:", topfive)

    def __get_word_dict(self):
        self.word_dict = list(set(self.words).union(self.words))

    def __create_zero_word_dict_values(self, a_word_dict):  # creates text's dictionary with zero key values
        text_word_dict = dict()
        for i in a_word_dict:
            text_word_dict.update({i: 0})
        return text_word_dict

    def __sort_text_dict_values(self, a_text_dict):
        return sorted(a_text_dict.items(), key=lambda a: a[1], reverse= True)

    def __find_texts_word_ct(self,a_dict):
        length_by_word = self.__create_zero_word_dict_values(a_dict)
        for i in self.words:
            length_by_word.update({i: len(i)})
        return length_by_word


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


            else:
                self.send_bad_request()
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
