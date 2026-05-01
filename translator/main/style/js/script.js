const form = document.getElementById("translate-form");
const input = document.getElementById("search-input");
const languageSelect = document.getElementById("language-select");
const statusMessage = document.getElementById("status-message");
const translationBlock = document.getElementById("translation-block");
const translationText = document.getElementById("translation-text");
const errorBlock = document.getElementById("error-block");
const errorText = document.getElementById("error-text");

let translateTimeout;
let currentRequest = 0;

function resetMessages() {
  statusMessage.textContent = "";
  errorBlock.hidden = true;
}

async function translateText() {
  const text = input.value.trim();
  const language = languageSelect.value;

  if (!text) {
    statusMessage.textContent = "";
    translationBlock.hidden = true;
    errorBlock.hidden = true;
    return;
  }

  currentRequest += 1;
  const requestId = currentRequest;
  statusMessage.textContent = "Translating...";
  errorBlock.hidden = true;

  const formData = new FormData(form);

  try {
    const response = await fetch(form.action || window.location.href, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    const data = await response.json();
    if (requestId !== currentRequest) {
      return;
    }

    if (data.success) {
      translationText.textContent = data.translation;
      translationBlock.hidden = false;
      errorBlock.hidden = true;
      statusMessage.textContent = "";
      return;
    }

    translationBlock.hidden = true;
    errorText.textContent = data.error;
    errorBlock.hidden = false;
    statusMessage.textContent = "";
  } catch (error) {
    if (requestId !== currentRequest) {
      return;
    }
    translationBlock.hidden = true;
    errorText.textContent =
      "Translation service is unavailable right now. Please try again in a moment.";
    errorBlock.hidden = false;
    statusMessage.textContent = "";
  }
}

function queueTranslation() {
  clearTimeout(translateTimeout);
  translateTimeout = setTimeout(translateText, 350);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  clearTimeout(translateTimeout);
  translateText();
});

input.addEventListener("input", queueTranslation);
languageSelect.addEventListener("change", () => {
  resetMessages();
  if (input.value.trim()) {
    translateText();
  }
});
