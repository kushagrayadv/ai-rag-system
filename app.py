import gradio as gr

from infrastructure.inference_pipeline import rag

prepopulated_questions = [
  "",
  "Tell me how can I navigate to a specific pose - include replanning aspects in your answer.",
  "Can you provide me with code for navigation to a specific pose while including replanning aspects?"
]


def get_response(selected_question):
  response = ""
  answer_stream = rag(selected_question)

  # Update the response in chunks
  for chunk in answer_stream:
    response += chunk['message']['content']
    yield response  # Stream the output live


gradio_app = gr.Interface(
  fn=get_response,
  inputs=gr.Dropdown(choices=prepopulated_questions, label="Select Your Question"),
  outputs=gr.Textbox(label="Answer", interactive=True),
  title="AI RAG System",
  description="Interact with the AI RAG System. Select a question from the dropdown and get a live answer.",
  live=True
)

if __name__ == '__main__':
  gradio_app.launch()
