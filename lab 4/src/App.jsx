import { useState } from 'react';
import './App.css';

export default function App() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  function handleSubmit(event) {
    event.preventDefault();
    const trimmed = input.trim();
    if (trimmed) {
      setTodos([...todos, { id: Date.now(), text: trimmed, completed: false }]);
      setInput('');
    }
  }

  function toggleTodo(id) {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  }

  function removeTodo(id) {
    setTodos(todos.filter(todo => todo.id !== id));
  }

  function clearCompleted() {
    setTodos(todos.filter(todo => !todo.completed));
  }

  function editTodo(id, currentText) {
    const newText = window.prompt('Edit todo', currentText);
    if (newText !== null && newText.trim() !== '') {
      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, text: newText.trim() } : todo
      ));
    }
  }

  const remainingItems = todos.filter(todo => !todo.completed).length;

  return (
    <div className="page">
      <div className="app">
        <header className="app-header">
          <h1>Todo List</h1>
        </header>
        <form className="todo-form" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="insert work"
          />
          <button type="submit">Add</button>
        </form>

        <div className="todo-section">
          <ul className="todo-list">
            {todos.map(todo => (
              <li key={todo.id} className={`todo-item${todo.completed ? ' completed' : ''}`}>
                <button
                  type="button"
                  className="todo-checkbox"
                  aria-label="Toggle done"
                  onClick={() => toggleTodo(todo.id)}
                />
                <span className="todo-text">{todo.text}</span>
                <div className="todo-actions">
                  <button type="button" className="edit-btn" onClick={() => editTodo(todo.id, todo.text)}>Edit</button>
                  <button type="button" className="delete-btn" onClick={() => removeTodo(todo.id)}>Delete</button>
                </div>
              </li>
            ))}
          </ul>

          <footer className="card-footer">
            <span>{remainingItems} {remainingItems === 1 ? 'item' : 'items'} remaining</span>
            <button type="button" className="link-btn" onClick={clearCompleted}>
              Clear completed
            </button>
          </footer>
        </div>
      </div>
    </div>
  );
}
