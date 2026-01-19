import React, { useState, useEffect } from "react";
import UploadForm from "./components/UploadForm";
import ImageResults from "./components/ImageResults";
import "./App.css";

const App = () => {
    const [images, setImages] = useState([]);

    useEffect(() => {
        if (images.length > 0) {
            document.getElementById("processed-images-section").scrollIntoView({
                behavior: "smooth",
            });
        }
    }, [images]);

    return (
        <div className="App">
            <header className="navbar">
                <div className="logo">IMAGE ENHANCER</div>
                <nav>
                    <a href="#home">Home</a>
                    <a href="#about">About Us</a>
                    <a href="#services">Services</a>
                    <a href="#contact">Contact</a>
                    <a href="#login">Login</a>
                    <button className="signup-btn">Sign Up</button>
                </nav>
            </header>
            <main className="hero-section">
                <div className="hero-content">
                    <h1>
                        Enhance your <span className="highlight">images</span> with ease
                    </h1>
                    <p>
                        Our application provides advanced image processing to improve your photos.
                    </p>
                    <UploadForm setImages={setImages} />
                </div>
                <div className="hero-illustration">
                    <div className="phone-mockup"></div>
                </div>
            </main>
            {images.length > 0 && (
                <section id="processed-images-section">
                    <ImageResults images={images} />
                </section>
            )}
        </div>
    );
};

export default App;
