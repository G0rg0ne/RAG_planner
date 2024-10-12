import replicate

f = open("info.txt", "r")
str_file = f.read()
promt = "when did spain score the goals?"
context = " using this context"

# The mistralai/mixtral-8x7b-instruct-v0.1 model can stream output as it's running.
for event in replicate.stream(
    "mistralai/mixtral-8x7b-instruct-v0.1",
    input={
        "top_k": 50,
        "top_p": 0.9,
        "prompt":  promt + context + str_file ,
        "temperature": 0.6,
        "system_prompt": "You are a very helpful, answer using one phrase",
        "length_penalty": 1,
        "max_new_tokens": 1024,
        "prompt_template": "<s>[INST] {prompt} [/INST] ",
        "presence_penalty": 0
    },
):
    print(str(event), end="")



import os
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

# Initialize the tokenizer, retriever, and the model
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

# Directory containing the .txt files
txt_files_directory = 'path_to_your_txt_files_directory'

# Load the texts from the .txt files
documents = []
for filename in os.listdir(txt_files_directory):
    if filename.endswith(".txt"):
        with open(os.path.join(txt_files_directory, filename), 'r', encoding='utf-8') as file:
            documents.append(file.read())

# Update retriever's index with the new documents
retriever.index.index_data(documents)

def generate_answer(question):
    inputs = tokenizer(question, return_tensors="pt")
    generated = model.generate(**inputs)
    return tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

# Example usage
question = "What is the capital of France?"
answer = generate_answer(question)
print(answer)
