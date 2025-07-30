class BasicTextEditor {
    constructor(parentId) {
        this.parent = document.getElementById(parentId);
        this.container = document.createElement("div");
        this.container.className = "basic-text-editor";

        this.textarea = document.createElement("textarea");
        this.textarea.style.width = "100%";
        this.textarea.style.height = "250px";
        this.textarea.style.resize = "none";
        this.textarea.style.fontFamily = "monospace";
        this.textarea.style.fontSize = "14px";
        this.textarea.style.padding = "5px";
        this.textarea.placeholder = "Start typing...";

        this.container.appendChild(this.textarea);
        this.parent.appendChild(this.container);
    }
}

module.exports = {
    BasicTextEditor
};
