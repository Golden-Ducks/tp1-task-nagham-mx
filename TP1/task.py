import re
numtowords = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
    6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
    11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen",
    15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen",
    19: "Nineteen", 20: "Twenty", 30: "Thirty", 40: "Forty",
    50: "Fifty", 60: "Sixty", 70: "Seventy", 80: "Eighty",
    90: "Ninety",100:"hundred"}
def cleaningfunction(text):
    text = text.replace("\n", " ")
    cleaned = ""
    symbols = "@#$^&*()[]{}<>~+=|/"
    punctuation = ".,;:!?\"'"
    i = 0
    while i < len(text):
        char = text[i]
        if char.isalnum() or char == " ":
            cleaned += char
        elif char in symbols:
            pass
        elif char.isalnum():
            cleaned += char
            #here we replace punctuaion with a space 
        i += 1
    cleaned = " ".join(cleaned.split())
    return cleaned.lower()

def number_into_word(number):
    try:
        return numtowords[number]
    except KeyError:
        try:
            tens = number - number % 10
            ones = number % 10
            return numtowords[tens] + " " + numtowords[ones].lower()
        except KeyError:
            return ""
def convert_num(text):
    i = 0
    result = ""
    while i < len(text):
        if text[i].isdigit():
            num = ""
            while i < len(text) and text[i].isdigit():
                num += text[i]
                i += 1
            if num:
                word_value = number_into_word(int(num))
                result += word_value
        else:
            result += text[i]
            i += 1
    return result.lower()
def decontracted(text):
    text = re.sub(r"won'\t", "will not", text)
    text = re.sub(r"'ve", " have", text)
    text = re.sub(r"'s", " is", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"'re", " are", text)
    text = re.sub(r"'m", " am", text)
    text = re.sub(r"can'\t", "can not", text)
    
    return text
def normalise_text(text):
    text = cleaningfunction(text)
    
    text = convert_num(text)
    text = decontracted(text)
    return text
# Test examples
text1 = "Today she Cooked 1 bourek. Later, she addedd two chamiyya, no pizza, and one tea   "
text2 = "Five pizza were ready, but 3 bourak burned!"
text3 = "We only had 8 chamiyya, no pizza, and one tea"
text4 = "is 6 too much? i ate nine bourak lol"
print(normalise_text(text1))
print(normalise_text(text2))
print(normalise_text(text3))
print(normalise_text(text4))