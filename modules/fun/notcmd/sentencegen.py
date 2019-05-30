# Gold Experience - Discord bot
# Copyright (C) 2019 Giovata
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

# modules/fun/notcmd/sentencegen.py

# I apologise for how messy this is.
# I wrote that first sentence about a year ago
# But I still plan to redo this in the future. 

import random

class Adjective:

    def __init__(self, adjective):
        self.adj = adjective

    def get(self):
        intensifiers = ["very", "very", "quite", "somewhat", "really", "slightly", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
        intensifier = intensifiers[random.randint(0, len(intensifiers)-1)]
        if intensifier == "-":
            return self.adj
        else:
            return intensifier + " " + self.adj

class Name:

    def __init__(self, name):
        self.name = name

class Noun:

    def __init__(self, singular, plural):
        self.singular = singular
        self.plural = plural

class Be:

    def __init__(self):
        self.object_setting = "-b"
        self.is_be = True


    @staticmethod
    def conjugate(tense, person, count):
        if tense == "present":
            if person == 1:
                if count == "singular":
                    return "am"
                elif count == "plural":
                    return "are"
            elif person == 2:
                return "are"
            elif person == 3:
                if count == "singular":
                    return "is"
                elif count == "plural":
                    return "are"
        elif tense == "past":
            if person == 1:
                if count == "singular":
                    return "was"
                elif count == "plural":
                    return "were"
            elif person == 2:
                return "were"
            elif person == 3:
                if count == "singular":
                    return "was"
                elif count == "plural":
                    return "were"
        elif tense == "future":
            return "will be"
        elif tense == "present prog":
            return be.conjugate("present", person, count) + " being"
        elif tense == "past prog":
            return be.conjugate("past", person, count) + " being"
        elif tense == "future prog":
            return "will be being"
        elif tense == "present perfect":
            return have.conjugate("present", person, count) + " been"
        elif tense == "past perfect":
            return have.conjugate("past", person, count) + " been"
        elif tense == "future perfect":
            return "will have been"

be = Be()

class Verb:

    def __init__(self, present, present_tps, past, past_part, present_part, object_setting):
        self.present = present
        self.present_tps = present_tps
        self.past = past
        self.past_part = past_part
        self.present_part = present_part
        self.object_setting = object_setting
        self.is_be = False
        self.singular = "-"
        self.plural = present_part

    def conjugate(self, tense, person, count):
        if tense == "present":
            if person == 3 and count == "singular":
                return self.present_tps
            else:
                return self.present
        elif tense == "past":
            return self.past
        elif tense == "future":
            return "will " + self.present
        elif tense == "present prog":
            return be.conjugate("present", person, count) + " " + self.present_part
        elif tense == "past prog":
            return be.conjugate("past", person, count) + " " + self.present_part
        elif tense == "future prog":
            return "will be " + self.present_part
        elif tense == "present perfect":
            return have.conjugate("present", person, count) + " " + self.past_part
        elif tense == "past perfect":
            return have.conjugate("past", person, count) + " " + self.past_part
        elif tense == "future perfect":
            return "will have " + self.past_part

have = Verb("have", "has", "had", "had", "having", "-d")

def get_adjectives(adj_file):
    with open(adj_file, "r") as f:
        list = []
        for adj in f:
            list.append(adj.replace("\n", ""))
        return list

def get_nouns(noun_file):
    with open(noun_file, "r") as f:
        list = []
        for noun in f:
            variants = noun.split(" ")
            templist = []
            for variant in variants:
                templist.append(variant.replace("\n", ""))
            list.append(templist)
        return list

def get_names(name_file):
    with open(name_file, "r") as f:
        list = []
        for name in f:
            list.append(name.replace("\n", ""))
        return list

def get_verbs(verb_file):
    with open(verb_file, "r") as f:
        list = []
        for verb in f:
            variants = verb.split(" ")
            templist = []
            for variant in variants:
                templist.append(variant.replace("\n", ""))
            list.append(templist)
        return list

def add_nouns(noun_file, nouns):
    raw = get_nouns(noun_file)
    for noun in raw:
        nouns.append(Noun(noun[0], noun[1]))

def add_adjectives(adj_file, adjectives):
    raw = get_adjectives(adj_file)
    for adj in raw:
        adjectives.append(Adjective(adj))

def add_names(name_file, names):
    raw = get_adjectives(name_file)
    for name in raw:
        names.append(Name(name))

def add_verbs(verb_file, verbs):
    raw = get_verbs(verb_file)
    verbs.append(be)
    for verb in raw:
        verbs.append(Verb(verb[0], verb[1], verb[2], verb[3], verb[4], verb[5]))

def get_clause(dictionary_path):

    noun_file = dictionary_path + "/nouns.txt"
    verb_file = dictionary_path + "/verbs.txt"
    adj_file = dictionary_path + "/adjectives.txt"
    name_file = dictionary_path + "/names.txt"

    names = []
    nouns = []
    verbs = []
    adjectives = []

    add_names(name_file, names)
    add_nouns(noun_file, nouns)
    add_verbs(verb_file, verbs)
    add_adjectives(adj_file, adjectives)

    tenses = ["present", "present", "present", "past", "past", "future", "future", "present prog", "past prog", "future prog", "present perfect", "past perfect", "future perfect"]
    persons = [3, 3, 3, 3, 3, 3, 2, 1]
    counts = ["singular", "plural"]
    adjs = [True, True, False, False, False, False, False, False, False]
    isNames = [True, False, False, False, False, False, False, False, False]

    subjectNoun = ""
    verb = ""
    objectNoun = ""

    tense = tenses[random.randint(0, len(tenses)-1)]
    person = persons[random.randint(0, len(persons)-1)]
    count = counts[random.randint(0, len(counts)-1)]

    def get_noun_phrase(count, person, be):

        noun_phrase = ""
        if be:
            noun_phrase = adjectives[random.randint(0, len(adjectives)-1)].get_adj()
        elif count == "singular":
            if person == 3:
                articles = ["a", "the", "the"]
                article = articles[random.randint(0, len(articles)-1)]
                valid_noun = False
                noun = "" 
                while valid_noun == False:
                    noun = nouns[random.randint(0, len(nouns)-1)]
                    if noun.singular != "-":
                        valid_noun = True
                noun_phrase = noun.singular
                adj = adjs[random.randint(0, len(adjs)-1)]
                if adj:
                    adjective = adjectives[random.randint(0, len(adjectives)-1)]
                    noun_phrase = adjective.get() + " " + noun_phrase
                if article == "a" and noun_phrase[0] in "aeiouAEIOU":
                    article = "an"
                noun_phrase = article + " " + noun_phrase
                isName = isNames[random.randint(0, len(isNames)-1)]
                if isName:
                    name = names[random.randint(0, len(names)-1)]
                    noun_phrase = name.name

            elif person == 1:
                if case == "subject":
                    noun_phrase = "I"
                elif case == "object":
                    noun_phrase = "me"
            elif person == 2:
                noun_phrase = "you"
        elif count == "plural":
            if person == 3:
                articles = ["some", "the", "the", "-", "-", "-"]
                article = articles[random.randint(0, len(articles)-1)]
                noun = nouns[random.randint(0, len(nouns)-1)]
                noun_phrase = noun.plural
                adj = adjs[random.randint(0, len(adjs)-1)]
                if adj:
                    adjective = adjectives[random.randint(0, len(adjectives)-1)]
                    noun_phrase = adjective.get() + " " + noun_phrase
                if noun.singular == "-":
                    count = "singular"
                if article != "-":
                    noun_phrase = article + " " + noun_phrase
            elif person == 1:
                if case == "subject":
                    noun_phrase = "we"
                elif case == "object":
                    noun_phrase = "us"
            elif person == 2:
                noun_phrase = "you"

        return noun_phrase

    case = "subject"
    subjectNoun = get_noun_phrase(count, person, False)
    verb = verbs[random.randint(0, len(verbs)-1)]

    verbPhrase = verb.conjugate(tense, person, count)
    sentence_format = "{s} {v}"
    be = False

    if verb.object_setting == "-a":
        sentence_formats = ["{s} {v}", "{s} {v} {o}", "{s} {v} {o}", "{s} {v} {o}", "{s} {v} {o}"]
        sentence_format = sentence_formats[random.randint(0, len(sentence_formats)-1)]
    elif verb.object_setting == "-b":
        if verb.is_be and random.randint(0, 100) > 60:
            be = True
            sentence_format = "{s} {v} {a}"
        else:
            sentence_format = "{s} {v} {o}"

    adjective = ""
    objectNoun = ""

    if sentence_format == "{s} {v} {o}":
        case = "object"
        person = persons[random.randint(0, len(persons)-1)]
        count = counts[random.randint(0, len(counts)-1)]
        objectNoun = get_noun_phrase(count, person, be)

    elif sentence_format == "{s} {v} {a}":
        adjective = adjectives[random.randint(0, len(adjectives)-1)].get()

    clause = sentence_format.format(s=subjectNoun, v=verbPhrase, o=objectNoun, a=adjective)

    return clause

def get_sentence(dictionary_path):
    
    clause = get_clause(dictionary_path)
    sentence = clause

    if random.randint(0, 100) > 95:

        connectives = [" and ", " but ", ", although ", ". However, ", " so ", ", so ", " because ", " and therefore ", ". Also, "]
        connective = connectives[random.randint(0, len(connectives)-1)]

        sentence = sentence + connective + get_clause(dictionary_path)

    punctuations = [".", ".", ".", ".", ".", ".", "...", "!", "?", "...", "!", "?", "... :thinking:", "? :thinking:", "! :ok_hand:"]
    punctuation = punctuations[random.randint(0, len(punctuations)-1)]

    sentence = sentence[0].upper() + sentence[1:] + punctuation
    sentence = sentence.replace("%s", " ")
    
    return sentence

if __name__ == "__main__":
    get_sentence(input("Enter full dictionary path: "))