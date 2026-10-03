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
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={bookName}
        onChange={(e) => setBookName(e.target.value)}
        placeholder="Enter Book Name"
      />
      <button type="submit">Add Book</button>
    </form>
  );
};

export default AddBookForm;
