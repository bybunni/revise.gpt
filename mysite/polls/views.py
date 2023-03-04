import os
import openai

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Question
from .forms import UploadFileForm
from PyPDF2 import PdfReader


openai.api_key = os.getenv("OPENAI_API_KEY")


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
        "my_name": "John Doe",
    }
    # return HttpResponse(template.render(context, request))
    return render(
        request, "polls/index.html", context
    )  # the original request, the template name, the context


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # the model, kwargs
    return render(request, "polls/detail.html", {"question": question})
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def success(request):
    return HttpResponse("File upload successful!")


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            text = handle_uploaded_file(request.FILES["file"])
            summary = summary_from_text(text)
            return render(request, "polls/text.html", {"text": summary})
            # return HttpResponseRedirect("success", {"text": text})
            # return HttpResponse(text)
    else:
        form = UploadFileForm()
    return render(request, "polls/upload.html", {"form": form})


def summary_from_text(text):
    instruction = (
        "Write a short LinkedIn style summary in the third person without the typical cliches."
        "Do not mention names."
        "Do not use pronouns."
        "Do not mention employers."
        "Highlight only the most impressive accomplishments."  # , include numbers if possible."
        "Summary:"
    )
    prompt = text + instruction
    davinci = False
    print("Waiting for response...")
    if davinci:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            echo=False,
        )
        return response["choices"][0]["text"]
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        return response["choices"][0]["message"]["content"]


def handle_uploaded_file(f):
    with open("polls/uploads/sample.pdf", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    reader = PdfReader("polls/uploads/sample.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
