import React from 'react';

function Input({ label, type, value, onChange }) {
  return (
    <div className="form-group">
      <label>{label}</label>
      <input 
        type={type} 
        value={value} 
        onChange={onChange} 
        required 
      />
    </div>
  );
}

export default Input;
