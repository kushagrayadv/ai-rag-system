from clearml.automation import PipelineController

from steps.etl import crawl_links, get_or_create_user

pipe = PipelineController(
  name="digital_data_etl",
  project="ai_rag_system",
  version="1.0.0",
  packages=[""],
  repo=""
)

pipe.add_parameter("user_full_name", "John Doe")
pipe.add_parameter("links", ["https://github.com/ros2/rcl"])

pipe.add_function_step(
  name="get_or_create_user",
  function=get_or_create_user,
  function_kwargs=dict(user_full_name="${pipeline.user_full_name}"),
  function_return=["user"],
  cache_executed_step=True,

)

pipe.add_function_step(
  name="crawl_links",
  function=crawl_links,
  function_kwargs=dict(
    user="${get_or_create_user.user}",
    links="${pipeline.links}"
  ),
  function_return=["invocation_id"],
  cache_executed_step=True,
  parents=["get_or_create_user"],
)

pipe.set_default_execution_queue("default")

if __name__ == "__main__":
  pipe.start_locally(run_pipeline_steps_locally=True)
  print(f"Pipeline started. Check the ClearML web UI for progress.")
