import express from "express";
import db from "../db/connection.mjs";
import { ObjectId } from "mongodb";

const router = express.Router();



router.get("/", (req, res) => {
  res.send("<h1>hello world in auth</h1>");
});

router.get("/validate", async (req, res) => {
    console.time("validation");
  let users = db.collection("users");
  
  users.findOne(
    { name: req.query.username },
    { projection: { _id: 0 } },
    (err, result) => {
      if (err) {
        res.status(500).json({ message: "server error try again" });
      } else if (result) {
        if (result.password == req.query.password) {
          if (result.suspended) {
            res.status(200).json({ message: "User suspended by admin",access:false });
          } else {
            res.status(200).json({ message: "Success", type: result.type,access:true });
            console.log("user logged");
            console.log(result);
          }
        } else {
          res.status(200).json({ message: `Password for ${req.query.username} is wrong`,access:false });
          console.log(req.url);
          
        }
      } else {
        res.status(200).json({ message: "User not found",access:false });
        console.log(req.url);
      }
    }
  );
  console.timeEnd("validation");
});





export default router;
