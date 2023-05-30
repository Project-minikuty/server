import express from "express";
import cors from "cors";
import "./loadenv.mjs";
import "express-async-errors";
import auth from "./routes/auth.mjs";
import admin from "./routes/admin.mjs";
import general from "./routes/da.mjs";

import { fileURLToPath } from 'url';
import { dirname } from 'path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PORT = process.env.PORT || 5050;
const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname+"/static"));
app.use("/auth", auth);
app.use("/admin",admin);
app.use("/",general);

app.get("/",(req,res)=>{
  console.time();
  // res.send("server up and running");
  // res.send(page);
  res.sendFile(__dirname+"/static/index.html");
  console.log(req.url);
  console.timeEnd();
  });

app.use('*', (req, res) => {
  res.status(404).json({
    success: 'false',
    message: 'Page not found',
    error: {
      statusCode: 404,
      message: 'You reached a route that is not defined on this server',
    },
  });
});


// start the Express server
app.listen(PORT, () => {
  console.log(`Server is running on port: ${PORT}`);
});