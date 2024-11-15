import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import AuthContext from "../../auth/authContext";
import "./competitionSignUp.css";

const CompetitionSignUp: React.FC = () => {
    const [competitions, setCompetitions] = useState<any[]>([]); // List of competitions
    const [statusMessage, setStatusMessage] = useState<string>("");

    const { authTokens } = useContext(AuthContext);

    // Fetch all competitions
    useEffect(() => {
        const fetchCompetitions = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/pgdi_api/competitions/", {
                    headers: {
                        Authorization: `Bearer ${authTokens.access}`,
                    },
                });
                setCompetitions(response.data);
            } catch (error) {
                console.error("Error fetching competitions:", error);
                setStatusMessage("Failed to fetch competitions.");
            }
        };

        fetchCompetitions();
    }, [authTokens]);

    const handleSignUp = async (competitionId: number) => {
        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/pgdi_api/competition_signup/",
                { competition_id: competitionId },
                {
                    headers: {
                        Authorization: `Bearer ${authTokens.access}`,
                    },
                }
            );

            if (response.status === 201) {
                setStatusMessage("Successfully signed up for the competition!");
            } else {
                setStatusMessage("Failed to sign up for the competition.");
            }
        } catch (error) {
            console.error("Error signing up for competition:", error);
            setStatusMessage(error.response?.data?.error || "An error occurred.");
        }
    };

    return (
        <div className="competition-signup-container">
            <h2>Available Competitions</h2>
            {statusMessage && <p className="status-message">{statusMessage}</p>}
            <div className="competition-list">
                {competitions.map((competition) => (
                    <div key={competition.id} className="competition-item">
                        <h3>{competition.name}</h3>
                        <p>
                            <strong>Start:</strong> {new Date(competition.start_date).toLocaleString()}
                        </p>
                        <p>
                            <strong>End:</strong> {new Date(competition.end_date).toLocaleString()}
                        </p>
                        <button onClick={() => handleSignUp(competition.id)}>
                            Sign Up
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CompetitionSignUp;
