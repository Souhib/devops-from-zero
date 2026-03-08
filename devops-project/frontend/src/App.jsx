import { useState, useEffect } from "react";

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  useEffect(() => {
    fetch("/api/tasks")
      .then((res) => res.json())
      .then(setTasks)
      .catch(console.error);
  }, []);

  const addTask = async (e) => {
    e.preventDefault();
    if (!newTask.trim()) return;

    const res = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTask }),
    });
    const task = await res.json();
    setTasks([...tasks, task]);
    setNewTask("");
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>DevOps Task List</h1>
      <form onSubmit={addTask}>
        <input
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Nouvelle tâche..."
          style={{ padding: 8, width: "70%" }}
        />
        <button type="submit" style={{ padding: 8, marginLeft: 8 }}>
          Ajouter
        </button>
      </form>
      <ul style={{ marginTop: 20 }}>
        {tasks.map((t) => (
          <li key={t.id} style={{ padding: 4 }}>
            {t.title}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
