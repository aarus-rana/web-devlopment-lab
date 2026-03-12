import React, { useState } from 'react';
import Input from './Input';

function Register({ onFormSwitch }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Register Attempt: Username=${username}, Email=${email}, Password=${password}`);
  };

  return (
    <div className="auth-form-container">
      <h2>Register</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        <Input 
          label="Username" 
          type="text" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
        />
        <Input 
          label="Email" 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
        />
        <Input 
          label="Password" 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />
        <button type="submit" className="submit-btn">Register</button>
      </form>
      <button className="toggle-btn" onClick={() => onFormSwitch('login')}>
        Already have an account? Login
      </button>
    </div>
  );
}

export default Register;
