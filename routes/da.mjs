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
  .get((req, res) => {
    res.sendStatus(403);
  })
  .post(async (req, res) => {
    let students = db.collection("parents");
    let names = await students
      .find({}, { projection: { name: 1, username: 1 } })
      .toArray();
    res.send(names);
  });
router
  .route("/dNames")
  .get((req, res) => {
    res.sendStatus(403);
  })
  .post(async (req, res) => {
    let students = db.collection("doctors");
    let names = await students
      .find({}, { projection: { name: 1, username: 1 } })
      .toArray();
    res.send(names);
  });
router
  .route("/aNames")
  .get((req, res) => {
    res.sendStatus(403);
  })
  .post(async (req, res) => {
    let students = db.collection("admins");
    let names = await students
      .find({}, { projection: { name: 1, username: 1 } })
      .toArray();
    res.send(names);
  });

router
  .route("/sDetails")
  .get((req, res) => {
    res.sendStatus(403);
  })
  .post(async (req, res) => {
    let id = req.body.id;
    let students = db.collection("parents");
    let s = await students.findOne({ _id: ObjectId(id) });
    res.send(s);
  });
router
  .route("/dDetails")
  .get((req, res) => {
    res.sendStatus(403);
  })
  .post(async (req, res) => {
    let id = req.body.id;
    let doctors = db.collection("doctors");
    let d = await doctors.findOne({ _id: ObjectId(id) });
    res.send(d);
  });
router
  .route("/aDetails")
  .get((req, res) => {
    res.sendStatus(403);
  })
  .post(async (req, res) => {
    let id = req.body.id;
    let admins = db.collection("admins");
    let a = await admins.findOne({ _id: ObjectId(id) });
    res.send(a);
  });

  
export default router;
