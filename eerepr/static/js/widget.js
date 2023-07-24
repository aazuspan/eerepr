export function render(view) {
  const getContent = () => view.model.get("content");
  const div = document.createElement("div");
  div.className = "ee";

  function toggleHeader() {
    const parent = this.parentElement;
    parent.className = parent.className === "ee-open" ? "ee-shut" : "ee-open";
  }

  view.model.on("change:content", () => {
    div.innerHTML = getContent();
    const toggles = div.querySelectorAll(".ee-toggle");
    for (let c of toggles) {
      c.onclick = toggleHeader;
    }
  });

  div.innerHTML = getContent();
  view.el.appendChild(div);
}
