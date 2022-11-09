function toggleHeader() {
    const parent = this.parentElement;
    const open = "eerepr-header-open";
    const closed = "eerepr-header-closed";
    parent.className = parent.className === open ? closed : open;
}

for (let c of document.getElementsByClassName("eerepr-collapser")) {
    c.onclick = toggleHeader;
}