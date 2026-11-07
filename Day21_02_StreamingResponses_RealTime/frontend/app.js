const button = document.getElementById(
    "researchButton"
);

const topicInput = document.getElementById(
    "topic"
);

const status = document.getElementById(
    "status"
);

const result = document.getElementById(
    "result"
);


button.addEventListener(
    "click",
    () => {

        const topic = topicInput.value.trim();

        if (!topic) {
            status.textContent =
                "Please enter a research topic.";

            return;
        }

        status.textContent =
            "Ready to start research.";

        result.textContent = "";
    }
);
