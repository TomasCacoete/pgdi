import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/authContext';
import Home from './Pages/HomePage/Home.tsx';
import Login from './Pages/LoginPage/Login';
import MapsPage from './Pages/Maps_API_Tests/maps.tsx';
import { APIProvider } from '@vis.gl/react-google-maps';

function App()  {
  return (
    <>
      <Router>
        <AuthProvider>
          <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
            <Routes>
              <Route path="/" element={<Login />} />
              <Route path="/home" element={<Home />} />
              <Route path="/map" element={<MapsPage />} />
            </Routes>
          </APIProvider>
        </AuthProvider>
      </Router>
    </>
  );
}

export default App;
