import React, { useState } from 'react';
import './index.css';

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