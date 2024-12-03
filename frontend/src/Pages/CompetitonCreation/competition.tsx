import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import AuthContext from "../../auth/authContext";
import "./competition.css";

const CompetitionCreation: React.FC = () => {
    const [name, setName] = useState<string>("");
    const [startDate, setStartDate] = useState<string>("");
    const [endDate, setEndDate] = useState<string>("");
    const [routes, setRoutes] = useState<any[]>([]); // Store all user routes
    const [selectedRoutes, setSelectedRoutes] = useState<number[]>([]); // Store selected route IDs
    const [statusMessage, setStatusMessage] = useState<string>("");

    const { authTokens } = useContext(AuthContext);

    // Fetch user routes on component mount
    useEffect(() => {
        const fetchRoutes = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/pgdi_api/user_routes/", {
                    headers: {
                        Authorization: `Bearer ${authTokens.access}`,
                    },
                });
                setRoutes(response.data);
                console.log(response.data)
            } catch (error) {
                console.error("Error fetching routes:", error);
            }
        };

        fetchRoutes();
    }, [authTokens]);

    const handleCreateCompetition = async () => {
        if (!name || !startDate || !endDate) {
            alert("Please fill all fields.");
            return;
        }

        try {
            const data = {
                name,
                start_date: startDate,
                end_date: endDate,
                routes: selectedRoutes,
            };

            const response = await axios.post("http://127.0.0.1:8000/pgdi_api/create_competition/", data, {
                headers: {
                    Authorization: `Bearer ${authTokens.access}`,
                },
            });

            if (response.status === 201) {
                setStatusMessage("Competition created successfully!");
                // Clear form
                setName("");
                setStartDate("");
                setEndDate("");
                setSelectedRoutes([]);
            } else {
                setStatusMessage("Failed to create competition.");
            }
        } catch (error) {
            console.error("Error creating competition:", error);
            setStatusMessage("An error occurred while creating the competition.");
        }
    };

    const toggleRouteSelection = (routeId: number) => {
        setSelectedRoutes((prev) =>
            prev.includes(routeId) ? prev.filter((id) => id !== routeId) : [...prev, routeId]
        );
    };

    return (
        <div className="competition-creation-container">
            <h2>Create Competition</h2>
            <div className="form-group">
                <label>Competition Name</label>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter competition name"
                />
            </div>
            <div className="form-group">
                <label>Start Date</label>
                <input
                    type="datetime-local"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
            </div>
            <div className="form-group">
                <label>End Date</label>
                <input
                    type="datetime-local"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </div>
            <div className="form-group">
                <label>Assign Routes</label>
                <div className="routes-list">
                    {routes.map((route) => (
                        <div key={route.id} className="route-item">
                            <input
                                type="checkbox"
                                id={`route-${route.id}`}
                                value={route.id}
                                checked={selectedRoutes.includes(route.id)}
                                onChange={() => toggleRouteSelection(route.id)}
                            />
                            <label htmlFor={`route-${route.id}`}>{route.name}</label>
                        </div>
                    ))}
                </div>
            </div>
            <button onClick={handleCreateCompetition}>Create Competition</button>
            {statusMessage && <p>{statusMessage}</p>}
        </div>
    );
};

export default CompetitionCreation;
