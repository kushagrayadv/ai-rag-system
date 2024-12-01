from pydantic_settings import BaseSettings, SettingsConfigDict


# TODO: change the config according to our project
class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

  # Huggingface API
  HUGGINGFACE_ACCESS_TOKEN: str | None = ""

  DATASET_ID: str = "billa-man/ai-rag-system-dataset-large"

  # MongoDB database
  DATABASE_HOST: str = ""
  DATABASE_NAME: str = "rag-database-large"

  # Qdrant vector database
  USE_QDRANT_CLOUD: bool = True
  QDRANT_DATABASE_HOST: str = "localhost"
  QDRANT_DATABASE_PORT: int = 6333
  QDRANT_CLOUD_URL: str = ""
  QDRANT_APIKEY: str | None = ""
  # --- Optional settings used to tweak the code. ---

  OLLAMA_CLIENT_HOST: str = "http://localhost:11434"

  # RAG
  TEXT_EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
  RERANKING_CROSS_ENCODER_MODEL_ID: str = "cross-encoder/ms-marco-MiniLM-L-4-v2"
  RAG_MODEL_DEVICE: str = "cpu"

  HF_MODEL_ID: str = "billa-man/finetuned-rag-system-robotics"

  # OpenAI API
  OPENAI_MODEL_ID: str = "gpt-4o-mini"

  # sohith's token
  OPENAI_API_KEY: str | None = ""

  @property
  def OPENAI_MAX_TOKEN_WINDOW(self) -> int:
    official_max_token_window = {
      "gpt-3.5-turbo": 16385,
      "gpt-4-turbo": 128000,
      "gpt-4o": 128000,
      "gpt-4o-mini": 128000,
    }.get(self.OPENAI_MODEL_ID, 128000)

    max_token_window = int(official_max_token_window * 0.90)

    return max_token_window


settings = Settings()
