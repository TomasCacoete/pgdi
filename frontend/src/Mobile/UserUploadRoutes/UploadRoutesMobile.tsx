import React, { useState, useContext } from "react";
import "./UploadRoutes.css"; // Make sure to import the CSS file where your styles are
import axios from "axios";
import AuthContext from "../../auth/authContext";
import Navbar from '../Components/Navbar/Navbar'

import Logo from '../../assets/logo2.svg'

const FileUpload: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadStatus, setUploadStatus] = useState<string>("");
    const [errorMessage, setErrorMessage] = useState<string>("");

    const { authTokens } = useContext(AuthContext);

    const headers = { // se nao conseguir ler token pagina nao renderiza
        Authorization: `Bearer ${authTokens.access}`,
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setSelectedFile(event.target.files[0]);
            setErrorMessage(""); // Clear error message when a file is chosen
        } else {
            setSelectedFile(null);
            setErrorMessage("No file chosen");
        }
    };

    const handleFileUpload = async () => {
        if (!selectedFile) {
            setErrorMessage("Please select a file first.");
            return;
        }
    
        const formData = new FormData();
        formData.append("file", selectedFile); // Match this with serializer
    
        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/pgdi_api/create_route/",
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${authTokens.access}`,
                        "Content-Type": "multipart/form-data",
                    },
                }
            );
    
            if (response.status === 201) {
                setUploadStatus("File uploaded successfully!");
                setErrorMessage(""); // Clear error message on successful upload
            } else {
                setUploadStatus("File upload failed.");
                setErrorMessage("Error uploading file.");
            }
        } catch (error) {
            console.error("Upload error:", error);
            setUploadStatus("Error uploading file.");
            setErrorMessage("Error uploading file.");
        }
    };
    

    return (
        <>
        <div className="file-upload-container">
            <div className="logo-container">
                <img src={Logo} alt="Logo" />
            </div>
            <div className="info-container">
                Upload your routes
            </div>  
            <div className="upload-container">
                <div className="header-upload">Upload GPX Files</div>
                <div className="main-upload">
                    <input type="file" className="input-file" onChange={handleFileChange} />
                    <button className="button-upload" onClick={handleFileUpload}>Upload</button>
                    {uploadStatus && <p>{uploadStatus}</p>}
                </div>
            </div>
            <div className="create-gpx-site">
                <p>Don't know how to create GPX files?</p>
                <p><a href="https://www.gpxgenerator.com/">Click here!</a></p>
            </div>
        </div>
        <Navbar></Navbar>
        </>
    );
};

export default FileUpload;