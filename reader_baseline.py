import openai

openai.api_base = "http://0.0.0.0:8080/v1"

# Enter any non-empty API key to pass the client library's check.
# openai.api_key = "xxx"

# Enter any non-empty model name to pass the client library's check.
completion = openai.ChatCompletion.create(
    model="chatglm-6b",
    messages=[
        {"role": "user", "content": "Hello, Do you know what is ChatGPT?"},
    ],
    stream=False,
)
print(completion.choices[0].message.content)


from typing import List
import json
import sys
import time

# import openai


class GraphGPT:

    def __init__(self, api_key: str, messages: List = None):
        # openai.organization = "org-RirZ5qWBA1aJGRRbjIC3DF6e"
        openai.api_key = "xxx"
        # openai.api_key = "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"
        if messages:
            self.messages = messages
        else:
            self.messages = [
                {"role": "system", "content": "You are an expert in data mining and knowledge graph fact-checking."},
                # {"role": "user", "content": "Please help check the correctness of each triplet by searching information online. Next, I will sequentially provide you with some triplets. If the information described by this triplet is correct, please reply with 'True' and the corresponding basis. If not, please reply with 'False' and the corresponding judgment basis. If you are unsure, please reply with 'not sure'."},
                {"role": "user", "content": "Please help me answer the following questions."},
                 # check the correctness of each triplet by searching from your corpus. Next, I will sequentially provide you with some triplets. If the information described by this triplet is correct, please reply with 'True'. If not, please reply with 'False' and the corresponding judgment basis. If you are unsure, please reply with 'not sure'. Do not reply with any extra words or punctuation."},
                {"role": "assistant", "content": "These questions are common sense questions and are all multiple-choice questions with only one correct answer."}
            ]

    def ask_chat_gpt(self) -> str:
        # response = openai.ChatCompletion.create(
        #     # model="gpt-3.5-turbo",
        #     # model="davinci-002",
        #     # model="text-davinci-002",
        #     model="gpt-4",
        #     messages=self.messages
        # )
        # response_content = response['choices'][0]['message']['content']
        completion = openai.ChatCompletion.create(
            model="chatglm-6b",
            messages=self.messages,
            stream=False,
        )
        return completion.choices[0].message.content

    def train(self, x1: str, y: str):
        self.messages.append({"role": "user", "content": f"'{x1}' is ture or false?"})
        response_content = self.ask_chat_gpt()
        self.messages.append({"role": "assistant", "content": response_content})

        # if 'True.' not in response_content and 'False.' not in response_content and 'Not sure.' not in response_content:
        #     feedback = f"You answered incorrectly. You answered '{response_content}', and the correct answer is '{y}'."
        if 'True.' in response_content:
            if 'True.' == y:
                feedback = "Good job!"
            else:
                feedback = f"You answered incorrectly. You answered '{response_content}', but the correct answer is '{y}'."
        elif 'False.' in response_content:
            if 'False.' == y:
                feedback = "Good job!"
            else:
                feedback = f"You answered incorrectly. You answered '{response_content}', but the correct answer is '{y}'."
        elif 'Not sure.' in response_content:
            if 'Not sure.' == y:
                feedback = "Good job!"
            else:
                feedback = f"You answered incorrectly. You answered '{response_content}', but the correct answer is '{y}'."
        else:
            feedback = "You're answering in the wrong format. If the information described by this triplet is correct, please reply with 'True'. If not, please reply with 'False' and the corresponding judgment basis. If you are unsure, please reply with 'not sure'. Do not reply with any extra words or punctuation."
        # if response_content not in {'True.', 'False.', 'Not sure.'}:
        #     feedback = "You're answering in the wrong format. If the information described by this triplet is correct, please reply with 'True'. If not, please reply with 'False' and the corresponding judgment basis. If you are unsure, please reply with 'not sure'. Do not reply with any extra words or punctuation."
        #
        # elif response_content == y:
        #     feedback = "Good job!"
        # else:
        #     feedback = f"You answered incorrectly. You answered '{response_content}', and the correct answer is '{y}'."
        self.messages.append({"role": "user", "content": feedback})

        print(f"\nCurrent training sample: x1={x1}, y={y}")
        print(f"self.messages=")
        for msg in self.messages:
            print(msg)

    def predict(self, x1: str) -> str:
        # self.messages.append({"role": "user", "content": f"'{x1}' Please directly give me one optimal answer in the form of A/B/C/D/E. Please reply with 'A', 'B', 'C', 'D', or 'E'. Do not reply with any extra words or punctuation."})
        self.messages.append({"role": "user",
                              "content": f"'{x1}' Please directly give me one optimal answer in the form of A/B/C/D. Please reply with 'A', 'B', 'C', or 'D'. Do not reply with any extra words or punctuation."})
        response_content = self.ask_chat_gpt()
        self.messages.pop()
        return response_content

    def save(self, model_path: str):
        model_dict = {
            'messages': self.messages
        }
        with open(model_path, "w", encoding='utf-8') as f:
            json.dump(model_dict, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(self, model_path: str, api_key: str) -> 'GraphGPT':
        with open(model_path, "r", encoding='utf-8') as f:
            model_dict = json.load(f)
            model = GraphGPT(api_key=api_key, messages=model_dict['messages'])
            return model


def load_statement_dict(statement_path):
    all_dict = {}
    with open(statement_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            instance_dict = json.loads(line)
            qid = instance_dict['id']
            label = instance_dict['answerKey']
            all_dict[qid] = {
                'question': instance_dict['question']['stem'],
                'answers': [dic['text'] for dic in instance_dict['question']['choices']],
                'answerKey': label
            }
    return all_dict


if __name__ == '__main__':


    # api_key = "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"
    # api_key = "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"
    # api_key = "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"
    # api_key = "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"
    # api_key = "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"
    api_key = "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"
    # api_key = "048c9d3bdba241a79ad102a381a9c7b3"

    sim_chatgpt = GraphGPT(api_key=api_key)
    print(sim_chatgpt.ask_chat_gpt())

    # for x1, y in train_data:
    #     sim_chatgpt.train(x1, y)
    #
    # sim_chatgpt.save('sim_chatgpt.json')

    sim_chatgpt2 = GraphGPT.load('sim_chatgpt.json', api_key=api_key)

    path = "data/medqa/dev.statement.jsonl"
    dict1 = load_statement_dict(path)
    num_questions = 0
    num_correct = 0

    for key in dict1.keys():

        # print(dict1[key]['question'])
        question = dict1[key]['question']
        answers = dict1[key]['answers']
        # print("A." + answers[0], "B." + answers[1], "C." + answers[2], "D." + answers[3], "E." + answers[4])
        # answers1 = " A." + answers[0] + " B." + answers[1] + " C." + answers[2] + " D." + answers[3] + " E." + answers[4] + "."
        answers1 = " A." + answers[0] + " B." + answers[1] + " C." + answers[2] + " D." + answers[3] + "."
        # print(dict1[key]['answerKey'])
        answerKey = dict1[key]['answerKey']
        num_questions = num_questions + 1
        x1 = question + answers1
        break_flag = 0
        if num_questions >= 1:
            while 1:
                try:
                    print("Question NUM:", num_questions, x1)
                    answers_chatgpt = sim_chatgpt2.predict(x1)
                    print("ChatGPT prediction: ", answers_chatgpt)
                    print("Label: ", answerKey)

                    if str(answerKey) in answers_chatgpt:
                        num_correct = num_correct + 1
                    acc = num_correct * 1.0 / (num_questions - 0)
                    print("ACC: ", acc)
                    time.sleep(1)
                    break
                except:
                    time.sleep(20)
                    break_flag += 1
                    if break_flag >= 5:
                        print('This system is down! Please set a larger time interval between two queries!')
                        sys.exit(1)
                    print('The system is busy! Please wait for one minute!\n')


