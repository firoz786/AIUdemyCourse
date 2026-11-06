const button = document.getElementById("researchButton");
const topicInput = document.getElementById("topic");
const status = document.getElementById("status");
const result = document.getElementById("result");

button.addEventListener("click", async (e) => {
    e.preventDefault();

    const topic = topicInput.value.trim();

    if (!topic) {
        status.textContent = "Please enter a research topic.";
        return;
    }

    status.textContent = "Researching...";
    result.textContent = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: topic
            })
        });

        if (!response.ok) {
            throw new Error("Request failed");
        }

        const data = await response.json();

        status.textContent = "Research completed.";
        result.textContent = data.response;

    } catch (error) {
        status.textContent = "Something went wrong.";
        result.textContent = "Unable to complete the request.";
    }
});