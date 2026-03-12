import { useState } from 'react';
import './App.css';
import Login from './components/Login';
import Register from './components/Register';

function App() {
  const [currentForm, setCurrentForm] = useState('login');

  const toggleForm = (formName) => {
    setCurrentForm(formName);
  }

  return (
    <div className="app-container">
      {
        currentForm === 'login' ? 
          <Login onFormSwitch={toggleForm} /> : 
          <Register onFormSwitch={toggleForm} />
      }
    </div>
  );
}

export default App;
