import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Registration.css';

function Registration() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegistration = async () => {
    try {
      const dataToSend = {
        username,
        password,
        email,
        created_at: 1, // Устанавливаем значение created_at на null
        last_auth: 1, // Устанавливаем значение last_auth на null
      };
  
      const response = await fetch('https://0bd4-2a01-4f9-2a-427-00-2.ngrok-free.app/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      });
  
      if (!response.ok) {
        const errorMessage = await response.text();
        throw new Error(errorMessage);
      }
  
      navigate('/login');
    } catch (error) {
      console.error('Ошибка во время регистрации:', error);
      setError(error.message || 'Не удалось зарегистрироваться');
    }
  };  

  return (
    <div className='container'>
      <h2>Registration</h2>
      <input
        className='input-regist'
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className='input-regist'
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <input
        className='input-regist'
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={handleRegistration} className='button'>Register</button>
      <Link to="/login">Login</Link>
      {error && <p>{error}</p>}
    </div>
  );
}

export default Registration;
