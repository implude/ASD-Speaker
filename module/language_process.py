wake_up_word_list = ['세리', '쎄리', '새리', "쌔리", '쉐리', '세이']
study_mode_word_list = ["공부모드", "공부 모드", "공부 모두"]



def is_wake_up_word(text):
    for i in wake_up_word_list:
        if i in text:
            return True
    return False

def is_study_mode(text):
    for i in study_mode_word_list:
        if i in text:
            return True
    return False
    