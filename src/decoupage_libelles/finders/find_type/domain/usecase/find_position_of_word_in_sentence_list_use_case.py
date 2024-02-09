from typing import List


class FindPositionOfWordInSentenceListUseCase:
    def execute(
            sentence_list: List[str],
            position_of_first_letter_of_word: int
            ) -> int:
        start = 0
        for i, word in enumerate(sentence_list):
            if start == position_of_first_letter_of_word:
                position_word_in_sentence_list = i
                break
            else:
                start += len(word) + 1
        return position_word_in_sentence_list
