import express from "express";
import fetch from "node-fetch";  
const app = express();
app.use(express.json());


app.get("/ping", (req, res) => {
  res.json({ status: "ok", service: "service-a" });
});


app.post("/stepA", async (req, res) => {
  try {
    const { message = "", trace = [] } = req.body ?? {};

   
    const upper = String(message).toUpperCase();

    
    const updated = {
      message: upper,
      trace: [
        ...trace,
        {
          service: "srv-a",
          language: "JS",
          info: { uppercased: true }
          
        }
      ]
    };

   
    const rep = await fetch("http://127.0.0.1:9002/stepB", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated)
    });

    if (!rep.ok) {
      const text = await r.text();
      return res.status(502).json({ error: `Service B error: ${text}` });
    }

    const data = await rep.json();
    res.json(data);
  } catch (err) {
    res.status(502).json({ error: `Service A failed: ${String(err)}` });
  }
});


const PORT = 9001;
app.listen(PORT, () => {
  console.log(` Service A listening on http://127.0.0.1:${PORT}`);
});
