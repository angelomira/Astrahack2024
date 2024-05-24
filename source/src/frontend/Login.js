// Login.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    const data = {
      username: username,
      password: password,
    };

    try {
      console.log('Отправка запроса на вход:', JSON.stringify(data));

      const response = await fetch('https://0bd4-2a01-4f9-2a-427-00-2.ngrok-free.app/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        credentials: 'include', // Включение куки в запрос
      });

      const responseData = await response.json();
      console.log('Ответ сервера:', responseData);

      if (response.ok) {
        if (responseData.user_id && responseData.token) {
          // Сохраняем токен и информацию о пользователе в localStorage
          localStorage.setItem('loggedInUser', JSON.stringify({ id: responseData.user_id, username }));
          localStorage.setItem('token', responseData.token);
          console.log('Локальное хранилище пройдено');
          navigate('/chat'); // Переход на страницу чата после успешного входа
          console.log('Произведен переход на страницу "chat"');
        } else {
          setError('Ошибка при аутентификации');
        }
      } else {
        setError(responseData.message || 'Не удалось войти');
      }
    } catch (error) {
      console.error('Ошибка:', error);
      setError('Не удалось войти');
    }
  };

  return (
    <div className='container'>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          className='input-login'
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className='input-login'
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className='button'>Login</button>
      </form>
      <Link to="/registration">Registration</Link>
      {error && <p>{error}</p>}
    </div>
  );
}

export default Login;
