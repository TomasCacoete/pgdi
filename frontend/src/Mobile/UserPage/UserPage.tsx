import React, { useState, useEffect, useContext } from 'react';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';
import AuthContext from '../../auth/authContext';
import './UserPage.css';

import userphoto from '../../assets/user-photo.jpg'
import logo from '../../assets/logo2.svg';
import Navbar from '../Components/Navbar/Navbar';

const UserPage = () => {
    const { authTokens } = useContext(AuthContext);
    const {logoutUser} = useContext(AuthContext);   

    const headers = { // se nao conseguir ler token pagina nao renderiza
        Authorization: `Bearer ${authTokens.access}`,
    };

    const navigate = useNavigate();

    const [routes, setRoutes] = useState<string[]>([]);
    const [competitions, setCompetitions] = useState<any[]>([]);
    const [user, setUser] = useState<any>();


    useEffect(() => {
        const fetchRoutes = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/pgdi_api/user_routes/", {
                    headers: {
                        Authorization: `Bearer ${authTokens.access}`,
                    },
                });
                //delete /media/routes/ from response.data.files
                response.data.map((route: any) => {
                    route.file = route.file.replace("/media/routes/", "");
                });
                setRoutes(response.data);
                //console.log(routes)
            } catch (error) {
                console.error("Error fetching routes:", error);
            }
        };

        const fetchUserCompetitions = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/pgdi_api/user_competitions/", {
                    headers: {
                        Authorization: `Bearer ${authTokens.access}`,
                    },
                });
                setCompetitions(response.data);
            } catch (error) {
                console.error("Error fetching competitions:", error);
            }
        };

        const fetchUser = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/pgdi_api/user/", {
                    headers: {
                        Authorization: `Bearer ${authTokens.access}`,
                    },
                });
                setUser(response.data);
                //console.log(response.data);
            } catch (error) {
                console.error("Error fetching user:", error);
            }
        }


        fetchRoutes();
        fetchUserCompetitions();
        fetchUser();
    }, [authTokens]);

    const handleUploadRoutes = () => {
        navigate('/upload');
    };

    return (
        <>
        <div className="user-page-container">
            <div className="logo-user">  
                <img src={logo} alt="logo" />
            </div>
            <div className="header">
                <div className="profile-picture">
                    <img
                        src={userphoto}
                        alt="User Profile"
                        className="profile-img"
                    />
                </div>
                <div className="user-info">
                    <h2>{user?.first_name} {user?.last_name}</h2>
                </div>
            </div>

            <div className="upload-section">
                <button className="upload-button" onClick={handleUploadRoutes}>
                    Upload Routes
                </button>
            </div>

            <div className="routes-section">
                <h3>My Routes</h3>
                <div className="routes-list-scroll">
                    {routes.map((route) => (
                        <div key={route.id} className="route-item-user">
                            <h4>{route.file}</h4>
                        </div>
                    ))}
                </div>
            </div>
            <div className="competition-section1">
                <h3>Signed Competitions</h3>
                <div className="competition-list-scroll">
                    {competitions.map((competition) => (
                        <div key={competition.id} className="competition-item1">
                            <h4>{competition.name}</h4>
                            <p>{competition.description}</p>
                        </div>
                    ))}
                </div>
            </div>
            <div className="logout-section">
                <button className="logout-button" onClick={logoutUser}>
                    Logout
                </button>
            </div>
        </div>
        <Navbar />  
        </>
    );
};

export default UserPage;
