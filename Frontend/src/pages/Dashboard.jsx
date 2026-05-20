import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskMin, setNewTaskMin] = useState('');
  const navigate = useNavigate();
  useEffect(() => {
    fetchData();
  }, []);
  const fetchData = async () => {
    try {
      const taskRes = await api.get('/tasks/');
      setTasks(taskRes.data);
      // const subRes = await api.get('/subjects/');
      // setSubjects(subRes.data);
    } catch (err) {
      if(err.response && err.response.status === 401) {
        navigate('/login');
      }
    }
  };
  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };
  const createTask = async (e) => {
    e.preventDefault();
    if (!newTaskTitle) return;
    try {
      await api.post('/tasks/', {
        title: newTaskTitle,
        estimated_minutes: parseInt(newTaskMin) || 60
      });
      setNewTaskTitle('');
      setNewTaskMin('');
      fetchData();
    } catch(err) {
      console.error("Erro ao criar tarefa", err);
    }
  };
  const toggleTaskStatus = async (task) => {
    try {
      const newStatus = task.status === 'PENDING' ? 'COMPLETED' : 'PENDING';
      await api.put(`/tasks/${task.id}`, { status: newStatus });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };
  const deleteTask = async (taskId) => {
    try {
      await api.delete(`/tasks/${taskId}`);
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };
  // Progress Calculation
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.status === 'COMPLETED').length;
  const progressPercent = totalTasks === 0 ? 0 : Math.round((completedTasks / totalTasks) * 100);
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>StudyFlow Dashboard</h1>
        <button onClick={handleLogout} className="btn" style={{ background: '#EF4444' }}>Sair</button>
      </div>
      
      <div className="glass-panel" style={{ marginBottom: '2rem' }}>
        <h2>Weekly Progress</h2>
        <h2>Progresso Geral: {progressPercent}%</h2>
        <div style={{ background: '#ddd', height: '20px', borderRadius: '10px', marginTop: '1rem', overflow: 'hidden' }}>
          <div style={{ background: 'var(--secondary)', height: '100%', width: '45%', transition: 'width 0.5s' }}></div>
          <div style={{ background: 'var(--secondary)', height: '100%', width: `${progressPercent}%`, transition: 'width 0.5s' }}></div>
        </div>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
        <div className="glass-panel">
          <h2>Subjects</h2>
          <p style={{ marginTop: '1rem', color: '#666' }}>No subjects added yet.</p>
          <h2>Adicionar Tarefa</h2>
          <form onSubmit={createTask} style={{ marginTop: '1rem' }}>
            <input 
              type="text" 
              placeholder="Título da Tarefa" 
              className="input" 
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              required
            />
            <input 
              type="number" 
              placeholder="Minutos Estimados (IA divide se > 120)" 
              className="input" 
              value={newTaskMin}
              onChange={(e) => setNewTaskMin(e.target.value)}
            />
            <button type="submit" className="btn" style={{ width: '100%' }}>Adicionar</button>
          </form>
        </div>
        <div className="glass-panel">
          <h2>Tasks</h2>
          <p style={{ marginTop: '1rem', color: '#666' }}>No tasks added yet.</p>
          <h2>Minhas Tarefas</h2>
          {tasks.length === 0 && <p style={{ marginTop: '1rem', color: '#666' }}>Nenhuma tarefa adicionada.</p>}
          <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {tasks.map(task => (
              <div key={task.id} style={{ 
                display: 'flex', justifyContent: 'space-between', alignItems: 'center', 
                padding: '1rem', background: 'rgba(255,255,255,0.5)', borderRadius: '8px',
                borderLeft: task.status === 'COMPLETED' ? '5px solid var(--secondary)' : '5px solid #F59E0B'
              }}>
                <div>
                  <h4 style={{ textDecoration: task.status === 'COMPLETED' ? 'line-through' : 'none' }}>
                    {task.title} {task.is_ai_suggested && <span style={{fontSize: '0.8rem', color: 'var(--primary)'}}>✨ IA</span>}
                  </h4>
                  <small>{task.estimated_minutes} min</small>
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button onClick={() => toggleTaskStatus(task)} className="btn" style={{ padding: '0.5rem', background: task.status === 'COMPLETED' ? '#6B7280' : 'var(--secondary)' }}>
                    {task.status === 'COMPLETED' ? 'Desfazer' : 'Concluir'}
                  </button>
                  <button onClick={() => deleteTask(task.id)} className="btn" style={{ padding: '0.5rem', background: '#EF4444' }}>X</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
export default Dashboard;