class OllamaAIInterface {
    constructor(parentId) {
        this.parent = document.getElementById(parentId);
        this.container = document.createElement("div");
        this.container.className = "ollama-ai-interface";

        // Create chat output area
        this.output = document.createElement("div");
        this.output.className = "ollama-output";
        this.output.style.height = "200px";
        this.output.style.overflowY = "auto";
        this.output.style.border = "1px solid #ccc";
        this.output.style.padding = "5px";
        this.output.style.marginBottom = "5px";
        this.output.style.backgroundColor = "#fff";
        this.container.appendChild(this.output);

        // Create input form
        this.form = document.createElement("form");
        this.form.className = "ollama-input-form";

        this.input = document.createElement("input");
        this.input.type = "text";
        this.input.placeholder = "Ask Ollama AI...";
        this.input.style.width = "80%";
        this.input.style.padding = "5px";
        this.input.required = true;

        this.submitBtn = document.createElement("button");
        this.submitBtn.type = "submit";
        this.submitBtn.textContent = "Send";
        this.submitBtn.style.padding = "5px 10px";
        this.submitBtn.style.marginLeft = "5px";

        this.form.appendChild(this.input);
        this.form.appendChild(this.submitBtn);
        this.container.appendChild(this.form);

        this.parent.appendChild(this.container);

        this.form.addEventListener("submit", (e) => {
            e.preventDefault();
            const question = this.input.value.trim();
            if (question) {
                this.addMessage("User", question);
                this.input.value = "";
                this.queryOllamaAI(question);
            }
        });
    }

    addMessage(sender, message) {
        const msgDiv = document.createElement("div");
        msgDiv.className = "ollama-message";
        msgDiv.style.marginBottom = "5px";
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        this.output.appendChild(msgDiv);
        this.output.scrollTop = this.output.scrollHeight;
    }

    async queryOllamaAI(question) {
        this.addMessage("Ollama AI", "Thinking...");
        try {
            const response = await fetch("http://localhost:33119/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question })
            });
            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }
            const data = await response.json();
            // Remove "Thinking..." message
            const thinkingMsg = Array.from(this.output.children).find(child => child.textContent.includes("Thinking..."));
            if (thinkingMsg) this.output.removeChild(thinkingMsg);
            // Assuming the response has an 'answer' field
            this.addMessage("Ollama AI", data.answer || "No answer received.");
        } catch (error) {
            // Remove "Thinking..." message
            const thinkingMsg = Array.from(this.output.children).find(child => child.textContent.includes("Thinking..."));
            if (thinkingMsg) this.output.removeChild(thinkingMsg);
            this.addMessage("Ollama AI", `Error: ${error.message}`);
        }
    }
}

module.exports = {
    OllamaAIInterface
};
