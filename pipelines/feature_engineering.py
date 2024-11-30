from clearml import Task, PipelineController
from steps import feature_engineering as fe_steps

def feature_engineering(author_full_names, wait_for=None):

    task = Task.init(project='ai_rag_system', task_name='Feature Engineering', task_type='pipeline')
    # Create a pipeline controller for executing steps
    controller = PipelineController()

    # Step 1: Query data
    raw_documents = controller.add_function_step(
        name='query_data_warehouse',
        function=fe_steps.query_data_warehouse,
        function_kwargs=dict(author_full_names=author_full_names, after=wait_for),
        function_return=['raw_documents']
    )

    # Step 2: Clean documents
    cleaned_documents = controller.add_function_step(
        name='clean_documents',
        function=fe_steps.clean_documents,
        function_kwargs=dict(raw_documents='${query_data_warehouse.raw_documents}'),
        function_return=['cleaned_documents']
    )

    # Step 3: Load to vector DB
    last_step_1 = controller.add_function_step(
        name='load_to_vector_db_1',
        function=fe_steps.load_to_vector_db,
        function_kwargs=dict(documents='${clean_documents.cleaned_documents}'),
        function_return=['invocation_id']
    )

    # Step 4: Chunk and embed
    embedded_documents = controller.add_function_step(
        name='chunk_and_embed',
        function=fe_steps.chunk_and_embed,
        function_kwargs=dict(documents='${clean_documents.cleaned_documents}'),
        function_return=['embedded_documents']
    )

    # Step 5: Load to vector DB
    last_step_2 = controller.add_function_step(
        name='load_to_vector_db_2',
        function=fe_steps.load_to_vector_db,
        function_kwargs=dict(documents='${chunk_and_embed.embedded_documents}'),
        function_return=['invocation_id']
    )

    # Start the pipeline
    controller.start()

    return [last_step_1.invocation_id, last_step_2.invocation_id]