import React, { useEffect, useState } from "react";

function App() {
  const [pipelines, setPipelines] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5004/status")
      .then(res => res.json())
      .then(data => setPipelines(data))
  }, []);

  return (
    <div>
      <h1>MicroLearn Dashboard</h1>
      {pipelines.map((p, i) => (
        <div key={i}>
          <h3>Pipeline {p.id}</h3>
          <p>Status: {p.status}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
