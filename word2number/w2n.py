from __future__ import print_function
import re

THOUSAND = []
MILLION = []
BILLION = []
POINT = []

spanish_number_system = {
    'cero': 0,
    'uno': 1,
    'dos': 2,
    'tres': 3,
    'cuatro': 4,
    'cinco': 5,
    'seis': 6,
    'siete': 7,
    'ocho': 8,
    'nueve': 9,
    'diez': 10,
    'once': 11,
    'doce': 12,
    'trece': 13,
    'catorce': 14,
    'quince': 15,
    'dieciseis': 16,
    'diecisiete': 17,
    'dieciocho': 18,
    'diecinueve': 19,
    'veinte': 20,
    'veintiuno': 21,
    'veintidos': 22,
    'veintitres': 23,
    'veinticuatro': 24,
    'veinticinco': 25,
    'veintiseis': 26,
    'veintisiete': 27,
    'veintiocho': 28,
    'veintinueve': 29,
    'treinta': 30,
    'cuarenta': 40,
    'cincuenta': 50,
    'sesenta': 60,
    'setenta': 70,
    'ochenta': 80,
    'noventa': 90,
    'cien': 100,
    'ciento': 100,
    'cientos': 100,
    'doscientos': 200,
    'trescientos': 300,
    'cuatrocientos': 400,
    'quinientos': 500,
    'seiscientos': 600,
    'setecientos': 700,
    'ochocientos': 800,
    'novecientos': 900,
    'mil': 1000,
    'millones': 1000000,
    'mil-millones': 1000000000,
    'coma': '.'
}

spanish_decimal_words = ['cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve']

american_number_system = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000,
    'point': '.'
}

american_decimal_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def number_formation(number_words, number_system):
    """
    function to form numeric multipliers for million, billion, thousand etc.

    input: list of strings
    return value: integer
    """
    numbers = []
    if not number_words: return 1
    for n, number_word in enumerate(number_words):
        numbers.append(number_system[number_word])
        if n==0 and numbers[-1] >= 100: numbers = [numbers[-1]//100, 100]
    if len(numbers) == 4:
        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
    elif len(numbers) == 3:
        return numbers[0] * numbers[1] + numbers[2]
    elif len(numbers) == 2:
        if 100 in numbers[1:]:
            return numbers[0] * numbers[1]
        else:
            return numbers[0] + numbers[1]
    else:
        return numbers[0]


def get_integer_part(clean_numbers, total_sum, language):

    billion_index = clean_numbers.index(language.BILLION) if language.BILLION in clean_numbers else -1
    million_index = clean_numbers.index(language.MILLION) if language.MILLION in clean_numbers else -1
    thousand_index = clean_numbers.index(language.THOUSAND) if language.THOUSAND in clean_numbers else -1

    if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) or (million_index>-1 and million_index < billion_index):
        raise ValueError("Malformed number! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    if len(clean_numbers) > 0:
        # hack for now, better way TODO
        if len(clean_numbers) == 1:
                total_sum += language.number_system[clean_numbers[0]]
        else:
            if billion_index > -1:
                billion_multiplier = number_formation(clean_numbers[0:billion_index], language.number_system)
                total_sum += billion_multiplier * 1000000000

            if million_index > -1:
                if billion_index > -1:
                    million_multiplier = number_formation(clean_numbers[billion_index+1:million_index], language.number_system)
                else:
                    million_multiplier = number_formation(clean_numbers[0:million_index], language.number_system)
                total_sum += million_multiplier * 1000000

            if thousand_index > -1:
                if million_index > -1:
                    thousand_multiplier = number_formation(clean_numbers[million_index+1:thousand_index], language.number_system)
                elif billion_index > -1 and million_index == -1:
                    thousand_multiplier = number_formation(clean_numbers[billion_index+1:thousand_index], language.number_system)
                else:
                    thousand_multiplier = number_formation(clean_numbers[0:thousand_index], language.number_system)
                total_sum += thousand_multiplier * 1000

            if thousand_index > -1 and thousand_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[thousand_index+1:], language.number_system)
            elif million_index > -1 and million_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[million_index+1:], language.number_system)
            elif billion_index > -1 and billion_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[billion_index+1:], language.number_system)
            elif thousand_index == -1 and million_index == -1 and billion_index == -1:
                hundreds = number_formation(clean_numbers, language.number_system)
            else:
                hundreds = 0
            total_sum += hundreds
        
    return total_sum


def get_decimal_sum(decimal_digit_words, language):
    """
    function to convert post decimal digit words to numerial digits
    input: list of strings
    output: double
    """
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if(dec_word not in language.decimal_words):
            decimal_number_str.append(get_integer_part(decimal_digit_words, 0, language))
            break
        else:
            decimal_number_str.append(language.number_system[dec_word])
    final_decimal_string = '0.' + ''.join(map(str,decimal_number_str))
    return float(final_decimal_string)


def get_individual_digits(clean_numbers, language):
    
    individual_digits = []
    for dec_word in clean_numbers:
        if(dec_word not in language.decimal_words):
            return 0
        else:
            individual_digits.append(language.number_system[dec_word])
    return int(''.join(map(str,individual_digits)))


class Language:
    def __init__(self, number_system, decimal_words):
        self.number_system = number_system
        self.decimal_words = decimal_words
        self.THOUSAND = list(self.number_system.keys())[list(self.number_system.values()).index(1000)]
        self.MILLION = list(self.number_system.keys())[list(self.number_system.values()).index(1000000)]
        self.BILLION = list(self.number_system.keys())[list(self.number_system.values()).index(1000000000)]
        self.POINT = list(self.number_system.keys())[list(self.number_system.values()).index('.')]


def detect_language(number_system, number_sentence):

    for word in number_sentence:
        if word in number_system:
            return True
    return False


def select_language_dictionary(number_sentence):
    
    spanish = detect_language(spanish_number_system, number_sentence)
    english = detect_language(american_number_system, number_sentence)

    if spanish and english:
        raise ValueError("Spanish and English detected. Please, use just one language")
    if not spanish and not english:
        raise ValueError("No valid number words found! Please enter a valid number word (eg. two million twenty three thousand and forty nine)") 

    if spanish:
        return Language(spanish_number_system, spanish_decimal_words)
    if english:
        return Language(american_number_system, american_decimal_words)


def word_to_num(number_sentence):
    """
    function to return integer for an input `number_sentence` string
    input: string
    output: int or double or None
    """
    if type(number_sentence) is not str:
        raise ValueError("Type of input is not string! Please enter a valid number word (eg. \'two million twenty three thousand and forty nine\')")

    number_sentence = number_sentence.replace('-', ' ')
    number_sentence = re.sub('millon($|\s)', 'millones ', number_sentence)
    number_sentence = number_sentence.replace('mil millones', 'mil-millones')
    number_sentence = number_sentence.lower()  # converting input to lowercase

    if(number_sentence.isdigit()):  # return the number if user enters a number string
        return int(number_sentence)

    split_words = number_sentence.strip().split()  # strip extra spaces and split sentence into words

    # Select language
    language = select_language_dictionary(split_words)
    
    clean_numbers = []
    clean_decimal_numbers = []

    # removing and, & etc.
    for word in split_words:
        if word in language.number_system:
            clean_numbers.append(word)

    # Error if user enters million,billion, thousand or decimal point twice
    if clean_numbers.count(language.THOUSAND) > 1 or clean_numbers.count(language.MILLION) > 1 or clean_numbers.count(language.BILLION) > 1 or clean_numbers.count(language.POINT)> 1:
        raise ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    # if we only have single numbers
    if all(ele in language.decimal_words for ele in clean_numbers):
        return get_individual_digits(clean_numbers, language)

    # separate decimal part of number (if exists)
    if clean_numbers.count(language.POINT) == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index(language.POINT)+1:]
        clean_numbers = clean_numbers[:clean_numbers.index(language.POINT)]

    total_sum = 0

    # integer part
    total_sum = get_integer_part(clean_numbers, total_sum, language)

    # adding decimal part to total_sum (if exists)
    if len(clean_decimal_numbers) > 0:
        decimal_sum = get_decimal_sum(clean_decimal_numbers, language)
        total_sum += decimal_sum

    return total_sum



if __name__ == "__main__":
    word_to_num("nueve coma novecientos noventa y nueve")