from clearml.automation import PipelineController
from steps.etl import crawl_links, get_or_create_user
from url_list import crawl_urls

pipe = PipelineController(
  name="digital_data_etl",
  project="ai_rag_system",
  version="1.0.0",
  packages=[""],
  repo=""
)

pipe.add_parameter("user_full_name", "Admin User")
pipe.add_parameter("links", crawl_urls)

pipe.add_function_step(
  name="get_or_create_user",
  function=get_or_create_user,
  function_kwargs=dict(user_full_name="${pipeline.user_full_name}"),
  function_return=["user"],
)

pipe.add_function_step(
  name="crawl_links",
  function=crawl_links,
  function_kwargs=dict(
    user="${get_or_create_user.user}",
    links="${pipeline.links}",
  ),
  function_return=["invocation_id"],
  parents=["get_or_create_user"],
)

pipe.set_default_execution_queue("default")

if __name__ == "__main__":
  print(f"Data ETL pipeline started...")
  pipe.start_locally(run_pipeline_steps_locally=True)
  print(f"Data ETL pipeline ended...")
