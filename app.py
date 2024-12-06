from infrastructure.inference_pipeline import rag

if __name__ == '__main__':
  query = """
    My name is Admin User.
    I want to know what is ros2 ?
  """

  answer = rag(query)
