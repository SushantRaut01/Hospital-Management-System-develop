import React, { useRef } from "react";

const PrintPrescription = () => {
  const iframeRef = useRef(null);

  const handlePrint = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/doctor/generate-prescription/", {
        method: "GET",
        headers: { Accept: "application/pdf" },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch PDF");
      }

      const blob = await response.blob();
      const blobUrl = URL.createObjectURL(blob);

      // Set PDF blob URL into iframe
      const iframe = iframeRef.current;
      iframe.src = blobUrl;

      // Wait for iframe to load before printing
      iframe.onload = () => {
        iframe.contentWindow.focus();
        iframe.contentWindow.print();
      };
    } catch (error) {
      console.error("Print Error:", error);
      alert("Could not generate or print the prescription.");
    }
  };

  return (
    <div className="text-center my-6">
      <button
        onClick={handlePrint}
        className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-6 rounded shadow"
      >
        🖨️ Print Prescription
      </button>

      {/* Hidden iframe to load PDF and trigger print */}
      <iframe
        ref={iframeRef}
        style={{ display: "none" }}
        title="Prescription PDF"
      />
    </div>
  );
};

export default PrintPrescription;
