
import "./index.css";
import BooksList from "./components/Books";

function App() {
  return (
    <>
      <section className="min-h-screen bg-black text-white">
        <h1 className="text-4xl font-semibold text-center p-8">Book Management App</h1>
        <BooksList />
      </section>
    </>
  );
}

export default App;
