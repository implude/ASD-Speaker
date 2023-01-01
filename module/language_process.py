from multiprocessing.resource_sharer import stop


wake_up_word_list = ['세리', '쎄리', '새리', "쌔리",]
study_mode_word_list = ["공부모드", "공부 모드", "공부 모두"]

start_word_list = ["시작", "스타트", "틀어", "켜", "재생"]
stop_word_list = ["그만", "멈춰", "중지", "종료", "꺼"]

white_noise_word_list = ["백색소음", "백색 소음"]
volume_word_list = ["볼륨", "음량", "소리"]

led_word_list = ["불", "빛", "등", "조명", "전등", "엘이디", "LED", "led"]

decrease_word_list = ["낮춰", "줄여", "낮추어", "낮혀", "낮게"]
increase_word_list = ["높여", "키워", "올려", "높혀", "높게"]

change_word_list = ["바꿔", "다음", "변경", "딴", "다른"]


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

def is_start_word(text):
    for i in start_word_list:
        if i in text:
            return True
    return False

def is_stop_word(text):
    for i in stop_word_list:
        if i in text:
            return True
    return False

def is_white_noise(text):
    for i in white_noise_word_list:
        if i in text:
            return True
    return False

def is_volume(text):
    for i in volume_word_list:
        if i in text:
            return True
    return False

def is_led(text):
    for i in led_word_list:
        if i in text:
            return True
    return False

def is_decrease_word(text):
    for i in decrease_word_list:
        if i in text:
            return True
    return False

def is_increase_word(text):
    for i in increase_word_list:
        if i in text:
            return True
    return False

def is_change_word(text):
    for i in change_word_list:
        if i in text:
            return True
    return False
