import React from 'react';
import './index.css';

const Header: React.FC = () => {
  return (
    <header>
      <h1>CycleTrack</h1>
      <p>Your Ultimate Cycling Companion</p>
    </header>
  );
}

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

const App: React.FC = () => {
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
      <Header />
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
    </div>
  );
}

export default App;