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