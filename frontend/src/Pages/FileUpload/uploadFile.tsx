import React, { useState } from "react";
import "./upload.css"; // Make sure to import the CSS file where your styles are

const FileUpload: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadStatus, setUploadStatus] = useState<string>("");

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
        formData.append("file", selectedFile);

        try {
            const response = await fetch("http://localhost:8000/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
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
