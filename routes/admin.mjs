import express from "express";
import db from "../db/connection.mjs";
import { ObjectId } from "mongodb";

const router = express.Router();

router.get("/", (req, res) => {
  res.send("<h1>hello world from admin</h1>");
});

router.post("/:admin_id/create", async (req, res) => {
  console.time("creation");

  let id = ObjectId();
  let newUser = {
    _id: id,
    username: req.body.username || "null",
    password: req.body.password || req.body.username || "122",
    type: req.body.type || "parent",
    createdBy: req.params.admin_id,
    suspended: false,
  };
  if (await userExist(req.body.username)) {
    res.status(200).send("User already exist");
  } else {
    let users = db.collection("users");
    let result = await users.insertOne(newUser);
    if (result.acknowledged) {
      res.status(201).send("User created");
    } else {
      console.log(result)
      res.status(200).send("User not created");
    }
  }
  console.timeEnd("creation");
});

router.post("/:admin_id/suspend", async (req, res) => {
  let id = req.params.admin_id;
  let user = req.body.username;
  if (await userExist(user)) {
    let users = db.collection("users");
    let result = await users.updateOne(
      { username: user },
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
router.post("/:admin_id/reinstate", async (req, res) => {
  let id = req.params.admin_id;
  
  let user = req.body.username;
  if (await userExist(user)) {
    let users = db.collection("users");
    let result = await users.updateOne(
      { username: user },
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
  let b = await users.findOne({ username: user }, { projection: { username: 1 } });
  if (b) {
    return true;
  } else {
    return false;
  }
}
