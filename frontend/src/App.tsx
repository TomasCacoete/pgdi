import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/authContext';

function App()  {
  return (
    <>
      <Router>
        <AuthProvider>
            <Routes>
              <Route path="/" element={<div>Ola</div>}/>
            </Routes>
        </AuthProvider>
      </Router>
    </>
  );
}

export default App;
