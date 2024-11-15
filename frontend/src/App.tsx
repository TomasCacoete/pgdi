import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/authContext';
import Home from './Pages/HomePage/Home.tsx';
import Login from './Pages/LoginPage/Login';
import UPLOAD from './Pages/FileUpload/uploadFile.tsx'

function App()  {
  return (
    <>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/home" element={<Home />} />
            <Route path="/upload" element={<UPLOAD/>} />
          </Routes>
        </AuthProvider>
      </Router>
    </>
  );
}

export default App;
