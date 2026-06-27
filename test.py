import json
from models.flashcard import FlashcardResponse


response = '''
{
  "flashcards": [
    {
      "question": "What is ML?",
      "answer": "Machine Learning"
    },
    {
      "question": "What is supervised learning?",
      "answer": "Learning from labeled data."
    }
  ]
}
'''

data = json.loads(response)

result = FlashcardResponse.model_validate(data)

print(result.flashcards[0].question)
print(result.flashcards[0].answer)