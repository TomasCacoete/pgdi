import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../../auth/authContext';
import './LoginMobile.css';
import Logo from '../../assets/logo.svg';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const { loginUser } = useContext(AuthContext);

    const navigate = useNavigate();

    // Handle input change
    const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        if (name === 'username') {
            setUsername(value);
        } else if (name === 'password') {
            setPassword(value);
        }
    };

    // Handle login
    const handleLogin = async () => {
        try {
            const response = await loginUser(username, password);
            if (response.status === 200) {
                localStorage.setItem('authTokens', JSON.stringify(response.data));
            } else {
                console.log(response.detail);
            }
        } catch (error: any) {
            console.log('There was an internal error, please try again', error);
        }
    };

    // Navigate to the register page
    const handleRegisterRedirect = () => {
        navigate('/register');
    };

    return (
        <div className="LoginContainer">
            <div className="logo">
                <img src={Logo} alt="Logo" />
            </div>
            <div className="Main">
                <div className="usernamebox">
                    <label className="login">Username</label>
                    <input
                        className="inputboxes"
                        type="text"
                        name="username"
                        value={username}
                        onChange={handleInput}
                    />
                </div>
                <div className="passwordbox">
                    <label className="pass">Password</label>
                    <input
                        className="inputboxes"
                        type="password"
                        name="password"
                        value={password}
                        onChange={handleInput}
                    />
                </div>
                <button className="button-login" onClick={handleLogin}>
                    Login
                </button>
            </div>
            <div className="register-text">
            Register{' '}
            <a onClick={handleRegisterRedirect} style={{ cursor: 'pointer'}}>
                here
            </a>
            </div>
        </div>
    );
};

export default Login;
