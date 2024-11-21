import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/authContext';

import LandingPage from './pages/LandingPage/LandingPage';

function App()  {
  return (
    <>
      <Router>
        <AuthProvider>
            <Routes>
              <Route path="/" element={<LandingPage/>}/>
            </Routes>
        </AuthProvider>
      </Router>
    </>
  );
}

export default App;
