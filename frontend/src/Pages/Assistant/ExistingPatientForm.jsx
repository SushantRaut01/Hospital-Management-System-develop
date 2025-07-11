import React, { useState } from "react";
import API_BASE_URL from "../../apiConfig";

const ExistingPatientForm = ({ onPatientAdded = () => {} }) => {
  const [pid, setPid] = useState("");
  const [patient, setPatient] = useState(null);
  const [notFound, setNotFound] = useState(false);

  // Handle patient search
  const handleSearch = async (e) => {
    e.preventDefault();
    setNotFound(false);
    setPatient(null);

    try {
      const response = await fetch(
      `${API_BASE_URL}/assistant/search-or-add-patient/?pid=${pid}`
      );
      if (response.ok) {
        const data = await response.json();
        setPatient(data);
      } else {
        setNotFound(true);
      }
    } catch (err) {
      console.error("Search error:", err);
      setNotFound(true);
    }
  };

  // Handle Add Patient button
  const handleAddPatient = async () => {
    try {
      const response = await fetch(
          `${API_BASE_URL}/assistant/search-or-add-patient/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ pid: patient.pid }),
        }
      );

      if (response.ok) {
        const updatedPatient = await response.json();
        onPatientAdded(updatedPatient); // Send to parent
        resetForm(); // Hide popup and reset
      } else {
        console.error("Failed to update status.");
      }
    } catch (error) {
      console.error("Error while adding patient:", error);
    }
  };

  // Reset and close form
  const resetForm = () => {
    setPid("");
    setPatient(null);
    setNotFound(false);
    document.getElementById("popupForm2")?.classList.add("hidden");
  };

  return (
    <div
      id="popupForm2"
      className="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center px-4"
    >
      <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-2xl relative">
        {/* Close Button */}
        <button
          onClick={resetForm}
          className="absolute top-4 right-4 text-2xl text-gray-500 hover:text-black"
        >
          &times;
        </button>

        <h2 className="text-2xl font-semibold mb-4">Search Existing Patient</h2>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="mb-4">
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Enter Patient ID"
              className="w-full border px-3 py-2 rounded"
              value={pid}
              onChange={(e) => setPid(e.target.value)}
              required
            />
            <button
              type="submit"
              className="bg-gray-800 text-white px-5 py-2 rounded-lg hover:bg-gray-900"
            >
              Search
            </button>
          </div>
        </form>

        {/* Not Found Message */}
        {notFound && <p className="text-red-600">No patient found.</p>}

        {/* Patient Info */}
        {patient && (
          <>
            <div className="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-2 gap-3 sm:gap-4 mt-4">
              <input className="border px-3 py-2 rounded" value={patient.name} readOnly />
              <input className="border px-3 py-2 rounded" value={patient.surname} readOnly />
              <input className="border px-3 py-2 rounded" value={patient.age} readOnly />
              <input className="border px-3 py-2 rounded" value={patient.weight} readOnly />
              <input className="border px-3 py-2 rounded" value={patient.phone} readOnly />
              <input className="border px-3 py-2 rounded" value={patient.gender} readOnly />
              <input className="border px-3 py-2 rounded" value={patient.state} readOnly />
              <input className="border px-3 py-2 rounded" value={patient.city} readOnly />
              <div className="col-span-2">
                <input
                  className="border px-3 py-2 rounded w-full"
                  value={patient.address}
                  readOnly
                />
              </div>
            </div>

            {/* Add Patient Button */}
            <div className="col-span-2 mt-6 flex justify-center">
              <button
                onClick={handleAddPatient}
                className="bg-black text-white text-lg px-6 py-3 rounded-lg hover:bg-gray-900 w-full sm:w-auto"
              >
                + Patient Add
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ExistingPatientForm;
