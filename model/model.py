from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import asyncio

# Define model path (update if your folder is in a different location)
model_path = "./model/robert-base-toxic"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

label_map = {0: "OTHER", 1: "PROFANITY", 2: "INSULT", 3: "ABUSE"}

async def predict(text):
    return await asyncio.to_thread(run_interface, text)

def run_interface(text):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Ensure model is on the correct device
    model.to(device) 

    # Tokenize and move inputs to the same device as the model
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}  # Move tensors to the correct device

    # Forward pass
    outputs = model(**inputs)
    predictions = label_map[outputs.logits.argmax(dim=-1).item()]

    return predictions  # Map to actual labels if needed

