import os

import alphabet_generator
import image_utils


def OCR(path):
    """ Return letter """
    image = image_utils.load_file(path)
    image = image_utils.crop_image(image)

    test_data = image_utils.analyze_image(image)
    alphabet_data = alphabet_generator.load_reference_proportions()

    difference = [{'letter': '', 'diff': 0} for letter in range(26)]

    for reference_letter in alphabet_data:
        index_letter = ord(reference_letter['letter']) - alphabet_generator.ASCII_A
        temp_diff = 0

        for x in range(image_utils.SPLIT_NUMBER):
            for y in range(image_utils.SPLIT_NUMBER):
                temp_diff += pow((test_data['subproportions'][x][y] * reference_letter['proportion']
                                  - reference_letter['subproportions'][x][y] * test_data['proportion']), 2)

        difference[index_letter]['letter'] = reference_letter['letter']
        difference[index_letter]['diff'] = temp_diff

    return sorted(difference, key=lambda letter: letter['diff'])[0]['letter']


def test_all_letters(dir):
    for letter in range(26):
        letter += alphabet_generator.ASCII_A
        print(chr(letter), OCR(dir + chr(letter) + ".jpg"))


def read_sentence(dir="Data/Sentence/"):
    """ Read and return sentence from images in Data/Sentence/[number].jpg"""
    result = ""
    length = len(os.listdir(dir))
    for letter in range(length):
        result += OCR(dir + str(letter) + ".jpg")
    return result


# Can be called just once to generate all needed files
alphabet_generator.generate_reference_data()

# To test it on comic sans
alphabet_generator.create_comic()
test_all_letters("Data/Draw/")

print(read_sentence())
