import React, { useCallback, useEffect, useState } from "react";
import api from "../api";
import AddBookForm from "./AddBookForm";
import { Trash2 } from "lucide-react";

const BooksList = () => {
  const [books, setBooks] = useState([]);

  const fetchBooks = useCallback(async () => {
    try {
      const response = await api.get("/books");
      setBooks(response.data.books);
    } catch (error) {
      console.error("Error fetching books", error);
    }
  }, []);

  const addBook = async ({ title, author, price }) => {
    try {
      await api.post("/books", { title, author, price: Number(price) });
      fetchBooks(); // refresh the list after a book has been added
    } catch (error) {
      console.error("error adding books", error);
    }
  };
  const deleteBook = async (bookId) => {
    try {
      await api.delete(`/books/${bookId}`);
      await fetchBooks();
    } catch (error) {
      console.error("Failed to delete book:", error);
    }
  };

  
  useEffect(() => {
    let ignore = false;

    async function loadBooks() {
      try {
        const response = await api.get("/books");
        if (!ignore) setBooks(response.data.books);
      } catch (error) {
        console.error("Error fetching books", error);
      }
    }

    loadBooks();

    return () => {
      ignore = true;
    };
  }, []);

  return (
    <div className="mx-auto max-w-2xl px-6">
      <h2 className="pb-6 text-2xl font-semibold">Books</h2>

      <AddBookForm addBook={addBook} />

      <div className="mt-6 space-y-2">
        {books.map((book) => (
          <div
            key={book.id}
            className="flex items-center justify-between rounded-lg px-4 py-3 text-lg font-medium"
          >
            <div>
              {book.title}{" "}
              <span className="font-normal text-gray-500">
                by {book.author} · ${Number(book.price).toFixed(2)}
              </span>
            </div>

            <button
              type="button"
              onClick={() => deleteBook(book.id)}
              className="text-red-500 hover:text-red-700"
              aria-label={`Delete ${book.title}`}
              title={`Delete ${book.title}`}
            >
              <Trash2 size={18} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BooksList;
