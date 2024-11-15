import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/authContext';
import Home from './Pages/HomePage/Home.tsx';
import Login from './Pages/LoginPage/Login';
import UPLOAD from './Pages/FileUpload/uploadFile.tsx'
import Competition from './Pages/CompetitonCreation/competition.tsx'
import CompetitionSignUp from './Pages/CompetitionSignUp/competitionSignUp.tsx'

function App()  {
  return (
    <>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/home" element={<Home />} />
            <Route path="/upload" element={<UPLOAD/>} />
            <Route path='/competition' element={<Competition/>}/>
            <Route path='/signUp_competition' element={<CompetitionSignUp/>}/>
          </Routes>
        </AuthProvider>
      </Router>
    </>
  );
}

export default App;
