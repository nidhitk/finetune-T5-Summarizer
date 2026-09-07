import re
import torch

from config import device, model, tokenizer


# def clean_data(text):
#     text = re.sub(r"\r\n", " ", text)
#     text = re.sub(r"<.*?>", " ", text)
#     text = re.sub(r"\s+", " ", text)
#     return text.strip().lower()
def clean_data(text):
    text = re.sub(r"[\r\n]+", " ", text)     # Remove new lines
    text = re.sub(r"<.*?>", " ", text)       # Remove HTML tags
    text = re.sub(r"\s+", " ", text)        # Remove extra spaces

    return text.strip().lower()


def summarize(dialogue: str) -> str:
    dialogue = clean_data(dialogue)
    inputs = tokenizer(
        dialogue,
        padding="max_length",
        max_length=512,
        truncation=True,
        return_tensors="pt",
    ).to(device)

    model.eval()
    with torch.no_grad():
        targets = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=150,
            num_beams=4,
            early_stopping=True,
        )

    return tokenizer.decode(targets[0], skip_special_tokens=True)
