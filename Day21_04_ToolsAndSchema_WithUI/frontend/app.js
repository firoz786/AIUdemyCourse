const button =
    document.getElementById(
        "researchButton"
    );

const topicInput =
    document.getElementById(
        "topic"
    );

const status =
    document.getElementById(
        "status"
    );

const result =
    document.getElementById(
        "result"
    );

const progressSection =
    document.getElementById(
        "progressSection"
    );

const resultSection =
    document.getElementById(
        "resultSection"
    );

const errorBox =
    document.getElementById(
        "error"
    );

const characterCount =
    document.getElementById(
        "characterCount"
    );


topicInput.addEventListener(
    "input",
    () => {

        const length =
            topicInput.value.length;

        characterCount.textContent =
            `${length} characters`;
    }
);


button.addEventListener(
    "click",
    async () => {

        const topic =
            topicInput.value.trim();


        if (!topic) {

            errorBox.textContent =
                "Please enter a research topic.";

            errorBox.classList.remove(
                "hidden"
            );

            return;
        }


        errorBox.classList.add(
            "hidden"
        );

        resultSection.classList.add(
            "hidden"
        );

        progressSection.classList.remove(
            "hidden"
        );


        button.disabled = true;

        button.textContent =
            "Researching...";


        status.textContent =
            "Your research agent is working...";


        try {

            const response =
                await fetch(
                    "/chat",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            message: topic
                        })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Research request failed."
                );
            }


            const data =
                await response.json();


            progressSection.classList.add(
                "hidden"
            );


            resultSection.classList.remove(
                "hidden"
            );


            result.textContent =
                data.response;


        } catch (error) {

            progressSection.classList.add(
                "hidden"
            );


            errorBox.textContent =
                error.message ||
                "Unable to complete research.";

            errorBox.classList.remove(
                "hidden"
            );


        } finally {

            button.disabled = false;

            button.innerHTML =
                "<span>✦</span> Start Research";
        }

    }
);
