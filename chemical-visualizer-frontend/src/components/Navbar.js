// Navbar.js
import React from "react";
import "./Navbar.css";

export default function Navbar({ setPage }) {
  return (
    <nav className="navbar">
      <div className="navbar-brand">Chemical Visualizer</div>
      <div className="navbar-buttons">
        <button onClick={() => setPage("upload")}>Upload CSV</button>
        <button onClick={() => setPage("history")}>History</button>
      </div>
    </nav>
  );
}
