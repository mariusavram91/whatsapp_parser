import re
"""
17/05/2018, 22:18 - Person1: IMG-1.jpg (file attached)
17/05/2018, 22:18 - Person2: IMG-2.jpg (file attached)

18/05/2018, 10:03 - Person1: Blah blah bleh
18/05/2018, 10:03 - Person2: Blah bleh blah!
"""


class Messages:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        messages = []
        with open(self.file_path, 'r') as f:
            messages = f.read().splitlines()

        return messages


class Message:
    def __init__(self, date, time, sender, content):
        self.date = date
        self.time = time
        self.sender = sender
        self.content = content

    def __str__(self):
        return self.date + ' ' + self.time + ' ' + \
            self.sender + ' ' + self.content


class Parser:
    def __init__(self, messages=None):
        self.messages = messages

    def is_start_message_line(self, line):
        text_pattern = re.compile(
            "^\d{1,2}\/\d{1,2}\/\d{1,4},\s\d{1,2}:\d{1,2}\s-\s.*:\s"
        )
        return text_pattern.match(line)

    def parse(self):
        messages_data = []

        for line in self.messages:
            if self.is_start_message_line(line):
                message_data, sep, content = line.partition(": ")
                date, sep, extra = message_data.partition(" ")
                date = date.replace(',', '')
                time, sep, sender = extra.partition(" - ")

                message = Message(date, time, sender, content)
                messages_data.append(message)
            elif line:
                # Append new line to last message's content
                messages_data[-1].content += ' ' + line

        return messages_data

    def clean_content(self, parsed_messages):
        for message in parsed_messages:
            attachment = re.compile('IMG-.*\(file attached\)')
            new_content = attachment.sub(' ', message.content).strip()

            url = re.compile('http[s]?:\/\/.*')
            new_content = url.sub(' ', new_content).strip()

            only_words = re.compile('\W+')
            new_content = only_words.sub(' ', new_content).strip()

            message.content = new_content

        # No need for messages with empty content
        parsed_messages = [message for message in parsed_messages if
                           message.content]

        return parsed_messages


class Data:
    def __init__(self, messages):
        self.messages = messages

    def words_count(self):
        total_count = 0

        for message in self.messages:
            total_count += len(message.content.split())

        return total_count


def main():
    messages = Messages('./example.txt').read()

    parser = Parser(messages)
    parsed_messages = parser.parse()
    clean_messages = parser.clean_content(parsed_messages)

    for message in clean_messages:
        print(message.content)

    data = Data(clean_messages)
    print(data.words_count())

if __name__ == "__main__":
    main()