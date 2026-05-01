from django.shortcuts import render
from translate import Translator

LANGUAGE_CHOICES = {
    "en": "English",
    "hi": "Hindi",
    "pa": "Punjabi",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "zh": "Chinese",
    "ar": "Arabic",
    "ru": "Russian",
}


def home(request):
    context = {"languages": LANGUAGE_CHOICES, "text": "", "selected_language": ""}
    if request.method == "POST":
        text = request.POST.get("translate", "").strip()
        language = request.POST.get("language", "").strip()
        context["text"] = text
        context["selected_language"] = language
        if not text:
            context["error"] = "Please enter text to translate."
            return render(request, "main/index.html", context)
        if language not in LANGUAGE_CHOICES:
            context["error"] = "Please choose a supported language."
            return render(request, "main/index.html", context)
        try:
            translator = Translator(to_lang=language)
            context["translation"] = translator.translate(text)
        except Exception:
            context["error"] = (
                "Translation service is unavailable right now. "
                "Please try again in a moment."
            )
    return render(request, "main/index.html", context)
