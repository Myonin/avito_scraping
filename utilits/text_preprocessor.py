def clean_text(input_text):
    input_text = input_text.str.lower()
    input_text = input_text.str.replace(r'[0-9]+', ' ')
    input_text = input_text.str.replace(r'[^a-z- ]+', ' ')
    input_text = input_text.str.replace(r' +', ' ')
    input_text = input_text.str.replace(r'^ ', '')
    input_text = input_text.str.replace(r' $', '')
    return input_text

def drop_short_words(input_text):
    return ' '.join([item for item in input_text.split(' ') if len(item) > 1])
