function toggleHeader() {
    const parent = this.parentElement;
    parent.className = parent.className === "ee-open" ? "ee-shut" : "ee-open";
}

for (let c of document.getElementsByClassName("ee-toggle")) {
    c.onclick = toggleHeader;
}