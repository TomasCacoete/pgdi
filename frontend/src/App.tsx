import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/authContext';
import Home from './Pages/HomePage/Home.tsx';
import Login from './Pages/LoginPage/Login';
import UPLOAD from './Pages/FileUpload/uploadFile.tsx'
import Competition from './Pages/CompetitonCreation/competition.tsx'
import CompetitionSignUp from './Pages/CompetitionSignUp/competitionSignUp.tsx'
import CompetitionSubmission from './Pages/CompetitionSubmission/submission.tsx'

import LoginMobile from './Mobile/LoginPageMobile/LoginMobile.tsx';
import UploadRoutesMobile from './Mobile/UserUploadRoutes/UploadRoutesMobile.tsx';
import CompetitionsMobile from './Mobile/MobileCompetitions/MobileCompetitions.tsx';
import CreateCompetitionsMobile from './Mobile/CreateCompetitionsMobile/CreateCompetitionsMobile.tsx';
import CompetitionSubmissonsMobile from './Mobile/CompetitionsSubmissions/CompetitionSubmissions.tsx';
import RegisterMobile from './Mobile/RegisterMobile/Register.tsx';
import UserPage from './Mobile/UserPage/UserPage.tsx';

function App()  {
  return (
    <>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<LoginMobile />} />
            <Route path="/home" element={<Home />} />
            <Route path="/upload" element={<UploadRoutesMobile/>} />
            <Route path='/competition' element={<CompetitionsMobile/>}/>
            <Route path='/submission' element={<CompetitionSubmissonsMobile/>}/>
            <Route path='/create_competition' element={<CreateCompetitionsMobile/>}/>
            <Route path="/register" element={<RegisterMobile/>} />
            <Route path="/user" element={<UserPage />} />
          </Routes>
        </AuthProvider>
      </Router>
    </>
  );
}

export default App;
