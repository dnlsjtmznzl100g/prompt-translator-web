import React from "react";

interface TranslationResultProps {
  result: {
    step1: string;
    step2: string;
    step3: string;
    step4: string;
  } | null;
}

const TranslationResult: React.FC<TranslationResultProps> = ({ result }) => {
  if (!result) return null;

  return (
    <div style={containerStyle}>
      <h2 style={titleStyle}>Translation Result</h2>

      <div style={stepBox}>
        <h3>Step 1: Direct Translation</h3>
        <p>{result.step1}</p>
      </div>

      <div style={stepBox}>
        <h3>Step 2: Better Word Choice</h3>
        <p>{result.step2}</p>
      </div>

      <div style={stepBox}>
        <h3>Step 3: Add Clarity</h3>
        <p>{result.step3}</p>
      </div>

      <div style={stepBox}>
        <h3>Step 4: Natural Flow</h3>
        <p>{result.step4}</p>
      </div>
    </div>
  );
};

// --- Simple Inline Styles ---
const containerStyle: React.CSSProperties = {
  marginTop: "20px",
  padding: "16px",
  border: "1px solid #ccc",
  borderRadius: "8px",
  backgroundColor: "#fafafa",
};

const titleStyle: React.CSSProperties = {
  marginBottom: "12px",
};

const stepBox: React.CSSProperties = {
  padding: "10px",
  marginBottom: "12px",
  borderRadius: "6px",
  backgroundColor: "#fff",
  border: "1px solid #ddd",
};

export default TranslationResult;

