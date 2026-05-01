from django.http import JsonResponse
from django.shortcuts import render
from deep_translator import GoogleTranslator

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
            return JsonResponse({"success": False, "error": message}) if request.headers.get('x-requested-with') == 'XMLHttpRequest' else render(request, "main/index.html", {**context, "error": message})

        if language not in LANGUAGE_CHOICES:
            message = "Please choose a supported language."
            return JsonResponse({"success": False, "error": message}) if request.headers.get('x-requested-with') == 'XMLHttpRequest' else render(request, "main/index.html", {**context, "error": message})

        try:
            translation = GoogleTranslator(source='auto', target=language).translate(text)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "translation": translation})

            context["translation"] = translation

        except Exception:
            message = "Translation failed. Try again."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": message})
            context["error"] = message

    return render(request, "main/index.html", context)