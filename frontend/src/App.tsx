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
            <Route path='/signUp_competition' element={<CompetitionSignUp/>}/>
            <Route path='/submission' element={<CompetitionSubmission/>}/>
          </Routes>
        </AuthProvider>
      </Router>
    </>
  );
}

export default App;
