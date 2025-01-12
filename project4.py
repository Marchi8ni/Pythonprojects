import requests

url = "https://raw.githubusercontent.com/arditsulceteaching/hosted_files/main/geo.json"
request = requests.get(url)
json_file = request.json()

print(json_file)
user_input = input('Enter the question ID: ')

for quiz in json_file['quizzes']:
    for quest in quiz['questions']:
        questions_list = quest['id']
        city = quest['choices']
        if str(questions_list) == user_input:
            for choice, is_True in city.items():
                if is_True:
                    print(f"The correct answer is: {choice}")
