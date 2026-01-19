import axios from "axios";

const API_URL = "http://127.0.0.1:5000"; // Correct backend URL

export const uploadImage = (file) => {
    const formData = new FormData();
    formData.append("file", file);

    return axios.post(`${API_URL}/process`, formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
};

export const downloadImage = (filename) => {
    return `${API_URL}/download/${filename}`;
};
