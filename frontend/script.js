const messageApi = "http://localhost:8001/messages";

async function fetchMessages() {
  const response = await fetch(messageApi);
  const messages = await response.json();
  return messages;
}

setInterval(async () => {
  const data = await fetchMessages();
  document.getElementById("output").innerText = data.symbols.join("");
}, 1000);
