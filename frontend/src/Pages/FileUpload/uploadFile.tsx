import React, { useState, useContext } from "react";
import "./upload.css"; // Make sure to import the CSS file where your styles are
import axios from "axios";
import AuthContext from "../../auth/authContext";

const FileUpload: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadStatus, setUploadStatus] = useState<string>("");

    const { authTokens } = useContext(AuthContext);

    const headers = { // se nao conseguir ler token pagina nao renderiza
        Authorization: `Bearer ${authTokens.access}`,
        };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const handleFileUpload = async () => {
        if (!selectedFile) {
            alert("Please select a file first.");
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
            } else {
                setUploadStatus("File upload failed.");
            }
        } catch (error) {
            console.error("Upload error:", error);
            setUploadStatus("Error uploading file.");
        }
    };
    

    return (
        <div className="file-upload-container">
            <h2>File Upload</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Upload</button>
            {uploadStatus && <p>{uploadStatus}</p>}
        </div>
    );
};

export default FileUpload;
