import React, { useState, useContext } from 'react';
import AuthContext from '../../auth/authContext';
import './home.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


interface FeatureProps {
  title: string;
  description: string;
  buttonText: string;
  onClick: () => void;
}

const Feature: React.FC<FeatureProps> = ({ title, description, buttonText, onClick }) => {
  return (
    <div className="feature">
      <h2>{title}</h2>
      <p>{description}</p>
      <button onClick={onClick}>{buttonText}</button>
    </div>
  );
}

interface MenuItemProps {
  icon: string;
  text: string;
}

const MenuItem: React.FC<MenuItemProps> = ({ icon, text }) => (
  <div className="menu-item">
    <span className="icon">{icon}</span>
    <span className="text">{text}</span>
  </div>
);

const App: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const { authTokens } = useContext(AuthContext);

  const headers = { // se nao conseguir ler token pagina nao renderiza
    Authorization: `Bearer ${authTokens.access}`,
  };

  const {logoutUser} = useContext(AuthContext)

  const navigate = useNavigate()

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleStartRide = (): void => {
    alert('Ride tracking started!');
  };

  const handleViewStats = (): void => {
    alert('Viewing ride statistics...');
  };

  const handleFindRoutes = (): void => {
    alert('Searching for nearby routes...');
  };

  const getAllUsers = () => {

    axios.get('http://127.0.0.1:8000/pgdi_api/get_users/', { headers })
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.error("Error fetching users:", error.response ? error.response.data : error.message);
    });
  }

  const LogOut = () => {
    logoutUser();
    console.log('user logado')
    navigate('/login')
  }


  return (
    <div className="App">
      <header>
        <h1>Amateur's Tour</h1>
        <p>Your Flexible Cycling Competition</p>
      </header>
      <main>
        <Feature
          title="Track Your Ride"
          description="Record your cycling routes, distance, speed, and elevation gain."
          buttonText="Start Ride"
          onClick={handleStartRide}
        />
        <Feature
          title="Ride Statistics"
          description="View your cycling performance and progress over time."
          buttonText="View Stats"
          onClick={handleViewStats}
        />
        <Feature
          title="Discover Routes"
          description="Explore popular cycling routes in your area."
          buttonText="Find Routes"
          onClick={handleFindRoutes}
        />
        <Feature
          title="GetUsers"
          description="getusers"
          buttonText="get all users"
          onClick={getAllUsers}
        />
        <Feature
          title="Logout"
          description="logout"
          buttonText="logout"
          onClick={LogOut}
        />
      </main>
      <div className={`bottom-menu ${isMenuOpen ? 'open' : ''}`}>
        <button className="toggle-btn" onClick={toggleMenu}>
          {isMenuOpen ? '▼' : '▲'}
        </button>
        <div className="menu-items">
          <MenuItem icon="🏠" text="Home" />
          <MenuItem icon="📊" text="Dashboard" />
          <MenuItem icon="🚲" text="My Rides" />
          <MenuItem icon="🗺️" text="Routes" />
          <MenuItem icon="⚙️" text="Settings" />
        </div>
      </div>
    </div>
  );
}

export default App;