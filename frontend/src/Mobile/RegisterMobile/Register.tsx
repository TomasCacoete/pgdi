import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css';
import Logo from '../../assets/logo.svg';
import axios from 'axios';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        phone_no: '',
        password: '',
    });
    const [statusMessage, setStatusMessage] = useState('');
    const navigate = useNavigate();

    // Handle input changes
    const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    // Handle registration
    const handleRegister = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/auth/register/', formData);
            if (response.status === 201) {
                setStatusMessage('Registration successful! Redirecting to login...');
                setTimeout(() => navigate('/'), 2000); 
            } else {
                setStatusMessage('Registration failed. Please try again.');
            }
        } catch (error: any) {
            console.error('Error during registration:', error);
            setStatusMessage(
                error.response?.data?.detail || 'An unexpected error occurred. Please try again.'
            );
        }
    };

    return (
        <div className="RegisterContainer">
            <div className="logo">
                <img src={Logo} alt="Logo" />
            </div>
            <div className="MainRegister">
                {statusMessage && <p className="status-message">{statusMessage}</p>}
                <div className="inputbox">
                    <label>Username</label>
                    <input
                        className="inputboxes"
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleInput}
                    />
                </div>
                <div className="inputbox">
                    <label>First Name</label>
                    <input
                        className="inputboxes"
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleInput}
                    />
                </div>
                <div className="inputbox">
                    <label>Last Name</label>
                    <input
                        className="inputboxes"
                        type="text"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleInput}
                    />
                </div>
                <div className="inputbox">
                    <label>Email</label>
                    <input
                        className="inputboxes"
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInput}
                    />
                </div>
                <div className="inputbox">
                    <label>Phone Number</label>
                    <input
                        className="inputboxes"
                        type="tel"
                        name="phone_no"
                        value={formData.phone_no}
                        onChange={handleInput}
                    />
                </div>
                <div className="inputbox">
                    <label>Password</label>
                    <input
                        className="inputboxes"
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleInput}
                    />
                </div>
                <button className="button-register" onClick={handleRegister}>
                    Register
                </button>
            </div>
        </div>
    );
};

export default Register;
