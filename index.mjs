import express from "express";
import cors from "cors";
import "./loadenv.mjs";
import "express-async-errors";
import posts from "./routes/auth.mjs";

const PORT = process.env.PORT || 5050;
const app = express();

app.use(cors());
app.use(express.json());

// Load the /posts routes
app.use("/auth", posts);

// Global error handling
// This should be the last route else any after it wont work
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