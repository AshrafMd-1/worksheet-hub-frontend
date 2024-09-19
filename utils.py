import requests


def roman_to_digits(roman_numeral):
    roman_to_digit_map = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
    }

    result = 0
    length = len(roman_numeral)

    i = 0
    while i < length:
        current_value = roman_to_digit_map[roman_numeral[i]]
        next_value = roman_to_digit_map[roman_numeral[i + 1]] if i + 1 < length else 0

        if current_value >= next_value:
            result += current_value
            i += 1
        else:
            result += next_value - current_value
            i += 2

    return result


def search_specific_worksheet(roll, sem, sub, week):
    pdf_url = f"https://iare-data.s3.ap-south-1.amazonaws.com/uploads/STUDENTS/{roll}/LAB/SEM{sem}/{sub}/{roll}_week{week}.pdf"
    res = requests.head(pdf_url)
    if res.status_code == 200:
        return pdf_url
    else:
        return None


def next_roll(roll):
    is_number = roll[8:].isdigit()

    if is_number and int(roll[8:]) < 99:
        return roll[:8] + str(int(roll[8:]) + 1).zfill(2)
    elif is_number and int(roll[8:]) == 99:
        return roll[:8] + "A0"
    elif int(roll[9]) < 9:
        return roll[:9] + str(int(roll[9]) + 1)
    elif roll[9] == "9" and roll[8] != "Z":
        return roll[:8] + chr(ord(roll[8]) + 1) + "0"
    elif roll[8] == "Z":
        return roll[:8] + "00"


def bulk_rolls_count(from_roll, to_roll):
    from_roll = from_roll.upper()
    to_roll = to_roll.upper()
    roll = []
    current_roll = from_roll

    while current_roll != next_roll(to_roll) and len(roll) <= 40:
        roll.append(current_roll)
        current_roll = next_roll(current_roll)

    if roll[-1].upper() == to_roll.upper():
        return {
            "status": "not exceeded",
        }
    else:
        return {
            "status": "exceeded",
            "roll": roll[-1].upper()
        }


def search_bulk_worksheet_v2(roll_f, roll_l, sem, sub, week):
    pdf_url = f"https://arorium.pythonanywhere.com/bulk"
    payload = {
        "roll_f": roll_f,
        "roll_l": roll_l,
        "sem": sem,
        "sub": sub,
        "week": week
    }
    res = requests.post(pdf_url, json=payload)
    if res.status_code == 200:
        return res.json()
    else:
        return None


def roll_to_number(roll):
    if roll.isdigit():
        return int(roll)
    else:
        return (ord(roll[0]) - 64) * 10 + int(roll[1])


def check_roll_range_validity(roll_f, roll_l):
    roll_f = roll_f.upper()[8:]
    roll_l = roll_l.upper()[8:]
    roll_count = [roll_to_number(roll_f), roll_to_number(roll_l)]
    if roll_count[0] > roll_count[1]:
        return False
    else:
        return True
