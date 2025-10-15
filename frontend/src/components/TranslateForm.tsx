import React, { useState } from "react";
import { translate } from "../api/translateApi";

const TranslateForm: React.FC = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await translate(text, "normal");
    setResult(res);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={4}
          cols={50}
        />
        <br />
        <button type="submit">Translate</button>
      </form>

      {result && (
        <div>
          <h3>Translations:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default TranslateForm;

