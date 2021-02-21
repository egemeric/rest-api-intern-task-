import re


class TextAnalyzer:

    def __init__(self, text):
        self.send_json_obj = {}
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
        self.med_word = word_count[int(len(word_count) / 2)][0]
        return self.med_word

    def language(self):
        self.__language()
        self.send_json_obj.update({"language": self.lng})
        pass

    def __language(self):
        guess_obj = LanguageGuess(self.words,
                                  len(self.word_dict))  # send  initial words and total words count without repetition
        if guess_obj.score > 10:
            self.lng = "EN"
        else:
            self.lng = "TR"

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

    def __get_word_dict(self):
        self.word_dict = list(set(self.words).union(self.words))

    def __create_zero_word_dict_values(self, a_word_dict):  # creates text's dictionary with zero key values
        text_word_dict = dict()
        for i in a_word_dict:
            text_word_dict.update({i: 0})
        return text_word_dict

    def __sort_text_dict_values(self, a_text_dict):
        return sorted(a_text_dict.items(), key=lambda a: a[1], reverse=True)

    def __find_texts_word_ct(self, a_dict):
        length_by_word = self.__create_zero_word_dict_values(a_dict)
        for i in self.words:
            length_by_word.update({i: len(i)})
        return length_by_word


start_eng_keywords = {"am", "is", "are", "did", "I", "am", "we", "they", "them",
                      "It", "on", "in", "the", "to", "he", "she", "my", "her", "his",
                      "our", "us", "what", "why", "when", "much", "many"
                      }  # if the sent text eng score > 10 these values are updated by LanguageGuess


class LanguageGuess:
    global start_eng_keywords
    learned_eng_keywords = set()
    score_table = {}

    def __init__(self, words, total_words):
        self.start_eng_keywords = start_eng_keywords
        self.__words_initial = words  # initial words
        self.__total_words_initial = total_words  # total words without repetition
        self.__create_score_table()  # create initial score table
        self.__guess_eng_lang()  # match words with start_eng_words
        self.__calc_score()  # calc occurrence
        self.__update_learned_eng_words()  # hypothetically all entered text is grammatically true

    def __create_score_table(self):
        print("Eng dictionary", self.start_eng_keywords)
        for i in self.start_eng_keywords:
            self.score_table.update({i: 0})

    def __guess_eng_lang(self):
        for i in self.__words_initial:
            score = self.score_table.get(i)
            if score is not None:
                self.score_table.update({i: score + 1})

    def __update_learned_eng_words(self):
        global start_eng_keywords
        if self.score > 10:  # if score is gr than 10 text is eng
            for i in self.__words_initial:
                self.learned_eng_keywords.add(i)
            start_eng_keywords = self.start_eng_keywords.union(self.learned_eng_keywords)
            print("learned eng keywords len:", len(self.learned_eng_keywords))
        print("Eng Score", self.score)

    def __calc_score(self):
        score = 0
        for i in self.score_table.values():
            score += i
        self.score = score / self.__total_words_initial * 100
        return self.score
