import re
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
        pass

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