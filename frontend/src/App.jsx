import { useState } from "react";
import heroImg from "./assets/hero.png";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import "./App.css";
import BooksList from "./components/Books";

function App() {
  return (
    <>
      <section id="center">
        <h1>Book Management App</h1>
        <BooksList />
      </section>
      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  );
}

export default App;
