numbers_dict = {
    "1":"one",
    "2":"two",
    "3":"three",
    "4":"four",
    "5":"five",
    "6":"six",
    "7":"seven",
    "8":"eight",
    "9":"nine",
    "10":"ten",
}

docs_dict = {
    "D1":"Today she cooked 4 bourak. Later, she added two chamiyya and 1 pizza.",
    "D2":"Five pizza were ready, but 3 bourak burned!",
    "D3":"We only had 8 chamiyya, no pizza, and one tea.",
    "D4":"Is 6 too much? I ate nine bourak lol.",
}

punctuation =  ".,!?;:'\"-()[]"

def normalize(txt):
    txt = txt.lower()

    for char in punctuation:
        txt = txt.replace(char,"")
    
    for digit, word in numbers_dict.items():
        txt = txt.replace(digit,word)
    
    return txt

for key, value in docs_dict.items():
    print(f"{key} original: {value}")
    print(f"{key} normalized: {normalize(value)}")



#     line 24
# Use string.punctuation
# import the string module to avoid typing out punctuation manually
    
#     line 27
# avoid using .replace() inside a loop.. it creates a new string every time
# No need for iterating over the entire text too many times, just use a single loop for characters
    
#     line 11
# your numbers_dict is missing "0"
