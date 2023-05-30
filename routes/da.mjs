import express from "express";
import db from "../db/connection.mjs";
import { ObjectId } from "mongodb";

const router = express.Router();

router
  .route("/da")
  .get((req, res) => {
    res.send("<h1>hello world from get doctor</h1>");
  })
  .post((req, res) => {
    res.send("<h1>hello world from post doctor</h1>");
  });

router
  .route("/sNames")
  .get((req,res) => {
    res.json({ error: "method error" });
  })
  .post(async (req, res) => {
    let students = db.collection("parents");
    let names = await students
      .find({}, { projection: { name: 1, username: 1 } })
      .toArray();
    res.send(names);
  });
router.post("/dNames", async (req, res) => {
  let students = db.collection("doctors");
  let names = await students
    .find({}, { projection: { name: 1, username: 1 } })
    .toArray();
  res.send(names);
});
router.post("/aNames", async (req, res) => {
  let students = db.collection("admins");
  let names = await students
    .find({}, { projection: { name: 1, username: 1 } })
    .toArray();
  res.send(names);
});

router.route("/sDetails").get((req,res)=>{
  res.sendStatus(403);
}).post(async (req,res)=>{
  let id=req.body.id;
  let students=db.collection("parents");
  let s = await students.findOne({_id:ObjectId(id)});
  
  res.send(s.name);
});
export default router;
