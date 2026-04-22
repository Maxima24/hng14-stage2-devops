import express from "express";
import axios from "axios";
import path from "path";
import * as dotenv from "dotenv";
import cors from "cors";
dotenv.config();
import { fileURLToPath } from "url";

const PORT = process.env.PORT || 3000;
const API_URL = process.env.API_URL || "http://api:8000";
if (!API_URL) {
  console.log("API_URL WAS NOT PASSED");
  console.log(API_URL);
}
if (!PORT) {
  console.log("PORT WAS NOT PASSED");
  console.log(PORT);
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, "views")));
app.use(
  cors({
    origin: "*",
    methods: ["GET", "POST"],
  }),
);

app.post("/submit", async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch {
    res.status(500).json({ error: "something went wrong" });
  }
});

app.get("/status/:id", async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch  {
    res.status(500).json({ error: "something went wrong" });
  }
});

app.listen(PORT, () => {
  console.log("Frontend running on port 3000");
});
