def save_banned_words(words):
    with open('banned_words.txt', 'w') as file:
        for word in words:
            file.write(f'{word}\n')
        print(f"saved {len(words)} banned words")

def load_banned_words():
    with open('banned_words.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]
