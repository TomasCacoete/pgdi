import { BrowserRouter as Router , Routes  , Route } from 'react-router-dom';
import { AuthProvider } from './auth/authContext';
import Home from './Pages/HomePage/Home.tsx'
import Login from './Pages/LoginPage/Login'

function App()  {

  return (
    <>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path='/login' element={<Login/>}/>
          </Routes>
        </AuthProvider>
      </Router>
    </>
  )
}

export default App;

