from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer

print('Downloading FinBERT...')
_ = AutoTokenizer.from_pretrained('ProsusAI/finbert')
_ = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')

print('Downloading SentenceTransformer...')
_ = SentenceTransformer('all-MiniLM-L6-v2')
print('Done.')
