from Bot import *
import dotenv

dotenv.load_dotenv()

questions_file = open("evaluation/questions.txt", "r", encoding="utf-8")
answers_file = open("evaluation/answers.txt", "w", encoding="utf-8")

chatbot = Bot()

index = 1
errors = 0
hits = 0
for question in questions_file:
    response = chatbot.get_reponse(question, [])
    answers_file.write(f"Question {index}:\n{question}\nAnswer {index}:\n{response}\n#####################\n")
    print(f"Answered question {index}")
    response = response.lower()
    if "não sei" in response or "não sei." in response or "não há informações" in response:
        errors += 1
    else:
        hits += 1
    index += 1

answers_file.write(f"Errors: {errors}\nHits: {hits}\n")
answers_file.write(f"Accuracy: {hits/(hits+errors)}")
print(f"Errors: {errors}")
print(f"Hits: {hits}")
questions_file.close()
answers_file.close()