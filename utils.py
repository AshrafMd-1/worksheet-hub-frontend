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
        return chr(ord(roll[8]) + 1) + "0"
    elif roll[8] == "Z":
        return roll[:8] + "00"


def bulk_rolls(from_roll, to_roll):
    from_roll = from_roll.upper()
    to_roll = to_roll.upper()
    roll = []
    current_roll = from_roll

    while current_roll != next_roll(to_roll) and len(roll) <= 20:
        roll.append(current_roll)
        current_roll = next_roll(current_roll)

    return roll


def search_bulk_worksheet(rolls, sem, sub, week):
    pdf_urls = []
    for roll in rolls:
        pdf_url = search_specific_worksheet(roll, sem, sub, week)
        if pdf_url:
            pdf_urls.append([roll, pdf_url])
        else:
            pdf_urls.append([roll, "Not found"])
    if len(pdf_urls) == 0:
        return None
    else:
        return pdf_urls
