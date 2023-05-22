import express from "express";
import db from "../db/connection.mjs";
import { ObjectId } from "mongodb";

const router = express.Router();

router.get("/", (req, res) => {
  res.send("<h1>hello world from admin</h1>");
});

router.post("/:admin/create", async (req, res) => {
  console.time("creation");

  let id = ObjectId();
  let newUser = {
    _id: id,
    name: req.body.username,
    password: req.body.password,
    type: req.body.type,
    createdBy: req.params.admin,
    suspended: false,
  };
  if (await userExist(req.body.username)) {
    res.status(400).send("User already exist");
  } else {
    let users = db.collection("users");
    let result = await users.insertOne(newUser);
    if (result.insertedCount === 1) {
      res.status(201).send("User created");
    } else {
      res.status(200).send("User not created");
    }
  }
  console.timeEnd("creation");
});

router.post("/:admin/suspend", async (req, res) => {
  let id = req.params.admin;
  let user = req.body.username;
  if (await userExist(user)) {
    let users = db.collection("users");
    let result = await users.updateOne(
      { name: user },
      { $set: { suspended: true, suspendedBy: id } }
    );
    if (result.acknowledged) {
      res.json({
        message: "user suspended",
        success: true,
      });
    } else {
      res.sendStatus(500);
    }
  } else {
    res.json({
      message: "user not found",
      success: false,
    });
  }
});
router.post("/:admin/reinstate", async (req, res) => {
  let id = req.params.admin;
  let user = req.body.username;
  if (await userExist(user)) {
    let users = db.collection("users");
    let result = await users.updateOne(
      { name: user },
      { $set: { suspended: false, reinstatedBy: id } }
    );
    if (result.acknowledged) {
      res.json({
        message: "user reinstated",
        success: true,
      });
    } else {
      res.sendStatus(500);
    }
  } else {
    res.json({
      message: "user not found",
      success: false,
    });
  }
});

export default router;

async function userExist(user) {
  let users = db.collection("users");
  let b = await users.findOne({ name: user }, { projection: { name: 1 } });
  if (b) {
    return true;
  } else {
    return false;
  }
}
