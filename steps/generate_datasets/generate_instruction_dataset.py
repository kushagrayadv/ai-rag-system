from clearml import Task
from typing_extensions import Annotated

from application.dataset import generation
from domain.dataset import DatasetType, InstructTrainTestSplit
from domain.prompt import GenerateDatasetSamplesPrompt
from domain.types import DataCategory


def generate_instruction_dataset(
  prompts: Annotated[dict[DataCategory, list[GenerateDatasetSamplesPrompt]], "prompts"],
  test_split_size: Annotated[float, "test_split_size"],
  mock: Annotated[bool, "mock_generation"] = False,
) -> InstructTrainTestSplit:
  dataset_generator = generation.get_dataset_generator(DatasetType.INSTRUCTION)
  datasets = dataset_generator.generate(prompts, test_size=test_split_size, mock=mock)

  instruct_dataset_categories = list(datasets.train.keys())
  train_num_samples = {
    category: instruct_dataset.num_samples for category, instruct_dataset in datasets.train.items()
  }
  test_num_samples = {category: instruct_dataset.num_samples for category, instruct_dataset in datasets.test.items()}

  metadata = {
    "data_categories": instruct_dataset_categories,
    "test_split_size": datasets.test_split_size,
    "train_num_samples_per_category": train_num_samples,
    "test_num_samples_per_category": test_num_samples,
  }

  task = Task.current_task()
  task.upload_artifact("instruct_datasets", datasets, metadata=metadata)

  return datasets
