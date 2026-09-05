CSS = r""":root {
  --font-color-primary: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
  --font-color-secondary: var(--jp-content-font-color2, rgba(0, 0, 0, 0.7));
  --font-color-accent: rgba(123, 31, 162, 1);
  --border-color: var(--jp-border-color2, #e0e0e0);
  --background-color: var(--jp-layout-color0, white);
  --background-color-row-even: var(--jp-layout-color1, white);
  --background-color-row-odd: var(--jp-layout-color2, #eeeeee);
}

html[theme="dark"],
body[data-theme="dark"],
body.vscode-dark {
  --font-color-primary: rgba(255, 255, 255, 1);
  --font-color-secondary: rgba(255, 255, 255, 0.7);
  --font-color-accent: rgb(173, 132, 190);
  --border-color: #2e2e2e;
  --background-color: #111111;
  --background-color-row-even: #111111;
  --background-color-row-odd: #313131;
}

.eerepr {
  padding: 1em;
  line-height: 1.5em;
  min-width: 300px;
  max-width: 1200px;
  overflow-y: scroll;
  max-height: 600px;
  border: 1px solid var(--border-color);
  font-family: monospace;
  font-size: 14px;
}

.eerepr li {
  list-style-type: none;
  margin: 0;
}

.eerepr ul {
  padding-left: 1.5em !important;
  margin: 0;
}

.eerepr > ul {
  padding-left: 0 !important;
}

.eerepr summary {
  color: var(--font-color-secondary);
  cursor: pointer;
  margin: 0;
}

.eerepr summary:hover {
  color: var(--font-color-primary);
  background-color: var(--background-color-row-odd)
}

.ee-k {
  color: var(--font-color-accent);
  margin-right: 6px;
}

.ee-v {
  color: var(--font-color-primary);
}

.eerepr details > summary::before {
  content: '▼';
  display: inline-block;
  margin-right: 6px;
  transition: transform 0.2s;
  transform: rotate(-90deg);
}

.eerepr details[open] > summary::before {
  transform: rotate(0deg);
}

.eerepr details summary::-webkit-details-marker {
  display:none;
}

.eerepr details summary {
  list-style-type: none;
}
"""
