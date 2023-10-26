from hangulize import hangulize


class Hanguel:

    # transform user's input into hangulized word
    def generate_hanguel(lang, user):
        lang = lang
        user = user
        quest = hangulize(user, lang)

        return quest