// App.jsx — Le composant principal du frontend
// C'est la page que l'utilisateur voit dans son navigateur.
// Elle affiche la liste des tâches et permet d'en ajouter.

import { useState, useEffect } from "react";

function App() {
  // useState = stocker des données qui peuvent changer (React les réaffiche automatiquement)
  const [tasks, setTasks] = useState([]); // Liste des tâches (vide au départ)
  const [newTask, setNewTask] = useState(""); // Le texte tapé dans le champ input

  // useEffect = exécuter du code au chargement de la page
  // Ici : appeler GET /api/tasks pour récupérer les tâches depuis le backend
  useEffect(() => {
    fetch("/api/tasks") // Appel HTTP vers le backend
      .then((res) => res.json()) // Convertir la réponse en JSON
      .then(setTasks) // Stocker les tâches dans le state
      .catch(console.error); // Afficher l'erreur dans la console si ça échoue
  }, []); // [] = exécuter une seule fois, au chargement

  // Fonction appelée quand l'utilisateur soumet le formulaire
  const addTask = async (e) => {
    e.preventDefault(); // Empêcher le rechargement de la page (comportement par défaut d'un formulaire)
    if (!newTask.trim()) return; // Ne rien faire si le champ est vide

    // Appel HTTP POST vers le backend pour créer la tâche
    const res = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" }, // On envoie du JSON
      body: JSON.stringify({ title: newTask }), // Le corps de la requête
    });
    const task = await res.json(); // Le backend retourne la tâche créée
    setTasks([...tasks, task]); // Ajouter la nouvelle tâche à la liste affichée
    setNewTask(""); // Vider le champ input
  };

  // Le JSX ci-dessous décrit ce qui est affiché dans le navigateur
  // C'est du HTML mélangé avec du JavaScript (syntaxe React)
  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>DevOps Task List</h1>
      {/* Formulaire pour ajouter une tâche */}
      <form onSubmit={addTask}>
        <input
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)} // Met à jour le state à chaque frappe
          placeholder="Nouvelle tâche..."
          style={{ padding: 8, width: "70%" }}
        />
        <button type="submit" style={{ padding: 8, marginLeft: 8 }}>
          Ajouter
        </button>
      </form>
      {/* Liste des tâches — .map() parcourt le tableau et crée un <li> par tâche */}
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
