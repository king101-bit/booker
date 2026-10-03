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
    <div className="mx-auto max-w-2xl px-6">
      <h2 className="pb-6 text-2xl font-semibold">Books</h2>

      <AddBookForm addBook={addBook} />

      <div className="mt-6 space-y-2">
        {books.map((book, index) => (
          <div
            key={index}
            className="px-4 py-3 text-lg font-medium"
          >
            {book.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BooksList;
