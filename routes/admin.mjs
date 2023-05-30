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
  const details = {
    1: [
      "admins",
      {
        _id:id,
        name: req.body.name ,
        username: req.body.username,
      },
    ],
    2: [
      "doctors",
      {_id: id,
        name: req.body.name,
        username: req.body.username,
      },
    ],
    3: [
      "parents",
      {
        _id: id,
        username: req.body.username,
        name: req.body.name,
        age: req.body.age,
        height: req.body.height,
        weight: req.body.weight,
        gender: req.body.gender,
        dob: req.body.dob,
        bmi: req.body.bmi,
        bloodGroup: req.body.bloodGroup,
        guardianName: req.body.guardianName,
        occupation: req.body.occupation,
        phoneNumber: req.body.phoneNumber,
        address: req.body.address,
      },
    ],
  };

  let type = req.body.type || 3;
  let newUser = {
    _id: id,
    username: req.body.username || "null",
    password: req.body.password || req.body.username || "122",
    type: type,
    createdBy: req.params.admin_id,
    suspended: false,
  };

  if (await userExist(req.body.username)) {
    res.status(200).send("User already exist");
  } else {
    let users = db.collection("users");
    let result = await users.insertOne(newUser);
    if (result.acknowledged) {
      let collection = db.collection(details[type][0]);
      let res2 = await collection.insertOne(details[type][1]);
      if (res2.acknowledged) {
        res.status(200).send("User created successfully");
      } else {
        res.status(200).send("Error inserting details");
      }
    } else {
      console.log(result);
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
  let b = await users.findOne(
    { username: user },
    { projection: { username: 1 } }
  );
  if (b) {
    return true;
  } else {
    return false;
  }
}
