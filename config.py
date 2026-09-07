import torch
from pathlib import Path

from settings import PROJECT_ROOT, get_required_env
from transformers import T5ForConditionalGeneration, T5Tokenizer

# model_dir = Path(get_required_env("MODEL_DIR"))
# MODEL_DIR = model_dir if model_dir.is_absolute() else PROJECT_ROOT / model_dir
# MODEL_DIR="saved_summury_model"
MODEL_DIR="nidhitk/T5-summarizer" #from hugging face

model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)

if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

model.to(device)
