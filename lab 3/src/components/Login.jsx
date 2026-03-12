import React, { useState } from 'react';
import Input from './Input';

function Login({ onFormSwitch }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Login Attempt: Username=${username}, Password=${password}`);
  };

  return (
    <div className="auth-form-container">
      <h2>Login</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        <Input 
          label="Username" 
          type="text" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
        />
        <Input 
          label="Password" 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />
        <button type="submit" className="submit-btn">Login</button>
      </form>
      <button className="toggle-btn" onClick={() => onFormSwitch('register')}>
        Need an account? Register
      </button>
    </div>
  );
}

export default Login;
