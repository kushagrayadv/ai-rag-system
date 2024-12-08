from clearml import Task
from typing_extensions import Annotated

from application.dataset import generation
from domain.prompt import GenerateDatasetSamplesPrompt
from domain.types import DataCategory


def create_prompts(
  documents: Annotated[list, "queried_cleaned_documents"]
) -> Annotated[dict[DataCategory, list[GenerateDatasetSamplesPrompt]], "prompts"]:
  dataset_generator = generation.get_dataset_generator()
  grouped_prompts = dataset_generator.get_prompts(documents)

  prompt_categories = list(grouped_prompts.keys())
  prompt_num_samples = {category: len(prompts) for category, prompts in grouped_prompts.items()}

  metadata = {"data_categories": prompt_categories, "data_categories_num_prompts": prompt_num_samples}

  task = Task.current_task()
  task.upload_artifact("prompts", grouped_prompts, metadata=metadata)

  return grouped_prompts
