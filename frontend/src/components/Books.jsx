import React, { useEffect, useState } from "react";
import api from "../api";
import AddBookForm from "./AddBookForm";

const BooksList = () => {
  const [books, setBooks] = useState([]);

  const fetchBooks = async () => {
    try {
      const response = await api.get("/books");
      setBooks(response.data.books);
    } catch (error) {
      console.error("Error fetching books", error);
    }
  };

  const addBook = async (bookName) => {
    try {
      await api.post("/books", { name: bookName });
      fetchBooks(); // refresh the list after a book has been added
    } catch (error) {
      console.error("error adding books", error);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <div>
      <h2>Books</h2>
      {books.map((book, index) => (
        <div key={index}>{book.name}</div>
      ))}
      <AddBookForm addBook={addBook} />
    </div>
  );
};

export default BooksList;
