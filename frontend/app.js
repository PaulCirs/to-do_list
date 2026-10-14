// En local (front sur le port 5500), on appelle l'API directement sur le port 8000.
// Plus tard (Docker/Kubernetes), nginx redirigera "/api" vers l'API : même adresse que le front.
const API_URL = location.port === "5500" ? "http://localhost:8000/api" : "/api";

const list = document.getElementById("todos");
const form = document.getElementById("new-todo");
const input = document.getElementById("title");
const errorBox = document.getElementById("error");

async function request(path, options = {}) {
  const res = await fetch(API_URL + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`Erreur API : ${res.status}`);
  return res.status === 204 ? null : res.json();
}

function showError(err) {
  errorBox.textContent = err.message;
  errorBox.hidden = false;
}

async function refresh() {
  try {
    const todos = await request("/todos");
    errorBox.hidden = true;
    list.replaceChildren(...todos.map(renderTodo));
  } catch (err) {
    showError(err);
  }
}

function renderTodo(todo) {
  const li = document.createElement("li");

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = todo.done;
  checkbox.onchange = () =>
    request(`/todos/${todo.id}`, { method: "PATCH", body: JSON.stringify({ done: checkbox.checked }) })
      .then(refresh, showError);

  const label = document.createElement("span");
  label.textContent = todo.title;
  if (todo.done) label.className = "done";

  const del = document.createElement("button");
  del.textContent = "✕";
  del.title = "Supprimer";
  del.onclick = () => request(`/todos/${todo.id}`, { method: "DELETE" }).then(refresh, showError);

  li.append(checkbox, label, del);
  return li;
}

form.onsubmit = async (event) => {
  event.preventDefault();
  try {
    await request("/todos", { method: "POST", body: JSON.stringify({ title: input.value }) });
    input.value = "";
    refresh();
  } catch (err) {
    showError(err);
  }
};

refresh();
