import React, { useEffect, useState } from "react";
import axios from "axios";

function Ballot() {
  const [ballot, setBallot] = useState(null);
  const [selected, setSelected] = useState([]);

  const user_id = localStorage.getItem("user_id");

  useEffect(() => {
    const fetchBallot = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/ballot/");
        setBallot(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchBallot();
  }, []);

  const toggleSelection = (id) => {
    if (selected.includes(id)) {
      setSelected(selected.filter((c) => c !== id));
    } else {
      if (selected.length < ballot.max_selections) {
        setSelected([...selected, id]);
      } else {
        alert(`You can only select up to ${ballot.max_selections} candidates.`);
      }
    }
  };

  const submitVote = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/vote/", {
        user_id,
        ballot_id: ballot.ballot_id,
        candidate_ids: selected,
      });
      alert(res.data.message);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        alert(err.response.data.error);
      } else {
        alert("Something went wrong");
      }
    }
  };

  if (!ballot) return <p>Loading ballot...</p>;

return (
  <div
    style={{
      minHeight: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      background: "linear-gradient(135deg, #1e3c72, #2a5298)",
      fontFamily: "Arial, sans-serif",
    }}
  >
    <div
      style={{
        background: "white",
        padding: "30px",
        borderRadius: "12px",
        width: "420px",
        boxShadow: "0 10px 25px rgba(0,0,0,0.2)",
        textAlign: "center",
      }}
    >
      {/* Ballot Image */}
      <img
        src="https://cdn-icons-png.flaticon.com/512/3135/3135768.png"
        alt="Ballot"
        style={{ width: "90px", marginBottom: "10px" }}
      />

      <h2 style={{ color: "#1e3c72" }}>{ballot.title}</h2>
      <p>{ballot.description}</p>

      <div style={{ textAlign: "left", marginTop: "20px" }}>
        {ballot.candidates.map((c) => (
          <div key={c.id} style={{ marginBottom: "10px" }}>
            <input
              type="checkbox"
              checked={selected.includes(c.id)}
              onChange={() => toggleSelection(c.id)}
              style={{ marginRight: "8px" }}
            />
            {c.name}
          </div>
        ))}
      </div>

      <button
        onClick={submitVote}
        style={{
          marginTop: "20px",
          width: "100%",
          padding: "10px",
          background: "#2a5298",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        Submit Vote
      </button>

      {/* Results Link */}
      <div style={{ marginTop: "15px" }}>
        <a
          href={`/results/${ballot.id}`}
          style={{
            color: "#2a5298",
            fontWeight: "bold",
            textDecoration: "none",
          }}
        >
          View Results
        </a>
      </div>

    </div>
  </div>
);


}

export default Ballot;
