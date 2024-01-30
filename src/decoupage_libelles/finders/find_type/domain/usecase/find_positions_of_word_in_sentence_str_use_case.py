class FindPositionsOfWordInSentenceStrUseCase:
    def execute(
            sentence: str,
            word_to_find: str
            ):
        positions_of_first_letter_of_word = []
        index = sentence.find(word_to_find)

        while index != -1:
            positions_of_first_letter_of_word.append(index)
            index = sentence.find(word_to_find, index + 1)

        return positions_of_first_letter_of_word