from typing import List


class FindPositionsOfWordInSentenceStrUseCase:
    def execute(self, sentence: str, word_to_find: str) -> List[int]:
        sentence_without_space = ('').join(sentence.split(' '))
        positions_of_first_letter_of_word = []
        index = sentence_without_space.find(word_to_find)

        while index != -1:
            positions_of_first_letter_of_word.append(index)
            index = sentence_without_space.find(word_to_find, index + 1)

        return positions_of_first_letter_of_word
