import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../../auth/authContext';
import './LoginMobile.css';
import Logo from '../../assets/logo.svg'

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const {loginUser} = useContext(AuthContext)
    
    const navigate = useNavigate()
    // Handle input change
    const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target; // Destructure to get the name and value
        if (name === 'username') {
            setUsername(value); // Update username state
        } else if (name === 'password') {
            setPassword(value); // Update password state
        }
    };

    const handleLogin = async () =>{
        
        try {
            const response = await loginUser(username, password); // Call loginUser with username and password
            if (response.status === 200) {
                localStorage.setItem('authTokens', JSON.stringify(response.data));
                navigate('/home')
            } else {
                console.log(response.detail); // Set error if status code is not 200
            }
          } catch (error: any) {
                console.log("There was an internal error, please try again",error) // Generic error message for unexpected errors
                // Log the actual error for debugging
          }
    }

    return (
        <div className="Wrapper">
        <div className="LoginContainer">
            <div className="logo"><img src={Logo} alt="Logo" /></div>
            <div className="Main">
            <div className="usernamebox">
                    <label className="login">Username</label>
                    <input 
                        className='inputboxes'
                        type="text" 
                        name="username" // Adding name attribute for identification
                        value={username} 
                        onChange={handleInput} // Attach the handleInput function
                    />
                </div>
                <div className="passwordbox">
                    <label className="pass">Password</label>
                    <input 
                        className='inputboxes'
                        type="password" // Changed to type="password" for security
                        name="password" // Adding name attribute for identification
                        value={password} 
                        onChange={handleInput} // Attach the handleInput function
                    />
                </div>
                <button className='button-login' onClick={handleLogin}>Login</button>
            </div>
        </div>
        </div>
    );
}

export default Login;
