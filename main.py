import json
from difflib import get_close_matches


def load_knowledgge_base(file_patch: str) -> dict:
    try:
        with open(file_patch, 'r') as file:
            data: dict = json.load(file)
            return data
    except FileNotFoundError:
        return {"questions": []}



def save_knowledge_base(file_patch: str, data: dict):
    with open(file_patch, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["questions"] == question:
            return q["answer"]


def chatbot():
    knowledge_base: dict = load_knowledgge_base('knowledge_base.json')

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == "quit":
            break

        best_match: str | None = find_best_match(user_input, [q["questions"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: i dont\'t know the answer. Can you teach me?')
            new_answer: str = input('Type answer or "skip" to skip: ')
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"questions": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learn a new response!')
            else:
                print('Bot: Skipping the addition of a new response.')

if __name__ == '__main__':
    chatbot()
