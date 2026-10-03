import React, { useState } from "react";

const AddBookForm = ({ addBook }) => {
  const [bookName, setBookName] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (bookName) {
      addBook(bookName);
      setBookName("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={bookName}
        onChange={(e) => setBookName(e.target.value)}
        placeholder="Enter Book Name"
        className="rounded-lg border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
      />

      <button
        type="submit"
        className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700"
      >
        Add Book
      </button>
    </form>
  );
};

export default AddBookForm;
