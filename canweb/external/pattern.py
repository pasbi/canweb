#!/usr/bin/env python3

import re

FLAT = "\u266D";
SHARP = "\u266F";
IGNORE_BEFORE_PATTERN = '^(' \
    + "|".join([
            re.escape("("),
            re.escape("["),
            re.escape("{"),
            re.escape("<"),
        ]) \
    + ")*";
IGNORE_AFTER_PATTERN = '(' \
    + "|".join([
            re.escape(")"),
            re.escape("]"),
            re.escape("}"),
            re.escape(">"),
            re.escape(":"),
            "\\(\\w*\\)",
            "\\[\\w*\\]"
        ]) \
    + ")*$";
CHORD_EXTENSION_PATTERN = "^(" \
    + "|".join([ "maj", "min", "2", "4", "5", "7th", "maj7", "min7", "sus4",
                "sus2", "sus", "°", "dim", "dim7", "aug", "6", "min6", "9",
                "min9", "maj9", "11", "min11", "maj11", "13", "min13", "maj13",
                "add9", "maj7th", "7", "b5", re.escape("+")
            ]) \
    + ")*$"

SHIFTER = {
    -1: "^(" + "|".join([ "s(?!us)", "es", "b", FLAT ]) + ")",
     1: "^(" + "|".join([ "is", "#", SHARP ]) + ")"
}
SPLIT_PATTERN = "(" + "|".join(
    list(map(re.escape, ["|", ",", "-", "/", "*", "`", "'"])) + ["\\s"]
    ) + ")+"
WORD_PATTERN = IGNORE_BEFORE_PATTERN + "[a-zA-Z'].*" 

HEADLINE_KEYWORDS = r"(pre|post)?\W*(verse|refrain|chorus|bridge|intro|outro)(\W|[0-9_IVX])*"
HEADLINE_BRACKETS = r"(\[.*\])"
HEADLINE_PATTERN = r"^\W*({}|{})\W*$".format(HEADLINE_KEYWORDS, HEADLINE_BRACKETS)

class Chord:
    def __init__(self, token):
        self.target_length = len(token)
        self.textBefore = ""
        self.textAfter = ""
        self.base = 0
        self.attachment = ""
        self.isValid = False
        self.isMinor = False
        self.parseChord(token)

    def transpose(self, t):
        # https://stackoverflow.com/a/3883019/4248972
        self.base = (self.base + t) % 12
        assert 0 <= self.base < 12

    def parseChord(self, token):
        def getPattern(pattern, token):
            """returns first matching pattern in token or empty string"""
            m = re.search(pattern, token)
            if m is None:
                return ""
            else:
                return m.group(0)

        if token == "":
            self.isValid = False
            return

        self.textBefore = getPattern(IGNORE_BEFORE_PATTERN, token)
        self.textAfter = getPattern(IGNORE_AFTER_PATTERN, token)
        token = token[len(self.textBefore):len(token)-len(self.textAfter)]

        if token == "":
            self.isValid = False
            return

        baseChar = token[0]
        token = token[1:]

        try:
            self.base = { "C": 0, "D": 2, "E": 4, "F": 5,
                "G": 7, "A": 9, "B": 11 }[baseChar.upper()]
        except KeyError:
            self.valid = False
            return

        for direction, pattern in SHIFTER.items():
            m = re.search(pattern, token)
            if m:
                token = token[len(m.group(0)):]
                self.base += direction

        self.transpose(0)

        self.isMinor = False
        if baseChar.islower():
            self.isMinor = True
        m = re.search("^m(?!(in|aj))", token)
        if m:
            token = token[len(m.group(0)):]
            self.isMinor = True

        self.attachment = getPattern(CHORD_EXTENSION_PATTERN, token)
        self.isValid = self.attachment == token

    def key(self):
        key = [ "C", "C"+SHARP, "D", "E"+FLAT, "E", 
                "F", "F"+SHARP, "G", "A"+FLAT, "A", 
                "B"+FLAT, "B" ][self.base]
        if self.isMinor:
            key = key.lower()
        return key

    def toString(self):
        if self.isValid:
            return "".join([ self.textBefore, self.key(),
                self.attachment, self.textAfter ])

    # private static final Pattern WORD_PATTERN = Pattern.compile("^[a-zA-Z'].*");
def split_tokens(line):
    
    tokens = []
    while len(line) > 0:
        m = re.search(SPLIT_PATTERN, line)
        if m is None:
            # no more whitespace left, rest of the line is a chord.
            tokens.append(line)
            break
        else:
            if m.start() == 0:
                w = line[:m.end()]
                tokens.append(w)
            else:
                c = line[:m.start()]
                tokens.append(c)
                w = line[m.start():m.end()]
                tokens.append(w)
            line = line[m.end():]

    def toChordIfValid(token):
        c = Chord(token)
        if c.isValid:
            return c
        else:
            return token

    tokens = list(map(toChordIfValid, tokens))
    return tokens

class Line:
    def __init__(self, line):
        self.tokens = split_tokens(line)
        self.line = line
        preds = {
            "chord": lambda t: type(t) is Chord,
            "word":  lambda t: not preds["chord"](t) and re.match(WORD_PATTERN, t) is not None,
            "space": lambda t: not preds["chord"](t) and re.match(SPLIT_PATTERN, t) is not None,
            "other": lambda t: not preds["chord"](t) and not preds["word"](t) and not preds["space"](t),
        }
        lens = { key: len(list(filter(preds[key], self.tokens))) 
                 for key in preds.keys() }

        self.isChordLine = lens["chord"] + lens["other"] >= lens["word"] and lens["chord"] > 0

    def toString(self, markup, transpose):
        if self.isChordLine:
            def toString(token):
                if type(token) is Chord:
                    token.transpose(transpose)
                    return start_tag + token.toString() + end_tag
                else:
                    return token

            space_account = 0
            line = markup.get("chordline/prefix", "")
            for t in self.tokens:
                if type(t) is Chord:
                    t.transpose(transpose)
                    c = t.toString()
                    space_account += t.target_length - len(c)
                    fill = " " * max(0, space_account)
                    space_account = min(space_account, 0)
                    line += markup.get("chord/prefix", "")
                    line += c
                    line += markup.get("chord/postfix", "")
                    line += fill
                else:
                    # t shall never be empty, else two chords are not separated anymore
                    # remove leading spaces until account is balanced
                    while len(t) > 1 and t[0] == " " and space_account < 0:
                        space_account += 1
                        t = t[1:]
                    line += t
            line += markup.get("chordline/postfix", "")
            return line + markup.get("chordline/linebreak", "\n")
        elif re.match(HEADLINE_PATTERN, self.line, re.IGNORECASE):
            line = ""
            line += markup.get("headline/prefix", "")
            line += self.line
            line += markup.get("headline/postfix", "")
            return line + markup.get("headline/linebreak", "\n")
        else:
            return self.line + markup.get("default/linebreak", "\n")

class Pattern:
    def __init__(self, pattern):
        pattern = pattern.replace("\r\n", "\n")
        self.lines = list(map(Line, pattern.split("\n")))

    def toString(self, markup, transpose):
        return "".join(map(
                    lambda line: 
                        line.toString(markup, transpose),
                    self.lines ))
