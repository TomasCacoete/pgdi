import React, { useState, useEffect, useContext, useCallback } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import AuthContext from "../../auth/authContext";
import "./Scoreboard.css";

import logo from "../../assets/logo2.svg";
import Navbar from "../Components/Navbar/Navbar";

const Scoreboard: React.FC = () => {    

    const { authTokens } = useContext(AuthContext);
    const { id } = useParams();

    const [scoreboard, setScoreboard] = useState<any[]>([]);
    const [statusMessage, setStatusMessage] = useState<string>("");
    const competitionId = parseInt(id);

    const fetchScoreboard = useCallback(async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/pgdi_api/get_competition_scores/', {
                headers: {
                    Authorization: `Bearer ${authTokens.access}`,
                },
                params: {
                    competition_id: competitionId,
                },
            });
            setScoreboard(response.data);
            console.log(response.data);
        } catch (error) {
            console.error("Error fetching scoreboard:", error);
            setStatusMessage("Failed to fetch the scoreboard.");
        }
    }, [authTokens, competitionId]);

    useEffect(() => {
        fetchScoreboard();
    }, [fetchScoreboard]);

    return (
        <div className="scoreboard-page">
            <div className="logo-score"><img src={logo} alt="Logo" /></div>
            <div className="header-scoreboard">Classification</div>
            {statusMessage && <p className="status-message">{statusMessage}</p>}
            <div className="scoreboard-upper">
                <p className="rank">Rank</p>
                <p className="name">Name</p>
                <p className="score">Time</p>
            </div>
            <div className="table-scoreboard">
                {scoreboard.map((item, index) => (
                    <div key={index} className="scoreboard-item">
                        <p className="rank">{index + 1}</p>
                        <p className="name">{item.user}</p>
                        <p className="score">{item.time}</p>
                    </div>
                ))}
            </div>
            <Navbar />
        </div>
    );
}

export default Scoreboard;