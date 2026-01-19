import React from "react";
import { downloadImage } from "../api";

const ImageResults = ({ images }) => {
    return (
        <div className="processed-images">
            <h2>Processed Images</h2>
            <div className="images-grid">
                {images.map((image, index) => (
                    <div className="image-card" key={index}>
                        <img
                            src={downloadImage(image)}
                            alt={`Processed Part ${index + 1}`}
                            className="image-preview"
                        />
                        <a href={downloadImage(image)} download>
                            <button className="download-btn">Download</button>
                        </a>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ImageResults;
