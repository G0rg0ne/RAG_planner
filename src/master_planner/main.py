from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
 
# The device to load the model onto. 
#
# Available device types:
# "cuda" - NVIDIA GPU
# "cpu" - Plain CPU
# "mps" - Apple silicon
device = "cpu"
access_token = "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"

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", token=access_token)
model.to(device)
 
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", token=access_token)