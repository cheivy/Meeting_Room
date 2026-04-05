import random
import string

def generate_meeting_id():
    """生成5位无重复字符的会议ID"""
    # 可选字符：大写字母 + 数字（排除容易混淆的字符）
    characters = string.ascii_uppercase + string.digits
    # 排除容易混淆的字符：0, O, 1, I
    characters = characters.replace('0', '').replace('O', '').replace('1', '').replace('I', '')

    # 随机选择5个不重复的字符
    meeting_id = ''.join(random.sample(characters, 5))
    return meeting_id