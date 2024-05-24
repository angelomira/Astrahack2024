import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './Chat.css';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [users, setUsers] = useState([]);
  const [activeUser, setActiveUser] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();
  const intervalIdRef = useRef(null);
  const [error, setError] = useState(null);

  const getToken = () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
    return token;
  };

  async function fetchUsers(count = 10) {
    try {
      const token = getToken();

      const response = await fetch(`https://0bd4-2a01-4f9-2a-427-00-2.ngrok-free.app/get-users?count=${count}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      const users = await response.json();
      console.log('Список пользователей:', users);
      setUsers(users);

      const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
      setActiveUser(loggedInUser);

      navigate('/chat');
    } catch (error) {
      console.error('Ошибка при выполнении запроса:', error);
    }
  }

  useEffect(() => {
    fetchUsers();
  }, []);

  useEffect(() => {
    if (selectedUser) {
      setMessages([]);
      fetchMessages();

      // Если предыдущий интервал существует, очищаем его
      if (intervalIdRef.current) {
        clearInterval(intervalIdRef.current);
      }

      // Устанавливаем новый интервал и сохраняем его в useRef
      const id = setInterval(fetchMessages, 5000);
      intervalIdRef.current = id;
    } else {
      setMessages([]);
      clearInterval(intervalIdRef.current); // Очищаем интервал при отсутствии выбранного пользователя
    }
  }, [selectedUser]);

  const fetchMessages = async () => {
    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
    if (!loggedInUser) {
      setError('User not logged in');
      return;
    }

    if (!selectedUser) {
      return;
    }

    try {
      const response = await fetch(`https://0bd4-2a01-4f9-2a-427-00-2.ngrok-free.app/peer/${selectedUser.id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        credentials: 'include',
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Unauthorized: Please log in again.');
        } else if (response.status === 404) {
          throw new Error('Messages not found');
        }
        throw new Error('Failed to fetch messages');
      }

      const data = await response.json();
      setMessages(data);
    } catch (error) {
      setError(error.message);
    }
  };

  const sendMessage = async () => {
    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
    if (loggedInUser && currentMessage.trim() !== '' && selectedUser) {
      const newMessage = {
        sender_id: loggedInUser.id,
        receiver_id: selectedUser.id,
        content: currentMessage,
      };
      console.log('Sending message:', newMessage);
      try {
        const response = await fetch(`https://0bd4-2a01-4f9-2a-427-00-2.ngrok-free.app/peer/${loggedInUser.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          credentials: 'include',
          body: JSON.stringify(newMessage),
        });
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error('Unauthorized: Please log in again.');
          }
          throw new Error('Failed to send message');
        }
        setCurrentMessage('');
        setMessages(prevMessages => [...prevMessages, newMessage]);
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('loggedInUser');
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredUsers = users.filter((user) =>
    user.username.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatTimestamp = (timestamp) => {
    if (!timestamp || typeof timestamp !== 'string') {
      return 'Invalid Timestamp';
    }

    const [datePart, timePart] = timestamp.split(' ');
    const [day, month, year] = datePart.split('-');
    const [hours, minutes, seconds] = timePart.split(':');
    const date = new Date(year, month - 1, day, hours, minutes, seconds);
    if (isNaN(date.getTime())) return 'Invalid Date';
    const formattedTime = `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    return formattedTime;
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="users-panel">
        <h2>Users</h2>
        <input
          type="text"
          value={searchTerm}
          onChange={handleSearchChange}
          placeholder="Search users..."
          className="search-input"
        />
        <ul>
          {filteredUsers.map((user) => (
            user.id !== activeUser?.id && (
              <li key={user.id} onClick={() => setSelectedUser(user)}>
                {user.username}
              </li>
            )
          ))}
        </ul>
        {activeUser && (
          <div className="logged-in-user">
            <h3>Logged in as:</h3>
            <p>{activeUser.username}</p>
          </div>
        )}
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </div>
      <div className="chat-panel">
        <div className="chat-header">
          {selectedUser && <h3>Chat with {selectedUser.username}</h3>}
        </div>
  
        <div className="message-history">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender_id === JSON.parse(localStorage.getItem('loggedInUser')).id ? 'sent' : 'received'}`}
            >
              <div className="message-content">{message.content}</div>
              <div className={`message-timestamp ${message.sender_id === JSON.parse(localStorage.getItem('loggedInUser')).id ? 'message-timestamp-sent' : 'message-timestamp-received'}`}>
                {formatTimestamp(message.timestamp)}
              </div>
            </div>
          ))}
        </div>
  
        <form onSubmit={(e) => e.preventDefault()} className="message-form">
          <input
            type="text"
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            placeholder="Type your message..."
            className="message-input"
            onKeyDown={handleKeyDown}
          />
          <button type="button" onClick={sendMessage} className="send-button">
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default Chat;
