import React, { createContext, useState, useEffect, ReactNode } from "react";
import {jwtDecode} from "jwt-decode";
//import { useNavigate } from "react-router-dom";

// Define interfaces for User and AuthTokens
interface User {
    user_type: string;
    username: string;
    id: number;
}

interface LoginSuccess {
    access: string;
    refresh: string;
}

interface LoginError {
    detail: string; // Error message or response structure on login failure
}

type LoginResponse = LoginSuccess | LoginError;


interface AuthTokens {
    access: string;
    refresh: string;
}

// Context type
interface AuthContextType {
    user: User | null;
    authTokens: AuthTokens | null;
    loginUser: (username: string, password: string) => Promise<LoginResponse>;
    logoutUser: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export default AuthContext;

// Define the props for AuthProvider
interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [authTokens, setAuthTokens] = useState<AuthTokens | null>(() => 
        localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')!) : null
    );
    const [user, setUser] = useState<User | null>(() => 
        localStorage.getItem('authTokens') ? jwtDecode<User>(localStorage.getItem('authTokens')!) : null
    );
    const [loading, setLoading] = useState(true);
    //const navigate = useNavigate();



    const loginUser = async (username: string, password: string) => {
        const response = await fetch('http://127.0.0.1:8000/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'username': username, 'password': password })
        });
        const data = await response.json();

        if (response.status === 200) {
            setAuthTokens(data);
            const decodedToken = jwtDecode<User>(data.access);
            setUser(decodedToken);
            localStorage.setItem('authTokens', JSON.stringify(data));
            localStorage.setItem("user_type", decodedToken.user_type);
            localStorage.setItem("username", decodedToken.username);
            localStorage.setItem("user_id", (decodedToken.id).toString());
            //navigate("/");
        } else {
            return data;
        }
    };

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        localStorage.removeItem('user_type');
        localStorage.removeItem('username');
        localStorage.removeItem('user_id');
        //navigate("/");
    };

    const updateToken = async () => {
        const response = await fetch('http://127.0.0.1:8000//auth/login/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'refresh': authTokens?.refresh })
        });
        const data = await response.json();

        if (response.status === 200) {
            setAuthTokens(data);
            const decodedToken = jwtDecode<User>(data.access);
            setUser(decodedToken);
            localStorage.setItem('authTokens', JSON.stringify(data));
        } else {
            logoutUser();
        }

        if (loading) {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (loading) {
            updateToken();
        }

        const fifteenMinutes = 1000 * 60 * 15;
        const interval = setInterval(() => {
            if (authTokens) {
                updateToken();
            }
        }, fifteenMinutes);
        return () => clearInterval(interval);
    }, [authTokens, loading]);

    const contextData: AuthContextType = {
        user: user,
        authTokens: authTokens,
        loginUser: loginUser,
        logoutUser: logoutUser,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    );
};
