from multiprocessing.resource_sharer import stop


wake_up_word_list = ['세리', '쎄리', '새리', "쌔리", '쉐리', '세이', '시리', '체리', '캐리', '혜리', '세력']
study_mode_word_list = ["공부모드", "공부 모드", "공부 모두"]

start_word_list = ["시작", "스타트", "틀어", "켜", "재생"]
stop_word_list = ["그만", "멈춰", "중지", "종료", "꺼"]



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
    if "백색소음" in text or "백색 소음" in text:
        return True
    return False

def is_volume(text):
    if "볼륨" in text or "음량" in text or "소리" in text:
        return True
    return False

def is_led(text):
    if "불" in text or "빛" in text or "등" in text or "조명" in text or "전등" in text or "전구" in text or "엘이디" in text or "LED" in text or "led" in text:
        return True
    return False

def is_decrease_word(text):
    if "낮춰" in text or "줄여" in text or "낮추어" in text or "낮혀" in text or "낮게" in text:
        return True
    return False

def is_increase_word(text):
    if "높여" in text or "키워" in text or "올려" in text or "높혀" in text or "높게" in text:
        return True
    return False

def is_change_word(text):
    if "바꿔" in text or "다음" in text or "변경" in text or "딴" in text or "다른" in text:
        return True
    return False