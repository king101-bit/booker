import { useState } from "react";

const emptyBook = { title: "", author: "", price: "" };

const inputClass =
  "rounded-lg border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20";

const AddBookForm = ({ addBook }) => {
  const [book, setBook] = useState(emptyBook);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setBook((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (book.title && book.author && book.price) {
      addBook(book);
      setBook(emptyBook);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-wrap gap-2">
      <input
        type="text"
        name="title"
        value={book.title}
        onChange={handleChange}
        placeholder="Title"
        className={inputClass}
      />

      <input
        type="text"
        name="author"
        value={book.author}
        onChange={handleChange}
        placeholder="Author"
        className={inputClass}
      />

      <input
        type="number"
        name="price"
        value={book.price}
        onChange={handleChange}
        placeholder="Price"
        min="0"
        step="0.01"
        className={`${inputClass} w-28`}
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
