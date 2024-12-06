from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM

from application.rag.retriever import ContextRetriever
from domain.embedded_chunks import EmbeddedChunk
from settings import settings


def login_to_huggingface():
  login(token="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")


def call_llm_service(query: str, context: str | None) -> str:
  tokenizer = AutoTokenizer.from_pretrained(settings.HF_MODEL_ID)
  model = AutoModelForCausalLM.from_pretrained(
    settings.HF_MODEL_ID
  )

  prompt = """
    You are a content creator. Write what the user asked you to while using the provided context as the primary source of information for the content.
    User query: {query}
    Context: {context}
  """

  llm_input = prompt.format(query=query, context=context)
  inputs = tokenizer(llm_input, return_tensors="pt", max_length=512, truncation=True).to(model.device)
  outputs = model.generate(inputs["input_ids"], max_length=200, num_return_sequences=1, temperature=0.7)
  answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

  return answer


def rag(query: str) -> str:
  retriever = ContextRetriever(mock=False)
  documents = retriever.search(query, k=3)
  context = EmbeddedChunk.to_context(documents)

  # login_to_huggingface()
  answer = call_llm_service(query, context)

  return answer
