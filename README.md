# revise.gpt
A simple Django app for uploading `pdf` files, extracting their text, and revising with an `openai` GPT model.

The default application will build a `LinkedIn style` resume summary paragraph.
1. Start the Django server `python manage.py runserver`
2. Navigate to `http://127.0.0.1:8000/polls/upload/`
3. Upload a `pdf` resume.
4. The model will respond with a summary.

You will need to set the `OPENAI_API_APIKEY` environment variable with your OpenAI API Key.