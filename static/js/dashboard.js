const taskList = document.getElementById("taskList");
const API_BASE = "http://127.0.0.1:5000"; // Flask Server

// Create Task Element
function createTaskElement(title, description, due_date) {
  const li = document.createElement("li");
  li.className = "p-4 border rounded flex justify-between items-center";

  li.innerHTML = `
    <div>
      <h3 class="font-semibold">${title}</h3>
      <p class="text-sm text-gray-600">${description}</p>
      <p class="text-xs text-gray-500">Due: ${due_date}</p>
      <p class="text-xs status-label text-yellow-600 font-semibold">Status: Pending</p>
    </div>
    <div class="flex items-center space-x-2">
      <button class="toggle-status bg-yellow-500 text-white px-2 py-1 rounded">Mark Done</button>
      <button class="delete-task bg-red-500 text-white px-2 py-1 rounded">Delete</button>
    </div>
  `;

  // Toggle Status
  li.querySelector(".toggle-status").addEventListener("click", (e) => {
    const statusLabel = li.querySelector(".status-label");
    const button = e.target;

    if (statusLabel.textContent.includes("Pending")) {
      statusLabel.textContent = "Status: Done";
      statusLabel.classList.replace("text-yellow-600", "text-green-600");
      button.textContent = "Mark Pending";
      button.classList.replace("bg-yellow-500", "bg-green-500");
    } else {
      statusLabel.textContent = "Status: Pending";
      statusLabel.classList.replace("text-green-600", "text-yellow-600");
      button.textContent = "Mark Done";
      button.classList.replace("bg-green-500", "bg-yellow-500");
    }
  });

li.querySelector(".delete-task").addEventListener("click", async (e) => {
  const deleteButton = e.target;
  try {
    const response = await fetch(`${API_BASE}/delete`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
      credentials: "include"
    });
    const data = await response.json();
    if (response.ok) {
      li.remove();
      alert(data.message || "Task deleted!");
    } else {
      alert(data.error || "Failed to delete task");
    }
  } catch (err) {
    console.log("Error:", err);
    alert("Failed to delete");
  }
});

return li;
};

// Submit handler
async function addTasks(event) {
  event.preventDefault();

  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;
  const dueDate = document.getElementById("due_date").value;
  try {

    const response = await fetch(`${API_BASE}/create-task`, {
      method: "POST",
      headers: { "Content-Type": "application/json"},
      body: JSON.stringify({ title, description, due_date: dueDate }),
      credentials: "include"
    });

    const data = await response.json();
    console.log("Backend response:", data);

    // Add task to UI immediately
    const taskElement = createTaskElement(title, description, dueDate);
    taskList.appendChild(taskElement);

    // Clear form
    event.target.reset();
    alert(data.message || "Task created!");
  } catch (err) {
    console.error("Error:", err);
    alert("Failed to create task");
  }
}

// Attach listener
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("taskForm").addEventListener("submit", addTasks);
});

// Functions to load all user tasks
async function loadUserTasks(){
    const response = await fetch(`${API_BASE}/read`, {
        method: "GET",
        headers: {"Content-Type": "application/json"},
        credentials: "include"
    });

    const data = await response.json();

    const container = document.getElementById("taskList");
    container.innerHTML = "";  // clear old tasks

    if (data.tasks && data.tasks.length > 0) {
        data.tasks.forEach(task => {
            const taskEl = createTaskElement(task.title, task.description, task.due_date);
            container.appendChild(taskEl);
        });
    } else {
        container.innerHTML = "<p>No tasks yet.</p>";
    }
}

document.addEventListener("DOMContentLoaded", () => {
  loadUserTasks();
});
