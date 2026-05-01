from django.http import JsonResponse
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
            message = "Please enter text to translate."
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": message})
            context["error"] = message
            return render(request, "main/index.html", context)
        if language not in LANGUAGE_CHOICES:
            message = "Please choose a supported language."
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": message})
            context["error"] = message
            return render(request, "main/index.html", context)
        try:
            translator = Translator(to_lang=language)
            translation = translator.translate(text)
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True, "translation": translation})
            context["translation"] = translation
        except Exception:
            message = (
                "Translation service is unavailable right now. "
                "Please try again in a moment."
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": message})
            context["error"] = message
    return render(request, "main/index.html", context)
