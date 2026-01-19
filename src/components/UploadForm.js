import React, { useState } from "react";
import { uploadImage } from "../api";

const UploadForm = ({ setImages }) => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return alert("Please select an image!");

        setLoading(true);

        try {
            const response = await uploadImage(file);
            setImages(response.data.file_names);
        } catch (error) {
            alert("Error processing the image!");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-form advanced-upload-box">
            <form onSubmit={handleSubmit}>
                <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => setFile(e.target.files[0])}
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Processing..." : "Upload and Process"}
                </button>
            </form>
        </div>
    );
};

export default UploadForm;
