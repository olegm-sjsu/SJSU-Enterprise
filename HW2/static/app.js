const API = "";

const issueList = document.getElementById("issue-list");
const emptyState = document.getElementById("empty-state");
const listError = document.getElementById("list-error");
const listErrorMessage = document.getElementById("list-error-message");
const retryBtn = document.getElementById("retry-btn");
const tabs = document.getElementById("tabs");
const repoNameEl = document.getElementById("repo-name");
const connectionPill = document.getElementById("connection-pill");
const connectionLabel = document.getElementById("connection-label");

const newIssuePanel = document.getElementById("new-issue-panel");
const newIssueForm = document.getElementById("new-issue-form");
const newIssueBtn = document.getElementById("new-issue-btn");
const emptyNewIssueBtn = document.getElementById("empty-new-issue-btn");
const cancelIssueBtn = document.getElementById("cancel-issue-btn");
const submitIssueBtn = document.getElementById("submit-issue-btn");
const formError = document.getElementById("form-error");

let currentState = "all";

function setActiveTab(state) {
  currentState = state;
  [...tabs.children].forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.state === state);
  });
}

function relativeTime(isoString) {
  const diffMs = Date.now() - new Date(isoString).getTime();
  const diffSec = Math.max(0, Math.floor(diffMs / 1000));
  const units = [
    ["year", 31536000],
    ["month", 2592000],
    ["day", 86400],
    ["hour", 3600],
    ["minute", 60],
  ];
  for (const [name, secs] of units) {
    const value = Math.floor(diffSec / secs);
    if (value >= 1) return `${value} ${name}${value > 1 ? "s" : ""} ago`;
  }
  return "just now";
}

function repoFromHtmlUrl(url) {
  const match = url.match(/github\.com\/([^/]+)\/([^/]+)\/issues/);
  return match ? `${match[1]}/${match[2]}` : null;
}

function setConnection(ok, message, repo) {
  connectionPill.className = `pill ${ok ? "pill-ok" : "pill-error"}`;
  connectionLabel.textContent = ok ? "Connected" : `Disconnected — ${message}`;
  if (repo) repoNameEl.textContent = repo;
  else if (ok) repoNameEl.textContent = "repo unknown until an issue exists";
}

function renderSkeleton() {
  issueList.innerHTML = "";
  emptyState.hidden = true;
  listError.hidden = true;
  for (let i = 0; i < 5; i++) {
    const li = document.createElement("li");
    li.className = "skeleton-row";
    li.innerHTML = `<div class="skeleton-bar" style="width: ${60 + Math.random() * 30}%"></div><div class="skeleton-bar short"></div>`;
    issueList.appendChild(li);
  }
}

let issuesByNumber = {};

function renderIssues(issues) {
  issueList.innerHTML = "";
  emptyState.hidden = issues.length !== 0;
  issuesByNumber = {};

  for (const issue of issues) {
    issuesByNumber[issue.number] = issue;

    const li = document.createElement("li");
    const row = document.createElement("div");
    row.className = `issue-row state-${issue.state}`;

    const labels = issue.labels
      .map((name) => `<span class="label-pill">${escapeHtml(name)}</span>`)
      .join("");

    row.innerHTML = `
      <span class="state-icon"></span>
      <div class="issue-main">
        <div class="issue-row-top">
          <a class="issue-title" href="${issue.html_url}" target="_blank" rel="noopener">${escapeHtml(issue.title)}</a>
          <div class="row-actions">
            <button class="btn btn-sm" data-action="edit" data-number="${issue.number}">Edit</button>
            <button class="btn btn-sm" data-action="toggle-state" data-number="${issue.number}">${issue.state === "open" ? "Close" : "Reopen"}</button>
          </div>
        </div>
        <div class="issue-meta">
          <span class="number">#${issue.number}</span>
          opened ${relativeTime(issue.created_at)}
          <span class="labels">${labels}</span>
        </div>
        <div class="edit-panel" id="edit-panel-${issue.number}" hidden>
          <div class="field">
            <label>Title</label>
            <input type="text" class="edit-title">
          </div>
          <div class="field">
            <label>Description</label>
            <textarea class="edit-body" rows="4"></textarea>
          </div>
          <div class="form-error edit-error" hidden></div>
          <div class="form-actions">
            <button class="btn" data-action="cancel-edit" data-number="${issue.number}">Cancel</button>
            <button class="btn btn-primary" data-action="save-edit" data-number="${issue.number}">Save</button>
          </div>
          <div class="comment-box">
            <label>Add a comment</label>
            <textarea class="comment-body" rows="2" placeholder="Leave a comment"></textarea>
            <div class="form-error comment-error" hidden></div>
            <div class="comment-success" hidden>Comment added.</div>
            <div class="form-actions">
              <button class="btn btn-primary" data-action="add-comment" data-number="${issue.number}">Comment</button>
            </div>
          </div>
        </div>
      </div>
    `;
    row.querySelector(".edit-title").value = issue.title;
    row.querySelector(".edit-body").value = issue.body || "";

    li.appendChild(row);
    issueList.appendChild(li);
  }
}

async function parseErrorDetail(res) {
  try {
    const body = await res.json();
    return body.detail || `HTTP ${res.status}`;
  } catch {
    return `HTTP ${res.status}`;
  }
}

function editPanelFor(number) {
  return document.getElementById(`edit-panel-${number}`);
}

function toggleEdit(number) {
  const panel = editPanelFor(number);
  panel.hidden = !panel.hidden;
  if (!panel.hidden) panel.querySelector(".edit-title").focus();
}

function cancelEdit(number) {
  const panel = editPanelFor(number);
  const issue = issuesByNumber[number];
  panel.querySelector(".edit-title").value = issue.title;
  panel.querySelector(".edit-body").value = issue.body || "";
  panel.querySelector(".edit-error").hidden = true;
  panel.hidden = true;
}

async function saveEdit(number, button) {
  const panel = editPanelFor(number);
  const title = panel.querySelector(".edit-title").value.trim();
  const body = panel.querySelector(".edit-body").value.trim();
  const errorEl = panel.querySelector(".edit-error");
  errorEl.hidden = true;

  button.disabled = true;
  button.textContent = "Saving…";

  try {
    const res = await fetch(`${API}/issues/${number}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, body }),
    });

    if (!res.ok) {
      errorEl.textContent = await parseErrorDetail(res);
      errorEl.hidden = false;
      return;
    }

    await loadIssues();
  } catch {
    errorEl.textContent = "Can't reach the API server.";
    errorEl.hidden = false;
  } finally {
    button.disabled = false;
    button.textContent = "Save";
  }
}

async function toggleState(number, button) {
  const issue = issuesByNumber[number];
  const nextState = issue.state === "open" ? "closed" : "open";
  button.disabled = true;

  try {
    const res = await fetch(`${API}/issues/${number}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state: nextState }),
    });

    if (!res.ok) {
      showListError(await parseErrorDetail(res));
      return;
    }

    await loadIssues();
  } catch {
    showListError("Can't reach the API server.");
  } finally {
    button.disabled = false;
  }
}

async function addComment(number, button) {
  const panel = editPanelFor(number);
  const textarea = panel.querySelector(".comment-body");
  const errorEl = panel.querySelector(".comment-error");
  const successEl = panel.querySelector(".comment-success");
  const body = textarea.value.trim();
  errorEl.hidden = true;
  successEl.hidden = true;

  if (!body) {
    errorEl.textContent = "Comment can't be empty.";
    errorEl.hidden = false;
    return;
  }

  button.disabled = true;
  button.textContent = "Posting…";

  try {
    const res = await fetch(`${API}/issues/${number}/comments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ body }),
    });

    if (!res.ok) {
      errorEl.textContent = await parseErrorDetail(res);
      errorEl.hidden = false;
      return;
    }

    textarea.value = "";
    successEl.hidden = false;
  } catch {
    errorEl.textContent = "Can't reach the API server.";
    errorEl.hidden = false;
  } finally {
    button.disabled = false;
    button.textContent = "Comment";
  }
}

issueList.addEventListener("click", (e) => {
  const target = e.target.closest("[data-action]");
  if (!target) return;
  const number = target.dataset.number;

  if (target.dataset.action === "edit") toggleEdit(number);
  else if (target.dataset.action === "cancel-edit") cancelEdit(number);
  else if (target.dataset.action === "save-edit") saveEdit(number, target);
  else if (target.dataset.action === "toggle-state") toggleState(number, target);
  else if (target.dataset.action === "add-comment") addComment(number, target);
});

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

async function loadIssues(state = currentState) {
  setActiveTab(state);
  renderSkeleton();

  let res;
  try {
    res = await fetch(`${API}/issues?state=${state}&per_page=100`);
  } catch (err) {
    showListError("Can't reach the API server.");
    setConnection(false, "API server unreachable");
    return;
  }

  if (!res.ok) {
    const detail = await parseErrorDetail(res);
    showListError(detail);
    setConnection(false, detail);
    return;
  }

  const issues = await res.json();
  listError.hidden = true;
  renderIssues(issues);

  const withUrl = issues.find((i) => i.html_url);
  setConnection(true, null, withUrl ? repoFromHtmlUrl(withUrl.html_url) : null);
}

function showListError(message) {
  issueList.innerHTML = "";
  emptyState.hidden = true;
  listErrorMessage.textContent = message;
  listError.hidden = false;
}

function openPanel() {
  newIssuePanel.hidden = false;
  document.getElementById("issue-title").focus();
}

function closePanel() {
  newIssuePanel.hidden = true;
  newIssueForm.reset();
  formError.hidden = true;
}

tabs.addEventListener("click", (e) => {
  const tab = e.target.closest(".tab");
  if (tab) loadIssues(tab.dataset.state);
});

retryBtn.addEventListener("click", () => loadIssues());
newIssueBtn.addEventListener("click", openPanel);
emptyNewIssueBtn.addEventListener("click", openPanel);
cancelIssueBtn.addEventListener("click", closePanel);

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !newIssuePanel.hidden) closePanel();
});

newIssueForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  formError.hidden = true;

  const title = document.getElementById("issue-title").value.trim();
  const body = document.getElementById("issue-body").value.trim();
  const labels = document.getElementById("issue-labels").value
    .split(",")
    .map((l) => l.trim())
    .filter(Boolean);

  submitIssueBtn.disabled = true;
  submitIssueBtn.textContent = "Creating…";

  try {
    const res = await fetch(`${API}/issues`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, body: body || null, labels: labels.length ? labels : null }),
    });

    if (!res.ok) {
      formError.textContent = await parseErrorDetail(res);
      formError.hidden = false;
      return;
    }

    closePanel();
    await loadIssues();
  } catch {
    formError.textContent = "Can't reach the API server.";
    formError.hidden = false;
  } finally {
    submitIssueBtn.disabled = false;
    submitIssueBtn.textContent = "Submit new issue";
  }
});

loadIssues();
