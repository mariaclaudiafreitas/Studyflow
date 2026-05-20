import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await api.post('/users/register', { email, password });
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao registrar.');
    }
  };

  return (
    <div className="glass-panel" style={{ maxWidth: '400px', margin: '100px auto' }}>
      <h2 style={{ marginBottom: '1rem' }}>Criar Conta</h2>

      {error && <p style={{ color: 'red', marginBottom: '1rem' }}>{error}</p>}

      <form onSubmit={handleRegister}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ width: '100%', marginBottom: '0.5rem', padding: '0.5rem' }}
        />

        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ width: '100%', marginBottom: '0.5rem', padding: '0.5rem' }}
        />

        <button type="submit" className="btn" style={{ width: '100%' }}>
          Registrar
        </button>
      </form>

      <p style={{ marginTop: '1rem', textAlign: 'center' }}>
        Já tem conta? <Link to="/login">Faça Login</Link>
      </p>
    </div>
  );
};

export default Register;