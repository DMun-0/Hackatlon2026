const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const loading = document.getElementById("loading");

const API_URL = "http://localhost:5000/api/chat";

// Send message on button click
sendBtn.addEventListener("click", sendMessage);

// Send message on Enter key
messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

async function sendMessage() {
  const message = messageInput.value.trim();

  if (!message) return;

  // Add user message to chat
  addMessageToChat(message, "user");
  messageInput.value = "";
  sendBtn.disabled = true;
  loading.style.display = "flex";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    addMessageToChat(data.response, "ai");
  } catch (error) {
    console.error("Error:", error);
    addMessageToChat(
      "Beklager, jeg kunne ikke kontakte serveren. Er Ollama kjørende?",
      "ai",
    );
  } finally {
    sendBtn.disabled = false;
    loading.style.display = "none";
    messageInput.focus();
  }
}

function addMessageToChat(message, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}-message`;

  const p = document.createElement("p");
  p.textContent = message;

  messageDiv.appendChild(p);
  chatBox.appendChild(messageDiv);

  // Scroll to bottom
  chatBox.scrollTop = chatBox.scrollHeight;
}
