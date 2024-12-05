from pydantic_settings import BaseSettings, SettingsConfigDict


# TODO: change the config according to our project
class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

  # --- Required settings even when working locally. ---

  # OpenAI API
  OPENAI_MODEL_ID: str = "gpt-4o-mini"
  OPENAI_API_KEY: str | None = None

  # Huggingface API
  HUGGINGFACE_ACCESS_TOKEN: str | None = "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"

  DATASET_ID: str = 'kushagrayadv/ai-rag-system-dataset'

  # Comet ML (during training)
  COMET_API_KEY: str | None = None
  COMET_PROJECT: str = "twin"

  # --- Required settings when deploying the code. ---
  # --- Otherwise, default values work fine. ---

  # MongoDB database
  DATABASE_HOST: str = "mongodb+srv://sohithbandari:Zjq1L1owGRbASeEw@csgy-6613-project-kysb.b7rso.mongodb.net/?retryWrites=true&w=majority&appName=csgy-6613-project-kysb"
  DATABASE_NAME: str = "rag"

  # Qdrant vector database
  USE_QDRANT_CLOUD: bool = True
  QDRANT_DATABASE_HOST: str = "localhost"
  QDRANT_DATABASE_PORT: int = 6333
  QDRANT_CLOUD_URL: str = "https://6f00fbd5-b1e3-424c-acad-8bd09a9c7090.us-west-1-0.aws.cloud.qdrant.io:6333"
  QDRANT_APIKEY: str | None = "apgKddFp_XPkbVREmxGetfqhvqI4ivjrBva9bJMG7FH4g0OpzOdoBg"

  # AWS Authentication
  AWS_REGION: str = "eu-central-1"
  AWS_ACCESS_KEY: str | None = None
  AWS_SECRET_KEY: str | None = None
  AWS_ARN_ROLE: str | None = None

  # --- Optional settings used to tweak the code. ---

  # AWS SageMaker
  HF_MODEL_ID: str = "mlabonne/TwinLlama-3.1-8B-DPO"
  GPU_INSTANCE_TYPE: str = "ml.g5.2xlarge"
  SM_NUM_GPUS: int = 1
  MAX_INPUT_LENGTH: int = 2048
  MAX_TOTAL_TOKENS: int = 4096
  MAX_BATCH_TOTAL_TOKENS: int = 4096
  COPIES: int = 1  # Number of replicas
  GPUS: int = 1  # Number of GPUs
  CPUS: int = 2  # Number of CPU cores

  SAGEMAKER_ENDPOINT_CONFIG_INFERENCE: str = "twin"
  SAGEMAKER_ENDPOINT_INFERENCE: str = "twin"
  TEMPERATURE_INFERENCE: float = 0.01
  TOP_P_INFERENCE: float = 0.9
  MAX_NEW_TOKENS_INFERENCE: int = 150

  # RAG
  TEXT_EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
  RERANKING_CROSS_ENCODER_MODEL_ID: str = "cross-encoder/ms-marco-MiniLM-L-4-v2"
  RAG_MODEL_DEVICE: str = "cpu"

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
