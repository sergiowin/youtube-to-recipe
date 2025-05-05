import React, { useEffect, useState } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import { FaChevronLeft, FaChevronRight, FaTrash } from "react-icons/fa";

const API_BASE = "http://127.0.0.1:5000/api";

function App() {
  const [url, setUrl] = useState("");
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);

  const fetchRecipes = async () => {
    try {
      const res = await axios.get(`${API_BASE}/recipes`);
      setRecipes(res.data);
      setCurrentIndex(0);
    } catch (err) {
      setError("Failed to fetch recipes.");
    }
  };

  useEffect(() => {
    fetchRecipes();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");
    try {
      const res = await axios.post(`${API_BASE}/recipes/process`, { url });
      setSuccess("Recipe extracted and saved!");
      setUrl("");
      fetchRecipes();
      setCurrentIndex(0);
    } catch (err) {
      setError(
        err.response?.data?.error || "Failed to process the YouTube video link."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this recipe?")) return;
    try {
      await axios.delete(`${API_BASE}/recipes/${id}`);
      setSuccess("Recipe deleted.");
      fetchRecipes();
      setCurrentIndex(0);
    } catch (err) {
      setError("Failed to delete recipe.");
    }
  };

  const handlePrev = () => {
    setCurrentIndex((prev) => (prev > 0 ? prev - 1 : recipes.length - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prev) => (prev < recipes.length - 1 ? prev + 1 : 0));
  };

  const currentRecipe = recipes[currentIndex] || null;

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-emerald-100 via-blue-100 to-emerald-200">
      <div className="w-full max-w-7xl mx-auto bg-white/90 rounded-3xl shadow-2xl p-16 flex flex-col gap-16 border border-emerald-200 backdrop-blur-md items-center justify-center">
        <h1 className="text-6xl font-extrabold text-center text-emerald-700 tracking-tight drop-shadow mb-6">
          YouTube Recipe Extractor
        </h1>
        <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-8 items-center justify-center mb-8 w-full max-w-3xl mx-auto">
          <input
            type="url"
            className="border-2 border-emerald-200 rounded-lg px-8 py-4 w-full md:w-2/3 focus:outline-none focus:ring-2 focus:ring-emerald-300 transition text-xl shadow-sm bg-emerald-50 text-black placeholder-emerald-400"
            placeholder="Paste YouTube video link here..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
          />
          <button
            type="submit"
            className="bg-gradient-to-r from-emerald-400 to-emerald-600 text-white px-10 py-4 rounded-lg font-semibold shadow-lg hover:scale-105 transition-transform w-full md:w-auto text-xl border border-emerald-300"
            disabled={loading}
          >
            {loading ? "Processing..." : "Extract Recipe"}
          </button>
        </form>
        <AnimatePresence>
          {error && (
            <motion.div
              className="text-red-600 mb-2 text-center text-lg font-medium"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              {error}
            </motion.div>
          )}
          {success && (
            <motion.div
              className="text-emerald-600 mb-2 text-center text-lg font-medium"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              {success}
            </motion.div>
          )}
        </AnimatePresence>
        <div className="flex flex-col items-center gap-12 w-full">
          <h2 className="text-4xl font-semibold text-emerald-700 mb-2">Recipes</h2>
          {recipes.length === 0 ? (
            <div className="text-emerald-400 text-xl">No recipes found.</div>
          ) : (
            <div className="w-full flex flex-col items-center gap-8">
              <div className="flex items-center justify-center gap-10 w-full">
                <button
                  className="p-4 rounded-full bg-emerald-100 hover:bg-emerald-200 transition shadow border border-emerald-200"
                  onClick={handlePrev}
                  aria-label="Previous Recipe"
                >
                  <FaChevronLeft className="text-4xl text-emerald-700" />
                </button>
                <div className="flex-1 max-w-6xl flex justify-center">
                  <AnimatePresence mode="wait">
                    {currentRecipe && (
                      <motion.div
                        key={currentRecipe.id}
                        className="bg-emerald-50/80 rounded-2xl p-12 shadow-xl border border-emerald-100 flex flex-col gap-8 w-[900px] overflow-y-auto transition-all duration-300 items-center justify-start"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 20 }}
                        layout
                      >
                        <h2 className="text-4xl font-bold mb-4 text-emerald-800 px-2 py-1 text-center">
                          {currentRecipe.title}
                        </h2>
                        <div className="mb-2 text-emerald-900 break-all px-2 py-1 text-lg w-full text-center">
                          <span className="font-semibold">YouTube Link: </span>
                          <a
                            href={currentRecipe.youtube_url}
                            className="text-emerald-600 underline"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {currentRecipe.youtube_url}
                          </a>
                        </div>
                        {currentRecipe.cooking_time && (
                          <div className="mb-2 px-2 py-1 text-lg w-full text-center">
                            <span className="font-semibold">Cooking Time: </span>
                            {currentRecipe.cooking_time}
                          </div>
                        )}
                        {currentRecipe.servings && (
                          <div className="mb-2 px-2 py-1 text-lg w-full text-center">
                            <span className="font-semibold">Servings: </span>
                            {currentRecipe.servings}
                          </div>
                        )}
                        <div className="mb-2 px-2 py-1 w-full">
                          <span className="font-semibold">Ingredients:</span>
                          <ul className="list-disc list-inside ml-4 text-lg">
                            {currentRecipe.ingredients?.map((ing, idx) => (
                              <li key={idx}>{ing}</li>
                            ))}
                          </ul>
                        </div>
                        <div className="px-2 py-1 w-full">
                          <span className="font-semibold">Instructions:</span>
                          <ol className="list-decimal list-inside ml-4 text-lg">
                            {currentRecipe.instructions?.map((step, idx) => (
                              <li key={idx}>{step}</li>
                            ))}
                          </ol>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
                <button
                  className="p-4 rounded-full bg-emerald-100 hover:bg-emerald-200 transition shadow border border-emerald-200"
                  onClick={handleNext}
                  aria-label="Next Recipe"
                >
                  <FaChevronRight className="text-4xl text-emerald-700" />
                </button>
              </div>
              <div className="flex gap-3 mt-2">
                {recipes.map((_, idx) => (
                  <button
                    key={idx}
                    className={`w-4 h-4 rounded-full ${idx === currentIndex ? "bg-emerald-700" : "bg-emerald-100"}`}
                    onClick={() => setCurrentIndex(idx)}
                    aria-label={`Go to recipe ${idx + 1}`}
                  />
                ))}
              </div>
              {currentRecipe && (
                <div className="flex justify-center mt-6">
                  <button
                    className="flex items-center gap-3 px-7 py-3 bg-red-100 text-red-600 rounded-lg shadow hover:bg-red-200 transition font-semibold border border-red-200 text-lg"
                    onClick={() => handleDelete(currentRecipe.id)}
                    aria-label="Delete Recipe"
                  >
                    <FaTrash /> Delete Recipe
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
