wake_up_word_list = ['세리', '쎄리', '새리', "쌔리", '쉐리', '세이']



def is_wake_up_word(text):
    for i in wake_up_word_list:
        if i in text:
            return True
    return False
    