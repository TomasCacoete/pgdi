import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import AuthContext from "../../auth/authContext";
import "./CompetitionSubmissons.css";

import Navbar from "../Components/Navbar/Navbar";
import Logo from "../../assets/logo2.svg";
import { useNavigate } from "react-router-dom";

const MyCompetitions: React.FC = () => {
    const [competitions, setCompetitions] = useState<any[]>([]);
    const [statusMessage, setStatusMessage] = useState<string>("");
    const [fileInputs, setFileInputs] = useState<{ [key: number]: File | null }>({});

    const { authTokens } = useContext(AuthContext);
    const navigate = useNavigate();

    // Fetch competitions where the user is signed up
    useEffect(() => {
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
                setStatusMessage("Failed to fetch your competitions.");
            }
        };

        fetchUserCompetitions();
    }, [authTokens]);

    // Handle file selection for a specific competition
    const handleFileChange = (competitionId: number, file: File | null) => {
        setFileInputs((prev) => ({
            ...prev,
            [competitionId]: file,
        }));
    };

    // Handle file submission
    const handleFileSubmit = async (competitionId: number) => {
        const file = fileInputs[competitionId];
        if (!file) {
            setStatusMessage("Please select a file before submitting.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("competition_id", competitionId.toString());

        try {
            const response = await axios.post("http://127.0.0.1:8000/pgdi_api/upload_submission/", formData, {
                headers: {
                    Authorization: `Bearer ${authTokens.access}`,
                    "Content-Type": "multipart/form-data",
                },
            });

            if (response.status === 201) {
                setStatusMessage(`File uploaded successfully for competition: ${competitionId}`);
            } else {
                setStatusMessage(`Failed to upload file for competition: ${competitionId}`);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            setStatusMessage(`An error occurred while uploading the file for competition: ${competitionId}`);
        }
    };

    const handleClassification = (competitionId: string) => {
        navigate(`/scoreboard/${competitionId}`);
    }

    return (
        <div className="my-competitions-container">
            <div className="logo"> <img src={Logo}></img> </div>
            <div className="header-comp">My Competitions</div>
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
                        <div className="competition-info">
                            <label htmlFor={`file-${competition.id}`}>
                                Upload GPX File:
                                <input
                                    id={`file-${competition.id}`}
                                    type="file"
                                    accept=".gpx"
                                    onChange={(e) => handleFileChange(competition.id, e.target.files?.[0] || null)}
                                />
                                
                            </label>
                            <button onClick={() => handleFileSubmit(competition.id)}>Submit</button>
                            <button onClick={() => handleClassification(competition.id)}>See Classifications</button>
                        </div>
                    </div>
                ))}
            </div>
            <Navbar />
        </div>
    );
};

export default MyCompetitions;
