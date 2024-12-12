import React, { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() =>
        JSON.parse(localStorage.getItem("authTokens") || "null")
    );
    const [user, setUser] = useState(() =>
        authTokens ? jwtDecode(authTokens.access) : null
    );
    const [loading, setLoading] = useState(true);
    
    const navigate = useNavigate();

    const loginUser = async (username, password) => {
        try {
            const response = await fetch("http://127.0.0.1:8000/auth/login/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (response.ok) {
                setAuthTokens(data);
                setUser(jwtDecode(data.access));
                localStorage.setItem("authTokens", JSON.stringify(data));
                localStorage.setItem("user", JSON.stringify(jwtDecode(data.access)));
                navigate('/user');
            } else {
                console.error("Login failed:", data);
                return data;
            }
        } catch (error) {
            console.error("Login error:", error);
        }
    };

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem("authTokens");
        localStorage.removeItem("user");
    };

    const updateToken = async () => {
        if (!authTokens) return;
        try {
            const response = await fetch("http://127.0.0.1:8000/auth/login/refresh/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ refresh: authTokens.refresh }),
            });
            const data = await response.json();
            if (response.ok) {
                setAuthTokens(data);
                setUser(jwtDecode(data.access));
                localStorage.setItem("authTokens", JSON.stringify(data));
            } else {
                logoutUser();
            }
        } catch (error) {
            console.error("Token refresh error:", error);
            logoutUser();
        }
    };

    useEffect(() => {
        const initialize = async () => {
            if (loading) {
                await updateToken();
                setLoading(false); // Set loading to false after the initial token update
            }
        };
        initialize(); // Call the initialization function

        const interval = setInterval(() => {
            if (authTokens) {
                updateToken();
            }
        }, 1000 * 60 * 15); // Refresh token every 15 minutes

        return () => clearInterval(interval); // Cleanup interval on unmount
    }, [authTokens, loading]);

    const contextData = {
        loginUser,
        authTokens,
        logoutUser,
        updateToken,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export default AuthContext;
