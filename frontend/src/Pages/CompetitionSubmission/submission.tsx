import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import AuthContext from "../../auth/authContext";
import "./submission.css";

const MyCompetitions: React.FC = () => {
    const [competitions, setCompetitions] = useState<any[]>([]); // List of user competitions
    const [statusMessage, setStatusMessage] = useState<string>("");
    const [fileInput, setFileInput] = useState<{ [key: number]: File | null }>({});
    
    const { authTokens } = useContext(AuthContext);

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
                console.log(response.data)
            } catch (error) {
                console.error("Error fetching competitions:", error);
                setStatusMessage("Failed to fetch your competitions.");
            }
        };

        fetchUserCompetitions();
    }, [authTokens]);

    const handleFileChange = (competitionId: number, file: File | null) => {
        setFileInput((prev) => ({
            ...prev,
            [competitionId]: file,
        }));
    };

    const handleSubmit = async (competitionId: number) => {
        const file = fileInput[competitionId];
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
                setStatusMessage("File uploaded successfully!");
            } else {
                setStatusMessage("Failed to upload file.");
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            setStatusMessage(error.response?.data?.error || "An error occurred.");
        }
    };

    return (
        <div className="my-competitions-container">
            <h2>My Competitions</h2>
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
                        <div>
                            <label htmlFor={`file-${competition.id}`}>
                                Upload GPX File:
                                <input
                                    id={`file-${competition.id}`}
                                    type="file"
                                    accept=".gpx"
                                    onChange={(e) => handleFileChange(competition.id, e.target.files?.[0] || null)}
                                />
                            </label>
                            <button onClick={() => handleSubmit(competition.id)}>Submit</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default MyCompetitions;
