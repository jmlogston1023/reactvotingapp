import { useEffect, useState } from "react";
import axios from "axios";

function Results() {

  const [results, setResults] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {

      const res = await axios.get(
        "/api/results/1/"
      );

      setResults(res.data);
    };

    fetchResults();
  }, []);

  if (!results) return <p>Loading...</p>;

  return (
    <div style={{width:"500px", margin:"auto"}}>
      <h2>{results.ballot}</h2>

      <p>Total Votes: {results.total_votes}</p>

      {results.results.map((r,i)=>(
        <div key={i} style={{marginBottom:"10px"}}>

          <strong>{r.candidate}</strong>

          <div style={{
            background:"#ddd",
            height:"20px",
            width:"100%"
          }}>

            <div style={{
              background:"#007BFF",
              height:"20px",
              width:`${(r.votes/results.total_votes)*100}%`
            }}></div>

          </div>

          {r.votes} votes

        </div>
      ))}

    </div>
  )
}

export default Results;
