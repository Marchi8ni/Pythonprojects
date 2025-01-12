import requests

url = "https://raw.githubusercontent.com/arditsulceteaching/hosted_files/main/geo.json"
request = requests.get(url)
json_file = request.json()

print(json_file)
user_input = input('Enter the question ID: ')

for q in json_file:
    question_ID = q['quizzes']['questions']['id']
    city = q['quizzes']['questions']['choices']
    if question_ID == user_input and city == True:
        print(f"The correct answer is: {city}")
