from clearml import PipelineController

from domain.dataset import DatasetType
from settings import Settings
from steps import generate_datasets as cd_steps


def generate_datasets(
  dataset_type: DatasetType = DatasetType.INSTRUCTION,
  test_split_size: float = 0.1,
  push_to_huggingface: bool = False,
  dataset_id: str | None = None,
  mock: bool = False,
) -> None:
  pipeline = PipelineController(name="feature_engineering",
                                project="ai_rag_system",
                                version="1.0.0",
                                packages=[""],
                                repo="")

  pipeline.add_function_step(
    name='query_feature_store',
    function=cd_steps.query_feature_store,
    function_return=['cleaned_documents']
  )

  pipeline.add_function_step(
    name='create_prompts',
    function=cd_steps.create_prompts,
    function_kwargs=dict(documents='${query_feature_store.cleaned_documents}', dataset_type=dataset_type),
    function_return=['prompts']
  )

  if dataset_type == DatasetType.INSTRUCTION:
    pipeline.add_function_step(
      name='generate_instruction_dataset',
      function=cd_steps.generate_instruction_dataset,
      function_kwargs=dict(prompts='${create_prompts.prompts}', test_split_size=test_split_size, mock=mock),
      function_return=['dataset']
    )
  elif dataset_type == DatasetType.PREFERENCE:
    pipeline.add_function_step(
      name='generate_preference_dataset',
      function=cd_steps.generate_preference_dataset,
      function_kwargs=dict(prompts='${create_prompts.prompts}', test_split_size=test_split_size, mock=mock),
      function_return=['dataset']
    )
  else:
    raise ValueError(f"Invalid dataset type: {dataset_type}")

  if push_to_huggingface:
    pipeline.add_function_step(
      name='push_to_huggingface',
      function=cd_steps.push_to_huggingface,
      function_kwargs=dict(dataset='${generate_instruction_dataset.dataset}', dataset_id=dataset_id),
    )

  pipeline.start_locally(run_pipeline_steps_locally=True)


if __name__ == "__main__":
  print(f"Dataset generation pipeline started...")
  generate_datasets(push_to_huggingface=True, dataset_id=Settings.DATASET_ID)